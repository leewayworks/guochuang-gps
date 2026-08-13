"""Small, deterministic readiness check for the GPS examples."""
from __future__ import annotations

from collections import Counter
from typing import Any

REQUIRED_EVIDENCE = {
    "experiment",
    "ip",
    "customer",
    "financial",
    "team_contribution",
    "survey",
}
VERIFIED_STATUSES = {"verified", "primary"}


def _verified_types(project: dict[str, Any]) -> set[str]:
    return {
        item.get("type")
        for item in project.get("evidence", [])
        if item.get("status") in VERIFIED_STATUSES and item.get("source")
    }


def _claim_parts(claim: Any) -> tuple[str, str]:
    """Support both the short example format and the normalized claim schema."""
    if isinstance(claim, dict):
        return str(claim.get("id", "")), str(claim.get("text", ""))
    return "", str(claim)


def _supports_claim(claim: Any, evidence: list[dict[str, Any]]) -> bool:
    claim_id, claim_text = _claim_parts(claim)
    for item in evidence:
        if item.get("status") not in VERIFIED_STATUSES or not item.get("source"):
            continue
        if claim_id and (
            claim_id in set(item.get("claim_ids") or [])
            or item.get("claim_id") == claim_id
        ):
            return True
        if claim_text and str(item.get("claim", "")) == claim_text:
            return True
    return False


def scan_compliance(project: dict[str, Any]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    evidence = project.get("evidence", [])
    for claim in project.get("claims", []):
        _, claim_text = _claim_parts(claim)
        if any(ch.isdigit() for ch in claim_text) and not _supports_claim(claim, evidence):
            findings.append(
                {
                    "code": "UNVERIFIED_CLAIM",
                    "severity": "high",
                    "message": f"Numeric claim has no traceable evidence: {claim_text}",
                }
            )

    if project.get("workflow", {}).get("external_vendor_writing"):
        findings.append(
            {
                "code": "OUTSOURCED_CORE_MATERIAL",
                "severity": "critical",
                "message": "Core material appears to be outsourced; confirm the 2026 integrity requirements.",
            }
        )

    members = project.get("team", {}).get("members", 0)
    if members not in range(3, 16):
        findings.append(
            {
                "code": "TEAM_SIZE",
                "severity": "high",
                "message": "Team size is outside the usual 3-15 range; check the selected track notice.",
            }
        )

    track = str(project.get("track", ""))
    if track in {"产业赛道", "industry"} and project.get("team", {}).get("teacher_member_rule_conflict"):
        findings.append(
            {
                "code": "TRACK_RULE_CONFLICT",
                "severity": "high",
                "message": "The main notice and industry annex differ on teacher membership; confirm with the local organizer.",
            }
        )
    return findings


def assess_project(project: dict[str, Any]) -> dict[str, Any]:
    evidence_types = _verified_types(project)
    coverage = len(evidence_types & REQUIRED_EVIDENCE) / len(REQUIRED_EVIDENCE)
    findings = scan_compliance(project)
    components = {
        "innovation": 30 if "experiment" in evidence_types else 12,
        "growth": 25 if {"survey", "team_contribution"} <= evidence_types else 8,
        "team": 20 if "team_contribution" in evidence_types else 6,
        "industry_value": 25 if {"customer", "financial"} <= evidence_types else 8,
    }
    raw_score = sum(components.values())
    critical = any(item["severity"] == "critical" for item in findings)
    high = any(item["severity"] == "high" for item in findings)

    # Keep the raw score visible, but cap the displayed score when a material
    # finding prevents a clean readiness label.
    score = min(raw_score, 39 if critical else 59 if high else raw_score)
    gaps = sorted(REQUIRED_EVIDENCE - evidence_types)
    if critical or coverage < 0.34:
        readiness_band, level = "not_assessable", "Not assessable"
    elif high or score < 60 or coverage < 0.67:
        readiness_band, level = "foundation_or_provincial", "Provincial / city foundation"
    elif score < 78:
        readiness_band, level = "provincial_conditions", "Strong provincial conditions"
    elif score < 90:
        readiness_band, level = "national_silver_conditions", "National silver conditions"
    else:
        readiness_band, level = "national_gold_conditions", "National gold conditions"

    quality_factor = 0.35 if critical else 0.55 if high else 0.85
    return {
        "level": level,
        "readiness_band": readiness_band,
        "score": score,
        "raw_score": raw_score,
        "confidence": round(min(0.95, coverage * quality_factor), 2),
        "evidence_coverage": round(coverage, 2),
        "components": components,
        "blocking_gaps": gaps,
        "compliance_findings": findings,
        "rule_basis": "GPS evidence-gated heuristic; informed by historical review patterns, not an official rubric",
        "notice_version": "教高函〔2026〕26号",
        "rubric_version": "2026 rubric pending official release",
    }


def summarize_sources(project: dict[str, Any]) -> dict[str, int]:
    return dict(Counter(item.get("status", "unknown") for item in project.get("evidence", [])))


if __name__ == "__main__":
    import json
    import pathlib
    import sys

    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/gps_score.py <project.json>")
    path = pathlib.Path(sys.argv[1])
    project = json.loads(path.read_text(encoding="utf-8"))
    print(json.dumps(assess_project(project), ensure_ascii=False, indent=2))
