"""Deterministic, evidence-gated diagnostics for Guochuang GPS.

The module applies GPS readiness anchors to an official rubric's top-level
weights. It does not reproduce an official judging score or predict awards.
"""
from __future__ import annotations

import copy
import json
from collections import Counter
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "skills" / "navigator" / "references" / "rubrics-2025.json"

VERIFIED_STATUSES = {"verified", "inspected"}
EVIDENCE_ROLES = {
    "problem",
    "mechanism",
    "result",
    "independent_validation",
    "persistence",
}

TRACK_ALIASES = {
    "高教主赛道": "higher_main",
    "高教": "higher_main",
    "highermain": "higher_main",
    "highereducationmain": "higher_main",
    "青年红色筑梦之旅": "red_tour",
    "红旅": "red_tour",
    "redtour": "red_tour",
    "产业赛道": "industry",
    "产业": "industry",
    "industry": "industry",
}
GROUP_ALIASES = {
    "\u672c\u79d1\u751f\u521b\u610f\u7ec4": "creative",
    "\u7814\u7a76\u751f\u521b\u610f\u7ec4": "creative",
    "\u672c\u79d1\u751f\u521b\u4e1a\u7ec4": "startup",
    "\u7814\u7a76\u751f\u521b\u4e1a\u7ec4": "startup",
    "创意组": "creative",
    "creative": "creative",
    "创业组": "startup",
    "创业": "startup",
    "startup": "startup",
    "venture": "startup",
    "公益组": "charity",
    "公益": "charity",
    "charity": "charity",
    "publicwelfare": "charity",
    "企业命题组": "enterprise_proposition",
    "企业命题": "enterprise_proposition",
    "enterpriseproposition": "enterprise_proposition",
    "成果转化组": "results_transfer",
    "成果转化": "results_transfer",
    "resultstransfer": "results_transfer",
}


def _token(value: Any) -> str:
    return (
        str(value or "")
        .strip()
        .lower()
        .replace(" ", "")
        .replace("_", "")
        .replace("-", "")
    )


def _normalize(value: Any, aliases: dict[str, str]) -> str | None:
    token = _token(value)
    normalized_aliases = {_token(key): target for key, target in aliases.items()}
    return normalized_aliases.get(token)



def _is_meaningful_text(value: Any) -> bool:
    """Return whether a locator or condition carries usable evidence detail."""
    if value is None:
        return False
    text = str(value).strip()
    placeholder_tokens = {
        "",
        "tbd",
        "todo",
        "unknown",
        "\u672a\u77e5",
        "missing",
        "\u5f85\u8865\u5145",
        "\u5f85\u5b9a",
        "\u672a\u63d0\u4f9b",
        "n/a",
        "na",
        "none",
        "null",
        "-",
        "—",
    }
    return text.lower() not in placeholder_tokens

def load_rubric_registry(path: str | Path | None = None) -> dict[str, Any]:
    """Load the versioned rubric registry."""
    registry_path = Path(path) if path else REGISTRY_PATH
    return json.loads(registry_path.read_text(encoding="utf-8"))


