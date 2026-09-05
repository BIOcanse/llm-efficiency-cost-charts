"""Import owner snapshots once; derive data and optionally render final charts.

Run from the repository root. Existing raw observations are immutable. Rebuilds
consume the saved source, and a frozen benchmark cannot receive another date.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from core import OWNER_API, OWNER_REVISION, VERSIONS, derive, normalized_rows, ranked, owner_url

ROOT = Path(__file__).resolve().parents[2]
RAW = "https://raw.githubusercontent.com/BIOcanse/llm-efficiency-cost-charts/main/"
REPO = "https://github.com/BIOcanse/llm-efficiency-cost-charts/"


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pending = path.with_suffix(path.suffix + ".tmp")
    pending.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    pending.replace(path)


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0]) if rows else ["id"]
    pending = path.with_suffix(".csv.tmp")
    with pending.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: json.dumps(value, ensure_ascii=False) if isinstance(value, (list, dict)) else value for key, value in row.items()})
    pending.replace(path)


def adapt_legacy_one(source: dict) -> dict:
    rows = []
    for ordinal, old in enumerate(source["rows"]):
        rows.append({"id": f"tb1-{ordinal:03d}-{old['key']}", "status": "display",
                     "metadata": {"model_display": old["model"], "model_org": old["modelOrganization"],
                                  "agent_display": {"label": old["agent"], "url": old.get("agentUrl")},
                                  "agent_version": old.get("agentVersion"), "date": old["date"],
                                  "verified": old.get("verified")},
                     "metrics": {"accuracy": old["accuracy"] * 100,
                                 "accuracy_ci95_half_width": old["stderr"] * 100 * 1.96}})
    return {"leaderboard": {"title": "Terminal-Bench 1.0", "dataset": "terminal-bench-core==0.1.1"}, "rows": rows}


def import_source(version: str, snapshot: str, evidence_dir: Path | None) -> dict:
    target = ROOT / "data" / "terminal-bench" / version / snapshot / "source.json"
    if target.exists():
        envelope = json.loads(target.read_text(encoding="utf-8"))
        raw_bytes = (target.parent / "leaderboard.raw.json").read_bytes()
        if hashlib.sha256(raw_bytes).hexdigest() != envelope["source_sha256"] or json.loads(raw_bytes) != envelope["response"]:
            raise ValueError(f"Saved source integrity mismatch: {target}")
        return envelope
    prior = list(target.parent.parent.glob("*/source.json"))
    if VERSIONS[version]["status"] == "frozen" and prior:
        raise ValueError(f"TB {version} is frozen at {prior[0].parent.name}; no new snapshots")
    source_time = datetime.now(timezone.utc)
    if evidence_dir:
        source_file = evidence_dir / f"leaderboard-{version}.json"
        content = source_file.read_bytes()
        source_time = datetime.fromtimestamp(source_file.stat().st_mtime, timezone.utc)
    else:
        if version == "1.0":
            raise ValueError("TB1 requires the pinned, converted official static source")
        parameters = {key: VERSIONS[version][key] for key in ("package", "name")}
        request = urllib.request.Request(OWNER_API, data=json.dumps(parameters).encode(), headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(request, timeout=45) as response:
            content = response.read(4_000_000)
    raw = json.loads(content)
    envelope = {"benchmark_version": version, "snapshot": snapshot,
                "retrieved_at_utc": source_time.isoformat().replace("+00:00", "Z"),
                "source_sha256": hashlib.sha256(content).hexdigest(),
                "owner_website_revision": OWNER_REVISION,
                "source_url": raw.get("provenance", {}).get("sourceUrl", OWNER_API),
                "request": {key: VERSIONS[version].get(key) for key in ("package", "name")},
                "dataset": VERSIONS[version], "response": raw}
    target.parent.mkdir(parents=True, exist_ok=True)
    # Preserve the downloaded bytes separately so the hash is independently checkable.
    (target.parent / "leaderboard.raw.json").write_bytes(content)
    if version == "1.0" and evidence_dir:
        (target.parent / "leaderboard.raw.ts").write_bytes((evidence_dir / "app__(home)__leaderboard__data.ts").read_bytes())
    atomic_json(target, envelope)
    return envelope


def build(version: str, snapshot: str, evidence_dir: Path | None, render: bool, access_policy: Path | None = None) -> dict:
    data_dir = ROOT / "data" / "terminal-bench" / version / snapshot
    policy_path = data_dir / "access_policy.json"
    if not policy_path.exists():
        if access_policy is None:
            raise ValueError("A new snapshot requires an explicitly audited --access-policy file")
        policy = json.loads(access_policy.read_text(encoding="utf-8"))
    else:
        policy = json.loads(policy_path.read_text(encoding="utf-8"))
        if access_policy is not None and json.loads(access_policy.read_text(encoding="utf-8")) != policy:
            raise ValueError("Saved access policy is immutable; create a new TB4 snapshot")
    datetime.strptime(policy["as_of_utc"], "%Y-%m-%d")
    source = import_source(version, snapshot, evidence_dir)
    if not policy_path.exists():
        atomic_json(policy_path, policy)
    raw = adapt_legacy_one(source["response"]) if version == "1.0" else source["response"]
    rows, validation = derive(normalized_rows(raw, version), policy)
    chart_relative = f"charts/terminal-bench/{version}/{snapshot}"
    rank_relative = f"rankings/terminal-bench/{version}/{snapshot}"
    metadata = {
        "id": snapshot, "benchmark_version": version, "status": VERSIONS[version]["status"],
        "retrieved_at_utc": source["retrieved_at_utc"],
        "built_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "payload": f"data/terminal-bench/{version}/{snapshot}.json",
        "release_url": f"{REPO}releases/tag/terminal-bench-{snapshot}",
        "data_url": f"{REPO}tree/main/data/terminal-bench/{version}/{snapshot}",
        "ranking_base": RAW + rank_relative, "chart_base": RAW + chart_relative,
        "task_count": VERSIONS[version]["tasks"], "counts": validation["counts"], "configurations": len(rows),
    }
    prior_payload = ROOT / "site" / metadata["payload"]
    payload = {"schema_version": 1, "benchmark": f"Terminal-Bench {version}", "snapshot": metadata,
               "counts": validation["counts"], "rows": rows, "access_policy": policy,
               "validation": validation, "source_sha256": source["source_sha256"],
               "owner_url": owner_url(version),
               "dataset": VERSIONS[version], "exports": {}}
    write_csv(data_dir / "results.csv", rows)
    write_csv(data_dir / "subscription_costs.csv", [row for row in rows])
    atomic_json(data_dir / "validation.json", validation)
    for metric in ("subscription", "api", "token"):
        write_csv(ROOT / rank_relative / f"{metric}_ranking.csv", ranked(rows, metric))
    write_csv(ROOT / rank_relative / "success_rate_ranking.csv", rows)
    if render:
        from render import render_all
        payload["exports"], layouts = render_all(payload, ROOT / chart_relative)
        validation["static_layouts"] = layouts
        atomic_json(data_dir / "validation.json", validation)
    elif prior_payload.exists():
        previous = json.loads(prior_payload.read_text(encoding="utf-8"))
        if previous["rows"] == rows and previous["access_policy"] == policy:
            payload["exports"] = previous.get("exports", {})
            if "static_layouts" in previous["validation"]:
                validation["static_layouts"] = previous["validation"]["static_layouts"]
    atomic_json(data_dir / "validation.json", validation)
    atomic_json(prior_payload, payload)
    print(json.dumps({"version": version, **validation}, ensure_ascii=False), flush=True)
    return metadata


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", required=True)
    parser.add_argument("--versions", nargs="+", choices=list(VERSIONS), default=["4.0"])
    parser.add_argument("--evidence-dir", type=Path)
    parser.add_argument("--access-policy", type=Path, help="Audited dated policy; required for new snapshots")
    parser.add_argument("--render", action="store_true")
    args = parser.parse_args()
    datetime.strptime(args.snapshot, "%Y-%m-%d")
    manifest_path = ROOT / "site/data/terminal-bench.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {"schema_version": 1, "current_version": "4.0", "versions": []}
    by_version = {item["id"]: item for item in manifest["versions"]}
    for version in args.versions:
        metadata = build(version, args.snapshot, args.evidence_dir, args.render, args.access_policy)
        entry = by_version.get(version, {"id": version, "status": VERSIONS[version]["status"], "snapshots": []})
        entry["snapshots"] = [item for item in entry["snapshots"] if item["id"] != args.snapshot] + [metadata]
        entry["snapshots"].sort(key=lambda item: item["id"], reverse=True)
        entry["current_snapshot"] = entry["snapshots"][0]["id"]
        by_version[version] = entry
    manifest["versions"] = sorted(by_version.values(), key=lambda item: tuple(map(int, item["id"].split("."))), reverse=True)
    atomic_json(manifest_path, manifest)


if __name__ == "__main__":
    main()
