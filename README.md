# GPS（**G**uochuang **P**reparation **S**kills）

> **From idea to gold. Navigate your Guochuang journey.**

GPS is a public beta release of Skills for teams preparing the **中国国际大学生创新大赛** (China International College Students' Innovation Competition, or 国创赛). It connects project materials, evidence, review and practice in one workflow. The readiness score is a heuristic, not a promise of an award.

A good project can still lose its thread when the project book, PPT, test records and rehearsal notes live in different places. GPS gives the team one route through them: find the claim, check the proof, fix the weak link, and rehearse the answer.

![Guochuang GPS concept](assets/guochuang-gps-concept.png)

## What GPS does

A typical review follows four steps:

1. **Rule gate.** Check the year, track, group, eligibility, integrity requirements, and local deadlines.
2. **Evidence map.** Link important claims to a file, page or slide, date, metric, condition, owner, and source status.
3. **Material review.** Use the specialist Skill for the project book, deck, defense, innovation, business case, or evidence set.
4. **Readiness report.** Summarize the strongest claims, unresolved gaps, risks, and the next three actions.

The result is a working list for the team: what to verify, what to rewrite, what to test, and who owns the next step. In the language of the product: GPS points the route, MAP shows the missing proof, GPA shows the current readiness, and CAMP turns the gaps into practice.

The workflow uses four internal labels:

- **GPA** names the readiness diagnostic.
- **MAP** is the claim and evidence ledger.
- **CAMP** turns open gaps into practice tasks.
- **GOLD** records the work still needed before stronger award claims are defensible.

These are labels for the workflow. They are not contest categories or award predictions.

## The seven Skills

| Skill | Use it for |
| --- | --- |
| navigator | Choose the review route and identify the next task |
| evidence | Build the claim-to-evidence ledger and find contradictions |
| proposal | Audit the project book or business plan section by section |
| deck | Plan and review slide headlines, visuals, sources, and time cuts |
| defense | Prepare reviewer questions, answer cards, and rehearsal drills |
| innovation | Check novelty, baselines, test conditions, and validation |
| business | Review customers, pricing, commercialization, finance, and risk |

Start with navigator when the project is still being sorted out. Load the specialist Skill that matches the task, and add evidence when a claim needs checking.

## Where the method comes from

The method was developed from structured review of local historical materials:

- project books, technical descriptions, pitch decks, and defense materials from 国创赛;
- technical-invention materials from 挑战杯大挑;
- business plans and pitch decks from 挑战杯小挑;
- the 2026 Ministry notice, 教高函〔2026〕26号, and information published by the national competition service site.

The repository keeps reusable patterns. It does not copy a winning project's wording, numbers, screenshots, or private files. Historical materials are reference material only. They do not define the 2026 rubric or indicate a team's chance of winning.

## Quick start

Run the bundled synthetic example from the repository root:

```powershell
python scripts/gps_score.py examples/demo-project.json
```

The example shows the input fields and the checks performed by the script. Its evidence paths are placeholders, so the report deliberately flags the unsupported numeric claim. It is not a real entry and is not a sample score for any team.

The script returns:

- a conditional readiness band;
- the displayed score and the uncapped raw_score;
- evidence coverage and confidence;
- blocking gaps and compliance findings;
- the notice version and rubric status.

The score is a GPS heuristic. It is not an official evaluation score. The 2026 evaluation rules, page limits, and speaking time are not treated as fixed until the official sources publish them.

## Install

The Skills are ordinary directories. Copy the repository's skills/ directory into the Skills directory used by your Agent tool, then load the Skill you need.

Codex can also install the repository as a plugin:

```text
codex plugin marketplace add leewayworks/guochuang-gps
codex plugin install guochuang-gps@guochuang-gps
```

The repository includes a Claude-compatible plugin manifest. If your Agent does not support plugins, copy the skills/ directory directly.

## Use GPS on a project folder

The default entry point is one sentence:

```text
Use GPS to review G:\path\to\project
```

`navigator` will inventory the directory, identify the material types, read the available project facts, select the specialist Skills, and ask only for missing details that can change the rule check or next action. On hosts that support dynamic Skill loading, it will invoke the needed passes; otherwise it will list them for you. You can add a year, track, stage, or deadline when you know them, but you do not need to list every file type or Skill.

For tighter control, use this form:

```text
Use GPS to review G:\path\to\project
Competition: China International College Students' Innovation Competition
Year: 2026
Stage: provincial review
```

The review returns `Snapshot`, `Eligibility gate`, `Current level`, `GOLD gap`, `MAP ledger summary`, `Next 3 actions`, and `Open questions`. It uses only facts traceable to the supplied materials and does not upload project files to this repository.

## Repository map

```text
skills/          seven independently loadable Skills
scripts/         deterministic readiness and compliance check
examples/        synthetic input
assets/          concept image
.codex-plugin/   Codex plugin manifest
.claude-plugin/  Claude-compatible plugin manifest
```

## Boundaries


GPS is not the official registration system, a judge, or a guarantee of an award. It cannot confirm a qualification when the source material is missing. It cannot make the 2026 evaluation rubric official before the contest publishes it.

Keep original competition files, student identities, customer-confidential material, personal contact details, and unreleased IP outside the public repository. Use the Skills on a local copy or a properly redacted export.

## License

MIT