def resolve_rubric(
    year: int | str,
    track: str,
    group: str,
    *,
    registry: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Resolve one supported route and propagate its temporal status."""
    try:
        assessment_year = int(year)
    except (TypeError, ValueError):
        return None
    if assessment_year not in {2025, 2026}:
        return None

    normalized_track = _normalize(track, TRACK_ALIASES)
    normalized_group = _normalize(group, GROUP_ALIASES)
    if not normalized_track or not normalized_group:
        return None

    data = registry or load_rubric_registry()
    for candidate in data.get("rubrics", []):
        if (
            candidate.get("track") == normalized_track
            and candidate.get("group") == normalized_group
        ):
            resolved = copy.deepcopy(candidate)
            resolved["assessment_year"] = assessment_year
            resolved["rubric_version"] = data["rubric_version"]
            if assessment_year == 2025:
                resolved["rubric_status"] = "official_hard"
                resolved["current_year_rubric_status"] = "official_hard"
            else:
                resolved["rubric_status"] = "historical_baseline"
                resolved["current_year_rubric_status"] = "pending"
                resolved["current_year_source_ids"] = [
                    "cicic-2026-review-rules-status"
                ]
            return resolved
    return None


def _claim_parts(claim: Any) -> tuple[str, str]:
    if isinstance(claim, dict):
        return str(claim.get("id", "")), str(claim.get("text", ""))
    return "", str(claim)


def _is_url(source: str) -> bool:
    return urlparse(source).scheme.lower() in {"http", "https"}


def _evidence_base(
    project_file: str | Path | None,
    base_dir: str | Path | None,
) -> Path:
    if base_dir is not None:
        return Path(base_dir).resolve()
    if project_file is not None:
        path = Path(project_file).resolve()
        return path if path.is_dir() else path.parent
    return Path.cwd().resolve()


def inspect_evidence(
    project: dict[str, Any],
    *,
    project_file: str | Path | None = None,
    base_dir: str | Path | None = None,
) -> list[dict[str, Any]]:
    """Validate evidence metadata and local file paths."""
    base = _evidence_base(project_file, base_dir)
    claims = [_claim_parts(claim) for claim in project.get("claims", [])]
    claims_by_id = {claim_id: text for claim_id, text in claims if claim_id}
    all_claim_texts = {text for _, text in claims if text}
    project_has_numeric_claim = any(
        any(character.isdigit() for character in text) for _, text in claims
    )

    inspected: list[dict[str, Any]] = []
    for index, raw_item in enumerate(project.get("evidence", []), start=1):
        item = copy.deepcopy(raw_item)
        item.setdefault("id", f"E-{index:03d}")
        source = str(item.get("source", "")).strip()
        status = str(item.get("status", "missing")).strip().lower()
        source_kind = "url" if _is_url(source) else "local"

        if not source:
            source_exists: bool | None = False
            resolved_source = None
        elif source_kind == "url":
            source_exists = None
            resolved_source = source
        else:
            source_path = Path(source)
            resolved_path = source_path if source_path.is_absolute() else base / source_path
            resolved_source = str(resolved_path.resolve())
            source_exists = resolved_path.is_file()

        linked_ids = {str(value) for value in item.get("claim_ids", []) if value}
        if item.get("claim_id"):
            linked_ids.add(str(item["claim_id"]))
        linked_text = str(item.get("claim", "")).strip()
        linked_claim_texts = {
            claims_by_id[claim_id]
            for claim_id in linked_ids
            if claim_id in claims_by_id
        }
        if linked_text and linked_text in all_claim_texts:
            linked_claim_texts.add(linked_text)
        has_claim_link = bool(linked_ids & set(claims_by_id)) or bool(linked_claim_texts)
        supports_numeric_claim = any(
            any(character.isdigit() for character in text)
            for text in linked_claim_texts
        )
        if not has_claim_link and project_has_numeric_claim and item.get("type") in {
            "experiment",
            "customer",
            "financial",
        }:
            supports_numeric_claim = True

        has_locator_or_condition = (
            _is_meaningful_text(item.get("page_or_slide"))
            or _is_meaningful_text(item.get("condition"))
        )
        url_was_inspected = (
            source_kind != "url"
            or (
                _is_meaningful_text(item.get("inspected_at"))
                and _is_meaningful_text(item.get("inspection_method"))
                and has_locator_or_condition
            )
        )
        status_is_verified = status in VERIFIED_STATUSES
        source_is_available = bool(source) and (
            source_exists is True
            or (source_kind == "url" and status_is_verified and url_was_inspected)
        )

        if source_kind == "url" and not url_was_inspected:
            quality_cap = 0
            cap_reason = "url_not_inspected"
        elif not source_is_available or status in {"missing", "contradicted"}:
            quality_cap = 0
            cap_reason = "missing_or_unavailable_source"
        elif not status_is_verified:
            quality_cap = 1
            cap_reason = "source_not_inspected"
        elif supports_numeric_claim and (not has_claim_link or not has_locator_or_condition):
            quality_cap = 2
            cap_reason = "quantitative_evidence_needs_claim_link_and_locator_or_condition"
        elif (
            item.get("evidence_role") == "independent_validation"
            and _is_meaningful_text(item.get("independence_group"))
        ):
            quality_cap = 4
            cap_reason = None
        else:
            quality_cap = 3
            cap_reason = None

        if quality_cap >= 3:
            effective_status = "verified"
        elif status == "contradicted":
            effective_status = "contradicted"
        elif source_kind == "local" and source_exists is False:
            effective_status = "missing"
        else:
            effective_status = "unverified"

        item.update(
            {
                "declared_status": status,
                "effective_status": effective_status,
                "source_kind": source_kind,
                "source_exists": source_exists,
                "resolved_source": resolved_source,
                "has_claim_link": has_claim_link,
                "has_locator_or_condition": has_locator_or_condition,
                "quality_cap": quality_cap,
                "quality_cap_reason": cap_reason,
                "countable_as_verified": quality_cap >= 3,
            }
        )
        inspected.append(item)
    return inspected


def _supports_claim(claim: Any, evidence: list[dict[str, Any]]) -> bool:
    claim_id, claim_text = _claim_parts(claim)
    for item in evidence:
        if not item.get("countable_as_verified"):
            continue
        linked_ids = {str(value) for value in item.get("claim_ids", []) if value}
        if item.get("claim_id"):
            linked_ids.add(str(item["claim_id"]))
        if claim_id and claim_id in linked_ids:
            return True
        if claim_text and str(item.get("claim", "")) == claim_text:
            return True
    return False


def scan_compliance(
    project: dict[str, Any],
    evidence: list[dict[str, Any]] | None = None,
) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    inspected = evidence if evidence is not None else inspect_evidence(project)
    for claim in project.get("claims", []):
        _, claim_text = _claim_parts(claim)
        if any(character.isdigit() for character in claim_text) and not _supports_claim(
            claim, inspected
        ):
            findings.append(
                {
                    "code": "UNVERIFIED_QUANTITATIVE_CLAIM",
                    "severity": "high",
                    "message": f"Quantitative claim lacks traceable evidence: {claim_text}",
                }
            )

    if project.get("workflow", {}).get("external_vendor_writing"):
        findings.append(
            {
                "code": "OUTSOURCED_CORE_MATERIAL",
                "severity": "critical",
                "message": "Core material appears outsourced; verify the applicable integrity rule.",
            }
        )

    members = project.get("team", {}).get("members")
    if members is not None and members not in range(3, 16):
        findings.append(
            {
                "code": "TEAM_SIZE",
                "severity": "high",
                "message": "Team size is outside the usual 3-15 range; verify the selected track notice.",
            }
        )
    return findings


def _gate_statuses(project: dict[str, Any], rubric: dict[str, Any]) -> dict[str, str]:
    statuses: dict[str, str] = {}
    supplied = project.get("gates", {})
    passed_values = {True, "verified", "passed", "complete", "yes"}
    for gate in rubric.get("gates", []):
        gate_id = gate["id"] if isinstance(gate, dict) else str(gate)
        value = supplied.get(gate_id)
        if value in passed_values:
            statuses[gate_id] = "passed"
        elif value in {False, "failed", "no"}:
            statuses[gate_id] = "failed"
        else:
            statuses[gate_id] = "missing"
    return statuses


def _dimension_assessment(
    project: dict[str, Any],
    rubric: dict[str, Any],
    evidence: list[dict[str, Any]],
) -> dict[str, Any]:
    requested = project.get("rubric_anchors", {})
    dimension_results: list[dict[str, Any]] = []
    total = 0.0

    for dimension in rubric.get("dimensions", []):
        dimension_id = dimension["id"]
        try:
            requested_anchor = float(requested.get(dimension_id, 0))
        except (TypeError, ValueError):
            requested_anchor = 0.0
        requested_anchor = min(4.0, max(0.0, requested_anchor))
        relevant = [
            item
            for item in evidence
            if item.get("countable_as_verified")
            and dimension_id in set(item.get("rubric_dimensions", []))
        ]
        has_independent_or_field_validation = any(
            (
                item.get("evidence_role") == "independent_validation"
                and _is_meaningful_text(item.get("independence_group"))
            )
            or _token(item.get("maturity_stage"))
            in {"field", "fieldvalidation", "repeat", "repeated"}
            or _token(item.get("customer_stage"))
            in {"pilot", "contract", "paid", "repeat", "repeated"}
            for item in relevant
        )
        has_student_ownership = any(
            item.get("type") == "team_contribution"
            or _is_meaningful_text(item.get("ownership_scope"))
            for item in relevant
        )

        cap_reason = None
        applied_anchor = requested_anchor
        if requested_anchor and not relevant:
            applied_anchor = min(applied_anchor, 1.0)
            cap_reason = "no_verified_dimension_evidence"
        elif requested_anchor > 3 and not (
            has_independent_or_field_validation and has_student_ownership
        ):
            applied_anchor = min(applied_anchor, 3.0)
            if applied_anchor < requested_anchor:
                cap_reason = "anchor_four_requires_validation_and_student_ownership"

        readiness_points = dimension["max_points"] * applied_anchor / 4.0
        total += readiness_points
        dimension_results.append(
            {
                "id": dimension_id,
                "label": dimension["label"],
                "max_points": dimension["max_points"],
                "requested_anchor": requested_anchor,
                "applied_anchor": applied_anchor,
                "readiness_points": round(readiness_points, 2),
                "evidence_ids": [item["id"] for item in relevant],
                "cap_reason": cap_reason,
            }
        )

    return {
        "score": round(total, 2),
        "max_score": rubric["total_points"],
        "rubric_id": rubric["id"],
        "rubric_status": rubric["rubric_status"],
        "basis": "GPS evidence-readiness anchors applied to official top-level rubric weights",
        "anchor_scale": {"min": 0, "max": 4},
        "dimensions": dimension_results,
    }


def _evidence_integrity(evidence: list[dict[str, Any]]) -> dict[str, Any]:
    verified = [item for item in evidence if item.get("countable_as_verified")]
    roles = {
        item.get("evidence_role")
        for item in verified
        if item.get("evidence_role") in EVIDENCE_ROLES
    }
    independence_groups = {
        item.get("independence_group")
        for item in verified
        if _is_meaningful_text(item.get("independence_group"))
    }
    return {
        "total_items": len(evidence),
        "verified_items": len(verified),
        "missing_local_sources": sum(
            item.get("source_kind") == "local" and item.get("source_exists") is False
            for item in evidence
        ),
        "capped_items": sum(item.get("quality_cap", 0) in {1, 2} for item in evidence),
        "independent_groups": len(independence_groups),
        "roles_covered": sorted(roles),
        "required_roles": sorted(EVIDENCE_ROLES),
    }


def _readiness_band(
    integrity: dict[str, Any],
    coverage: float,
    alignment_score: float,
    findings: list[dict[str, str]],
) -> str:
    if integrity["verified_items"] == 0:
        return "not_assessable"
    if any(item["severity"] == "critical" for item in findings):
        return "not_assessable"
    if coverage < 0.4:
        return "foundation"
    if coverage < 0.7:
        return "evidence_building"
    if coverage < 1.0 or alignment_score < 75:
        return "review_ready"
    if any(item["severity"] == "high" for item in findings):
        return "review_ready"
    return "defense_ready"


def assess_project(
    project: dict[str, Any],
    *,
    project_file: str | Path | None = None,
    base_dir: str | Path | None = None,
) -> dict[str, Any]:
    """Assess one normalized project without making an award prediction."""
    year = project.get("year")
    rubric = resolve_rubric(year, project.get("track", ""), project.get("group", ""))
    if rubric is None:
        return {
            "assessment_year": year,
            "rubric": None,
            "rubric_alignment_score": None,
            "gps_readiness": {
                "band": "not_assessable",
                "confidence": 0.0,
                "reason": "track_group_or_year_not_resolved",
            },
            "evidence_coverage": 0.0,
            "evidence_integrity": {
                "total_items": len(project.get("evidence", [])),
                "verified_items": 0,
                "missing_local_sources": 0,
                "capped_items": 0,
                "independent_groups": 0,
                "roles_covered": [],
                "required_roles": sorted(EVIDENCE_ROLES),
            },
            "gates": {},
            "blocking_gaps": ["rubric_route"],
            "compliance_findings": [],
            "routing_questions": [
                "Confirm the competition year, track and group before scoring."
            ],
            "rule_basis": "No rubric selected; no score produced.",
        }

    inspected = inspect_evidence(project, project_file=project_file, base_dir=base_dir)
    integrity = _evidence_integrity(inspected)
    coverage = len(integrity["roles_covered"]) / len(EVIDENCE_ROLES)
    findings = scan_compliance(project, inspected)
    gates = _gate_statuses(project, rubric)
    failed_gates = [gate_id for gate_id, status in gates.items() if status != "passed"]

    if failed_gates:
        alignment = None
        band = "not_assessable"
        confidence = 0.0
    else:
        alignment = _dimension_assessment(project, rubric, inspected)
        band = _readiness_band(integrity, coverage, alignment["score"], findings)
        confidence = round(
            min(0.95, coverage * (0.5 + min(3, integrity["independent_groups"]) * 0.1)),
            2,
        )

    blocking_gaps = [
        f"evidence_role:{role}"
        for role in sorted(EVIDENCE_ROLES - set(integrity["roles_covered"]))
    ]
    blocking_gaps.extend(f"gate:{gate_id}" for gate_id in failed_gates)
    blocking_gaps.extend(
        item["code"]
        for item in findings
        if item["severity"] in {"critical", "high"}
    )

    return {
        "assessment_year": int(year),
        "rubric": {
            "id": rubric["id"],
            "track": rubric["track"],
            "group": rubric["group"],
            "rubric_version": rubric["rubric_version"],
            "rubric_status": rubric["rubric_status"],
            "current_year_rubric_status": rubric["current_year_rubric_status"],
            "source_ids": rubric.get("source_ids", []),
            "current_year_source_ids": rubric.get("current_year_source_ids", []),
        },
        "rubric_alignment_score": alignment,
        "gps_readiness": {
            "band": band,
            "confidence": confidence,
            "meaning": "process readiness, not an award prediction",
        },
        "evidence_coverage": round(coverage, 2),
        "evidence_integrity": integrity,
        "gates": gates,
        "blocking_gaps": sorted(set(blocking_gaps)),
        "compliance_findings": findings,
        "source_summary": {
            "declared_statuses": dict(
                Counter(str(item.get("declared_status", "unknown")) for item in inspected)
            ),
            "effective_statuses": dict(
                Counter(str(item.get("effective_status", "unknown")) for item in inspected)
            ),
        },
        "routing_questions": [],
        "rule_basis": (
            "Official 2025 top-level weights with GPS evidence-readiness anchors. "
            "For 2026 this is a historical baseline while the current rubric is pending."
        ),
    }


def summarize_sources(project: dict[str, Any]) -> dict[str, int]:
    return dict(
        Counter(str(item.get("status", "unknown")) for item in project.get("evidence", []))
    )


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/gps_score.py <project.json>")
    project_path = Path(sys.argv[1]).resolve()
    payload = json.loads(project_path.read_text(encoding="utf-8"))
    print(
        json.dumps(
            assess_project(payload, project_file=project_path),
            ensure_ascii=False,
            indent=2,
        )
    )
