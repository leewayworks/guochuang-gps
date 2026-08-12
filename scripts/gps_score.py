"""Deterministic evidence-gated triage for Guochuang GPS."""
from __future__ import annotations

from collections import Counter
from typing import Any

REQUIRED_EVIDENCE = {"experiment", "ip", "customer", "financial", "team_contribution", "survey"}


def _verified_types(project: dict[str, Any]) -> set[str]:
    return {item.get("type") for item in project.get("evidence", [])
            if item.get("status") in {"verified", "primary"} and item.get("source")}


def scan_compliance(project: dict[str, Any]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for claim in project.get("claims", []):
        if any(ch.isdigit() for ch in str(claim)):
            matched = any(item.get("status") in {"verified", "primary"} and item.get("claim")
                          and str(item["claim"]) in str(claim) for item in project.get("evidence", []))
            if not matched:
                findings.append({"code": "UNVERIFIED_CLAIM", "severity": "high",
                                 "message": f"数字主张缺少可追溯证据：{claim}"})
    if project.get("workflow", {}).get("external_vendor_writing"):
        findings.append({"code": "OUTSOURCED_CORE_MATERIAL", "severity": "critical",
                         "message": "核心材料存在外部代写/代做风险，触及 2026 学生/教师‘十不准’。"})
    if project.get("team", {}).get("members", 0) not in range(3, 16):
        findings.append({"code": "TEAM_SIZE", "severity": "high",
                         "message": "团队人数必须为 3–15 人；请以所选赛道最新规则复核。"})
    if project.get("track") == "产业赛道" and project.get("team", {}).get("teacher_member_rule_conflict"):
        findings.append({"code": "TRACK_RULE_CONFLICT", "severity": "high",
                         "message": "主通知与产业附件对教师/师生组队存在表述张力，须向赛区确认。"})
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
    score = sum(components.values())
    gaps = sorted(REQUIRED_EVIDENCE - evidence_types)
    critical = any(item["severity"] == "critical" for item in findings)
    if critical:
        level = "不可判定"
    elif coverage < 0.34 or score < 40:
        level = "市级/省级基础"
    elif score < 60 or coverage < 0.67:
        level = "省级/国铜潜力"
    elif score < 78:
        level = "国银潜力"
    else:
        level = "国金潜力"
    return {"level": level, "score": score, "confidence": round(min(.95, coverage * (.55 if findings else .85)), 2),
            "evidence_coverage": round(coverage, 2), "components": components,
            "blocking_gaps": gaps, "compliance_findings": findings,
            "rule_basis": "2025 官方评审基线；2026 评审规则待官网发布后替换"}


def summarize_sources(project: dict[str, Any]) -> dict[str, int]:
    return dict(Counter(item.get("status", "unknown") for item in project.get("evidence", [])))


if __name__ == "__main__":
    import json
    import pathlib
    import sys
    if len(sys.argv) != 2:
        raise SystemExit("用法：python scripts/gps_score.py <project.json>")
    path = pathlib.Path(sys.argv[1])
    print(json.dumps(assess_project(json.loads(path.read_text(encoding="utf-8"))), ensure_ascii=False, indent=2))
