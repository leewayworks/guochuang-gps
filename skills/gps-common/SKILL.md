---
name: gps-common
description: Use when routing, sourcing, or wording a GPS diagnosis that involves track alignment, evidence status, historical comparisons, or readiness conclusions.
---

# GPS Common Governance

This is a shared governance layer, not a user-facing review Skill. It keeps routing, source authority, and claim language consistent across GPS passes.

## Owns

- Review mode selection and pass boundaries.
- Source hierarchy, 2025 fallback provenance, and source conflicts.
- Status vocabulary and non-predictive readiness language.
- Saved report names and collision handling.

## Does not own

- Project intake or final synthesis (`navigator`).
- Essence, advantages, selling points, opportunity, or case-pattern transfer (`positioning`).
- Claim inspection (`evidence`), technical validation (`innovation`), business judgment (`business`), or deterministic scoring.

## Apply

1. Read `references/routing.yaml` to select `full_diagnosis`, `quick_triage`, or `narrow_specialist`; respect the owner boundary and required passes.
2. Read `references/source-registry.yaml` before treating a rule, rubric, or historical material as authoritative.
3. Read `references/output-language.md` before stating any conclusion, score interpretation, or readiness result.
4. When a Markdown report is saved, apply the naming rules below. Preserve a filename and destination explicitly requested by the user.

## Saved Markdown reports

Return results in the conversation unless the user asks for a file. When saving without an explicit filename, use these defaults:

| Review type | Default filename |
| --- | --- |
| Full diagnosis | `<project-name>-GPS评审.md` |
| Quick triage | `<project-name>-GPS初评.md` |
| Narrow specialist | `<project-name>-<topic>评审.md` |

Use the project name stated by the user or supported by inspected materials. If it is unavailable, use the sanitized project-directory name; if that is also unavailable, use `项目`. Keep Unicode names. Replace Windows-reserved filename characters (`< > : " / \ | ? *`) and control characters with `-`, collapse repeated separators, and remove trailing spaces or periods.

Do not overwrite an existing report unless the user asks. Append `-02`, `-03` and so on. Suggested specialist topics are `定位`, `创新`, `市场`, `证据`, `项目书`, `PPT` and `答辩`.

Keep source level, rubric status, and claim status separate. A 2025 rubric may be an official source for 2025 and only a `historical_baseline` for a 2026 diagnosis.
