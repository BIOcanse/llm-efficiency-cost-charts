from __future__ import annotations

import hashlib
import json
import math
import random
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from core import component_semantics, derive, normalized_rows, ranked, frontier_rows, FRONTIER_KEYS
from build_snapshot import adapt_legacy_one, build, import_source

ROOT = Path(__file__).resolve().parents[2]


class MeasurementTests(unittest.TestCase):
    def test_frontier_ties_and_missing(self):
        points = [("a", 0, 10), ("b", 0, 10), ("c", 1, 10), ("d", 1, 20), ("e", 2, 19), ("f", 3, 30), ("g", None, 100), ("h", math.nan, 100), ("i", -1, 100), ("j", 0, None)]
        rows = [{"id": name, "api_per_attempt": x, "score": y} for name, x, y in points]
        self.assertEqual([row["id"] for row in frontier_rows(rows, "api")], ["a", "b", "d", "f"])
        self.assertEqual(frontier_rows([], "api"), [])

    def test_frontier_against_independent_pairs(self):
        rng = random.Random(270907)
        for _ in range(100):
            rows = [{"id": str(i), "api_per_attempt": rng.randrange(10), "score": rng.randrange(10)} for i in range(25)]
            expected = [row for row in rows if not any(other["api_per_attempt"] <= row["api_per_attempt"] and other["score"] >= row["score"] and (other["api_per_attempt"] < row["api_per_attempt"] or other["score"] > row["score"]) for other in rows)]
            self.assertEqual({row["id"] for row in frontier_rows(rows, "api")}, {row["id"] for row in expected})

    def test_inclusive_and_disjoint_input(self):
        inclusive = {"total_tokens": 110, "uncached_input_tokens": 100, "cached_input_tokens": 90, "output_tokens": 10}
        self.assertEqual(component_semantics(inclusive), "named_uncached_field_includes_cache_arithmetically")
        self.assertEqual(component_semantics({**inclusive, "uncached_input_tokens": 10}), "disjoint_components_match")
        self.assertEqual(component_semantics({"total_tokens": 110}), "components_missing")
        self.assertEqual(component_semantics({**inclusive, "total_tokens": 99}), "components_do_not_reconcile")

    def test_missing_is_not_zero_and_zero_success_never_wins(self):
        raw = {"rows": [{"id": "zero", "metadata": {"model_display": "M", "agent_display": "A"}, "metrics": {"accuracy": 0, "n_trials": 10, "successes": 0, "total_tokens": 100, "total_cost_usd": 5}}, {"id": "missing", "metadata": {"model_display": "N", "agent_display": "A"}, "metrics": {"accuracy": 50, "n_trials": 0}}]}
        rows = normalized_rows(raw, "4.0")
        zero = next(row for row in rows if row["id"] == "zero")
        missing = next(row for row in rows if row["id"] == "missing")
        self.assertEqual(zero["api_per_attempt"], 0.5)
        self.assertIsNone(zero["api_per_success"])
        self.assertIsNone(missing["trials"])
        self.assertIsNone(missing["token_per_attempt"])
        self.assertEqual(ranked(rows, "api"), [])

    def test_success_count_consistency(self):
        with self.assertRaisesRegex(ValueError, "reconcile"):
            normalized_rows({"rows": [{"id": "bad", "metadata": {}, "metrics": {"accuracy": 50, "n_trials": 10, "successes": 1}}]}, "4.0")

    def test_zero_cost_is_not_missing(self):
        rows = [{"model": "free", "score": 50, "api_per_success": 0}, {"model": "paid", "score": 50, "api_per_success": 2}]
        ranking = ranked(rows, "api")
        self.assertEqual(ranking[0]["model"], "free")
        self.assertEqual(ranking[0]["relative_value_percent"], 100)
        self.assertEqual(ranking[0]["relative_cost_percent"], 0)
        self.assertEqual(ranking[1]["relative_value_percent"], 0)

    def test_new_snapshot_requires_review_and_legacy_is_frozen(self):
        with TemporaryDirectory(prefix="terminal-bench-test-") as temporary:
            root = Path(temporary)
            with patch("build_snapshot.ROOT", root):
                with self.assertRaisesRegex(ValueError, "explicitly audited"):
                    build("4.0", "2099-01-01", None, False)
                previous = root / "data/terminal-bench/3.0/2026-09-05/source.json"
                previous.parent.mkdir(parents=True)
                previous.write_text("{}", encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "frozen"):
                    import_source("3.0", "2099-01-01", None)

    def test_published_artifacts(self):
        from PIL import Image

        manifest = json.loads((ROOT / "site/data/terminal-bench.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["current_version"], "4.0")
        file_counts = {".png": 0, ".svg": 0}
        for version in manifest["versions"]:
            if version["id"] != "4.0":
                self.assertEqual(len(version["snapshots"]), 1)
                self.assertEqual(version["status"], "frozen")
            for snapshot in version["snapshots"]:
                payload = json.loads((ROOT / "site" / snapshot["payload"]).read_text(encoding="utf-8"))
                self.assertEqual(payload["snapshot"], snapshot)
                self.assertTrue(snapshot["retrieved_at_utc"].endswith("Z"))
                self.assertTrue(snapshot["built_at_utc"].endswith("Z"))
                stack = [payload["validation"]["static_layouts"]]
                while stack:
                    item = stack.pop()
                    if isinstance(item, dict):
                        for key, value in item.items():
                            if key in {"label_collisions", "out_of_bounds_labels", "text_collisions", "out_of_bounds"}:
                                self.assertEqual(value, 0, (version["id"], key))
                            elif isinstance(value, (dict, list)):
                                stack.append(value)
                    elif isinstance(item, list):
                        stack.extend(item)
                self.assertEqual(set(payload["exports"]), {"en", "zh-CN"})
                for locale, files in payload["exports"].items():
                    for name in files:
                        path = ROOT / "charts/terminal-bench" / version["id"] / snapshot["id"] / locale / name
                        self.assertTrue(path.is_file(), path)
                        file_counts[path.suffix] += 1
                        if path.suffix == ".png":
                            with Image.open(path) as picture:
                                self.assertEqual(picture.size, (4800, 2700))
        self.assertEqual(file_counts[".png"], file_counts[".svg"])
        self.assertGreaterEqual(file_counts[".png"], 60)

    def test_snapshot_reconciliation(self):
        expected = {"4.0": (18, 18, 16), "3.0": (12, 11, 7), "2.1": (22, 22, 18), "2.0": (0, 0, 0), "1.0": (0, 0, 0)}
        for version, counts in expected.items():
            with self.subTest(version=version):
                directory = ROOT / "data/terminal-bench" / version / "2026-09-05"
                envelope = json.loads((directory / "source.json").read_text(encoding="utf-8"))
                self.assertEqual(hashlib.sha256((directory / "leaderboard.raw.json").read_bytes()).hexdigest(), envelope["source_sha256"])
                raw = adapt_legacy_one(envelope["response"]) if version == "1.0" else envelope["response"]
                policy = json.loads((directory / "access_policy.json").read_text(encoding="utf-8"))
                rows, validation = derive(normalized_rows(raw, version), policy)
                self.assertEqual(tuple(validation["counts"][key] for key in ("token", "api", "subscription")), counts)
                published = json.loads((ROOT / f"site/data/terminal-bench/{version}/2026-09-05.json").read_text(encoding="utf-8"))
                self.assertEqual(rows, published["rows"])
                for metric, key in FRONTIER_KEYS.items():
                    selected = frontier_rows(rows, metric)
                    self.assertEqual(published["frontiers"][metric], [row["id"] for row in selected])
                    eligible = [row for row in rows if row[key] is not None]
                    oracle = [row for row in eligible if not any(other[key] <= row[key] and other["score"] >= row["score"] and (other[key] < row[key] or other["score"] > row["score"]) for other in eligible)]
                    self.assertEqual({row["id"] for row in selected}, {row["id"] for row in oracle})
                for row in rows:
                    if row["token_per_attempt"] is not None:
                        self.assertTrue(math.isclose(row["token_per_attempt"] * row["trials"], row["total_tokens"], rel_tol=1e-12))
                    if row["api_per_attempt"] is not None:
                        self.assertTrue(math.isclose(row["api_per_attempt"] * row["trials"], row["total_api_usd"], rel_tol=1e-12))
                    if row["successes"] and row["api_per_success"] is not None:
                        self.assertTrue(math.isclose(row["api_per_success"] * row["successes"], row["total_api_usd"], rel_tol=1e-12))
                for metric in ("subscription", "api", "token"):
                    ranking = ranked(rows, metric)
                    if ranking:
                        self.assertEqual(ranking[0]["relative_value_percent"], 100)
                        self.assertEqual(ranking[-1]["relative_cost_percent"], 100)
                if version == "4.0":
                    astra = [row for row in rows if row["base_model"] == "GPT-6 Astra"]
                    self.assertEqual(len(astra), 5)
                    self.assertTrue(all(row["api_value_ratio"] == 70 for row in astra))
                    glm = next(row for row in rows if row["base_model"] == "GLM-5.3")
                    self.assertAlmostEqual(glm["subscription_offpeak_per_attempt"], glm["subscription_per_attempt"] / 2)
                    self.assertEqual(glm["access_confidence"], "low")
                if version == "1.0":
                    self.assertEqual(len(rows), 62)
                    self.assertEqual(len({row["id"] for row in rows}), 62)
                    self.assertEqual(max(row["score"] for row in rows), 64.5)
                    self.assertTrue(all("/blob/" in row["source_url"] for row in rows))
                if version == "2.1":
                    exceptions = [row for row in rows if row["trial_count_note"].startswith("metrics_count_preferred")]
                    self.assertEqual(len(exceptions), 1)
                    self.assertEqual(exceptions[0]["trials"], 447)
                    self.assertEqual(exceptions[0]["raw_associated_n_trials"], 445)


if __name__ == "__main__":
    unittest.main(verbosity=2)
