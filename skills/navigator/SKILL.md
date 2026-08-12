---
name: navigator
description: Use when a Guochuang project needs a current-stage diagnosis, track/group choice, next-step roadmap, or a coordinated audit across proposal, deck, defense, innovation, business, and evidence materials.
---

# GPS Navigator

GPS is the front door to Guochuang Preparation Skills. It identifies where a project is, what is blocking it, and which specialist pass should happen next.

## Intake contract

Ask for the project folder or pasted brief, target year, intended track/group, contest stage, deadline, and the people who can verify facts. If any are missing, label them `unknown`; never infer a qualification from a project title.

## Route in this order

1. **Rule lock.** Load `references/rules-2026.md`. Check year, track, group, registration, leader status, age, team size, equity, prior awards, IP, and material deadline. Flag the main-notice/industry-track teacher wording conflict instead of silently choosing a side.
2. **MAP pass.** Build a claim–evidence ledger. Separate `verified`, `primary`, `secondary`, `user_asserted`, and `missing`. A number without a source, unit, test condition, date, and owner is not a verified result.
3. **GPA pass.** Run `python scripts/gps_score.py examples/demo-project.json` or call `assess_project()` on the normalized brief. Report score, evidence coverage, confidence, blocking gaps, and rule basis together.
4. **Specialist route.** Use `proposal` for project-book logic, `deck` for slide architecture, `defense` for questioning, `innovation` for novelty and validation, `business` for market/finance, and `evidence` for source audits.
5. **CAMP plan.** Convert the top three gaps into owner + artifact + due date. Use a three-day rescue plan only when the deadline is under 72 hours.

## Output contract

Return exactly these sections: `Snapshot`, `Eligibility gate`, `Current level`, `GOLD gap`, `MAP ledger summary`, `Next 3 actions`, `Open questions`. `Current level` is a conditional potential band—not a promised award. State “2025 official baseline; 2026 rules pending” whenever applicable.

## Hard stops

Do not generate a submission-ready claim when the source is missing. Do not fabricate market size, patents, customers, experiments, revenue, or team contributions. Do not turn a visual template from another contest into a 2026 hard rule.

## References

- `references/rules-2026.md` — versioned rules and source hierarchy.
- `references/material-schema.md` — normalized input and output fields.
