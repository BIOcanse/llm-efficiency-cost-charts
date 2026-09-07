"""Terminal-Bench normalization and transparent, dated cost derivation.

No renderer or website code guesses missing fields. Published totals own the
denominators; token component semantics are recorded, never silently changed.
"""
from __future__ import annotations

import math
from collections import Counter
from typing import Any


VERSIONS = {
    "4.0": {"tasks": 66, "status": "active", "package": "terminal-bench/terminal-bench", "name": "4-0-0", "dataset_commit": "452bf305c6daa62fc59061d22133a7cbc7c1572e"},
    "3.0": {"tasks": 74, "status": "frozen", "package": "terminal-bench/terminal-bench", "name": "3-0-0", "dataset_commit": "2b0442c3c583b710ca8da14c8e601b99f2f1f244"},
    "2.1": {"tasks": 89, "status": "frozen", "package": "terminal-bench/terminal-bench-2-1", "name": "main", "dataset_commit": None},
    "2.0": {"tasks": 89, "status": "frozen", "package": "terminal-bench/terminal-bench-2", "name": "2-0", "dataset_commit": None},
    "1.0": {"tasks": 80, "status": "frozen", "dataset": "terminal-bench-core==0.1.1", "dataset_commit": "91e10457b5410f16c44364da1a34cb6de8c488a5"},
}
EFFORT_ORDER = {"none": 0, "minimal": 1, "low": 2, "medium": 3, "high": 4, "xhigh": 5, "max": 6, "ultra": 7}
FRONTIER_KEYS = {"subscription": "subscription_per_attempt", "api": "api_per_attempt", "token": "token_per_attempt"}
OWNER_API = "https://ofhuhcpkvzjlejydnvyd.supabase.co/functions/v1/leaderboard-read"
OWNER_REVISION = "130be8458294043b33bbde1c765f3180f5ba96fb"


def owner_url(version: str) -> str:
    if version == "1.0":
        return f"https://github.com/harbor-framework/terminal-bench-website/blob/{OWNER_REVISION}/app/%28home%29/leaderboard/data.ts"
    return f"https://www.tbench.ai/?version={version}"


