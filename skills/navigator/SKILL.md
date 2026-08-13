---
name: navigator
description: Use when a user asks for a GPS review of a Guochuang project folder or materials, needs a competition track or stage check, or wants a readiness diagnosis and next-step plan.
---

# GPS Navigator

Use navigator as the default entry point. When a user gives a project folder and asks for a GPS or Guochuang review, start the review without requiring a full intake form. Inspect the folder first, infer only what the materials support, and ask for the few missing facts that can change eligibility or routing.

## One-line entry

Accept a request such as:

`Use GPS to review G:\path\to\project`

Treat the supplied path as the project scope. If the user names a competition, year, track or stage, use it. Otherwise identify those fields from the materials. If the year is still unknown, ask after the first inventory and label any provisional use of the current rule card as `unconfirmed`.

## Automatic intake

Before asking questions:

1. Recursively inventory PDF, PPTX, DOCX, XLSX, image, video, text, source-code and archive files.
2. Read filenames, document text, metadata and obvious project headers to identify project name, year, track, group, stage and deadline.
3. Detect likely project-book, deck, defense, test, IP, customer, finance, team-contribution and survey materials.
4. Record what was inspected and what needs visual review. Do not treat an empty text extraction as an empty page.
5. Ask only for missing facts that affect the rule gate or the next action. Continue the material audit while those answers are pending. If the host cannot parse a format or load another Skill, record that limitation and continue with the available material.

Do not infer a qualification from a title, a filename, a past award or a visual style. Keep `source_verified`, `user_asserted`, `inferred_for_routing` and `unknown` distinct.

## Route

1. **Rule lock.** Load `references/rules-2026.md`. Check notice version, track, group, registration, leader requirements, age, team size, equity, prior national awards, IP ownership, integrity and local deadlines. Preserve conflicts between the main notice and an industry annex, then assign a confirmation owner.
2. **MAP pass.** Build the claim-to-evidence ledger. A quantitative claim is verified only when its source, page or slide, unit, test condition, date and owner are recorded.
3. **Specialist selection.** Load only the Skills suggested by the inventory. If the host supports dynamic Skill loading, invoke them directly; otherwise name the recommended passes in the report. Use: `proposal` for a project book, `deck` for slides, `defense` for a script or rehearsal, `innovation` for technical validation, `business` for customers and finance, and `evidence` for source and contradiction checks. Load `evidence` whenever claims or sources need checking.
4. **Readiness pass.** Normalize the findings and run `scripts/gps_score.py` when the input contains the required fields. Report `score`, `raw_score`, `readiness_band`, evidence coverage, confidence, blocking gaps, compliance findings, notice version and rubric status together. The script is a GPS heuristic, not an official rubric.
5. **CAMP plan.** Turn the three largest gaps into `owner + artifact + due date + acceptance check`. Use a short rescue plan only when the deadline is within 72 hours.

## Stage routing

| Stage | Main question | Minimum hand-off |
| --- | --- | --- |
| Discovery | Is the problem real and worth pursuing? | interview log, problem statement, rule unknowns |
| Build | Does the intervention work under a stated condition? | baseline, test record, student contribution map |
| School or provincial review | Can a reviewer verify the story quickly? | project-book ledger, slide table, question bank |
| National preparation | Which claims fail under interruption? | timed drill, screen evidence list, risk owners |

## Output contract

Return exactly these headings:

`Snapshot`, `Eligibility gate`, `Current level`, `GOLD gap`, `MAP ledger summary`, `Next 3 actions`, `Open questions`.

`Snapshot` must include the path, files inspected, project facts and unknowns. `Eligibility gate` must separate verified, user-asserted, unresolved and conflicting rules. `MAP ledger summary` must include counts or a compact table. `Next 3 actions` must be concrete tasks, not general advice.

`Current level` is a conditional readiness band. Never present it as a predicted award. Mention that the 2026 evaluation rules remain pending when that is the current source status. If the source set is too thin to assess, say `Not assessable` and explain what would change that status.

## Hard stops

Do not write a submission-ready number, customer, patent, experiment or team contribution when its source is missing. Do not turn a historical slide template or a 2025 score table into a 2026 requirement. Do not upload, copy or commit the user's project materials unless the user explicitly asks for that action.

References: `references/rules-2026.md` and `references/material-schema.md`.