def number(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    result = float(value)
    if not math.isfinite(result) or result < 0:
        raise ValueError(f"Invalid nonnegative measurement: {value!r}")
    return result


def label(value: Any) -> str:
    if isinstance(value, dict):
        return str(value.get("label", ""))
    if isinstance(value, list):
        return " + ".join(str(part) for part in value)
    return str(value or "")


def url(value: Any) -> str | None:
    return value.get("url") if isinstance(value, dict) else None


def component_semantics(metrics: dict) -> str:
    fields = [number(metrics.get(key)) for key in ("total_tokens", "uncached_input_tokens", "cached_input_tokens", "output_tokens")]
    if any(value is None for value in fields):
        return "components_missing"
    total, named_input, cached, output = fields
    if math.isclose(total, named_input + cached + output, abs_tol=1, rel_tol=0):
        return "disjoint_components_match"
    if math.isclose(total, named_input + output, abs_tol=1, rel_tol=0):
        return "named_uncached_field_includes_cache_arithmetically"
    return "components_do_not_reconcile"


def normalized_rows(raw: dict, version: str) -> list[dict]:
    results = []
    seen = set()
    for source in raw["rows"]:
        if source.get("status", "display") != "display":
            continue
        result_id = str(source["id"])
        if result_id in seen:
            raise ValueError(f"Duplicate submission: {result_id}")
        seen.add(result_id)
        metadata, metrics = source["metadata"], source["metrics"]
        model = label(metadata.get("model_display", metadata.get("model_names")))
        agent = label(metadata.get("agent_display", metadata.get("agent_name")))
        developer = label(metadata.get("model_org"))
        if developer.lower() == "z.ai":
            developer = "Z.ai"
        effort = str(metadata.get("reasoning_effort") or "not_reported")
        agent_version = metadata.get("agent_version")
        if agent_version in ("unknown", "", None):
            agent_version = None
        score = number(metrics.get("accuracy"))
        if score is None or score > 100:
            raise ValueError(f"Accuracy is not 0–100 percent: {result_id}")
        half_width = number(metrics.get("accuracy_ci95_half_width"))
        if half_width is None and metrics.get("accuracy_stderr") is not None:
            half_width = 1.96 * number(metrics["accuracy_stderr"])
        metrics_trials = number(metrics.get("n_trials"))
        associated_trials = number(source.get("n_trials"))
        trials = metrics_trials if metrics_trials is not None else associated_trials
        if trials is not None and not trials.is_integer():
            raise ValueError(f"Non-integer trial count: {result_id}")
        # Migrated legacy rows use 0 for absent trial associations, not zero runs.
        trials = int(trials) if trials else None
        successes = number(metrics.get("successes"))
        if successes is not None:
            if trials is None or successes > trials:
                raise ValueError(f"Success count without valid trials: {result_id}")
            if abs(successes / trials * 100 - score) > 0.011:
                raise ValueError(f"Successes do not reconcile with accuracy: {result_id}")
        total_tokens = number(metrics.get("total_tokens"))
        total_cost = number(metrics.get("total_cost_usd"))
        api_valid = not (version == "3.0" and "Grok 4.5" in model)
        cost_note = "owner_cost_reporting_caveat" if not api_valid else "published_run_cost_not_current_repricing"
        token_per_attempt = total_tokens / trials if total_tokens is not None and trials else None
        api_per_attempt = total_cost / trials if total_cost is not None and trials and api_valid else None
        # Prefer exact success counts; rounded leaderboard percent is a fallback.
        rate = successes / trials if successes is not None else score / 100
        series = f"{model} · {agent}" + (f" {agent_version}" if agent_version else "")
        results.append({
            "id": result_id, "benchmark_version": version,
            "model": series, "base_model": model, "developer": developer,
            "agent": agent, "agent_version": agent_version,
            "model_ids": metadata.get("model_names"), "model_url": url(metadata.get("model_display")),
            "agent_url": url(metadata.get("agent_display")), "effort": effort,
            "effort_order": EFFORT_ORDER.get(effort, -1), "score": score,
            "success_rate": rate, "ci95_half_width": half_width,
            "ci95_low": max(0, score - half_width) if half_width is not None else None,
            "ci95_high": min(100, score + half_width) if half_width is not None else None,
            "trials": trials, "successes": successes, "task_count": VERSIONS[version]["tasks"],
            "raw_metrics_n_trials": metrics_trials, "raw_associated_n_trials": associated_trials,
            "trial_count_note": "metrics_count_preferred_over_different_association_count" if metrics_trials is not None and associated_trials is not None and metrics_trials != associated_trials else "published_metrics_or_association_count",
            "total_tokens": total_tokens, "token_per_attempt": token_per_attempt,
            "total_tokens_million": token_per_attempt / 1e6 if token_per_attempt is not None else None,
            "tokens_per_success": token_per_attempt / rate if token_per_attempt is not None and rate > 0 else None,
            "total_api_usd": total_cost, "api_per_attempt": api_per_attempt,
            "api_per_success": api_per_attempt / rate if api_per_attempt is not None and rate > 0 else None,
            "cost_note": cost_note,
            "raw_named_uncached_input_tokens": number(metrics.get("uncached_input_tokens")),
            "raw_cached_input_tokens": number(metrics.get("cached_input_tokens")),
            "raw_output_tokens": number(metrics.get("output_tokens")),
            "component_semantics": component_semantics(metrics),
            "avg_trial_duration_sec": number(metrics.get("avg_trial_duration_sec")),
            "source_url": url(metadata.get("pr_url")) or owner_url(version),
            "submission_date": metadata.get("date"), "source_updated_at": source.get("updated_at"),
            "source_verified": metadata.get("verified"), "data_scope": "complete" if trials else "summary_only",
        })
    # Unknown agent versions must not be mistaken for demonstrated identical
    # builds. Same named-system effort curves are explicitly qualified in UI.
    return sorted(results, key=lambda row: (-row["score"], row["model"], row["effort_order"]))


def subscription(row: dict, policy: dict) -> dict:
    result = {"subscription_per_attempt": None, "subscription_per_success": None,
              "subscription_offpeak_per_attempt": None, "access_kind": "excluded",
              "access_label": None, "access_evidence_date": None, "access_confidence": "unavailable",
              "access_rule": None, "access_sources": [], "api_value_ratio": None}
    cost = row["api_per_attempt"]
    if cost is None:
        result["access_rule"] = "missing_or_unreliable_benchmark_cost"
        return result
    agent, provider, model = row["agent"], row["developer"], row["base_model"]
    rule = None
    if agent in ("Codex", "Codex CLI") and provider == "OpenAI":
        rule = policy["codex"]
    elif agent == "Claude Code" and provider == "Anthropic":
        rule = policy["fable"] if "Fable" in model else policy["claude"]
    elif agent == "Claude Code" and provider == "Z.ai":
        if model.replace(" ", "-") != "GLM-5.3":
            result["access_rule"] = "exact_checkpoint_no_longer_supported_by_current_plan"
            return result
        rule = policy["glm"]
        if row["component_semantics"] not in ("disjoint_components_match", "named_uncached_field_includes_cache_arithmetically"):
            result["access_rule"] = "plan_credit_formula_known_benchmark_components_missing"
            return result
        named, cached, output = (row[key] for key in ("raw_named_uncached_input_tokens", "raw_cached_input_tokens", "raw_output_tokens"))
        uncached = named - cached if row["component_semantics"].startswith("named_") else named
        if uncached < 0:
            raise ValueError(f"Negative residual uncached input: {row['id']}")
        weighted = rule["credits_per_10000_tokens"]
        credits = (uncached * weighted[0] + cached * weighted[1] + output * weighted[2]) / 10000
        cost = rule["monthly_usd"] * credits / (rule["weekly_credits"] * policy["weeks_per_month"] * row["trials"])
        result["subscription_offpeak_per_attempt"] = cost * 0.5
    elif agent == "Gemini CLI":
        result.update(access_rule="official_request_quota_but_benchmark_model_request_count_missing", access_sources=["https://geminicli.com/docs/resources/quota-and-pricing/"])
        return result
    elif agent in ("Grok Build", "Kimi CLI", "Kimi Code", "Kimi Code CLI", "Devin") or (agent == "Claude Code" and ("Kimi" in model or provider == "Moonshot AI")):
        result["access_rule"] = "applicable_plan_conversion_unavailable"
        return result
    elif agent == "Cursor CLI":
        if "Composer" in model or "Grok" in model:
            result["access_rule"] = "cursor_models_pool_not_api_pool_quota"
            return result
        rule = policy["cursor_api_pool"]
    if rule:
        if rule.get("api_value_ratio"):
            cost /= rule["api_value_ratio"]
        result.update(access_kind="subscription_estimate", access_label=rule["plan"],
                      access_rule=rule["id"], access_sources=rule["sources"],
                      access_evidence_date=rule["evidence_date"], access_confidence=rule["confidence"],
                      api_value_ratio=rule.get("api_value_ratio"))
    else:
        result.update(access_kind="api_no_applicable_plan", access_label="API",
                      access_rule="no_supported_subscription_for_evaluated_harness", access_confidence="published",
                      access_sources=[row["source_url"]])
    result["subscription_per_attempt"] = cost
    result["subscription_per_success"] = cost / row["success_rate"] if row["success_rate"] > 0 else None
    return result


def derive(rows: list[dict], policy: dict) -> tuple[list[dict], dict]:
    derived = [{**row, **subscription(row, policy)} for row in rows]
    if not derived:
        raise ValueError("No leaderboard observations")
    validation = {
        "rows": len(derived),
        "counts": {"token": sum(row["token_per_attempt"] is not None for row in derived),
                   "api": sum(row["api_per_attempt"] is not None for row in derived),
                   "subscription": sum(row["subscription_per_attempt"] is not None for row in derived)},
        "component_semantics": dict(Counter(row["component_semantics"] for row in derived)),
        "access_decisions": dict(Counter(row["access_rule"] for row in derived)),
        "missing_agent_version": sum(row["agent_version"] is None for row in derived),
        "missing_trials": sum(row["trials"] is None for row in derived),
        "trial_count_discrepancies": [row["id"] for row in derived if row["trial_count_note"].startswith("metrics_count_preferred")],
    }
    return derived, validation


def ranked(rows: list[dict], metric: str) -> list[dict]:
    key = {"subscription": "subscription_per_success", "api": "api_per_success", "token": "tokens_per_success"}[metric]
    candidates = [row for row in rows if row[key] is not None and row[key] >= 0]
    candidates.sort(key=lambda row: (row[key], -row["score"], row["model"]))
    if not candidates:
        return []
    best, worst = candidates[0][key], candidates[-1][key]
    return [{**row, "rank": index + 1, "relative_cost_percent": row[key] / worst * 100 if worst else 100,
             "relative_value_percent": best / row[key] * 100 if row[key] else 100} for index, row in enumerate(candidates)]


def frontier_rows(rows: list[dict], metric: str) -> list[dict]:
    """Exact weak-cost/strong-success frontier; preserve equal-coordinate ties."""
    key = FRONTIER_KEYS[metric]
    ordered = sorted((row for row in rows if isinstance(row.get(key), (int, float))
                      and not isinstance(row[key], bool) and math.isfinite(row[key]) and row[key] >= 0
                      and isinstance(row.get("score"), (int, float)) and math.isfinite(row["score"])
                      and row.get("data_scope") != "partial"),
                     key=lambda row: (row[key], -row["score"]))
    frontier = []
    best = -math.inf
    last_coordinate = None
    for row in ordered:
        coordinate = (row[key], row["score"])
        if row["score"] > best or coordinate == last_coordinate:
            frontier.append(row)
            best = row["score"]
            last_coordinate = coordinate
    return frontier
