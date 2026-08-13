# 2026 rule card and fallback policy

Last checked: 2026-08-13. Bind local execution details to their organizer, stage and publication date.

## Source hierarchy

`official_hard` > `official_dynamic` > `local_execution` > `interpretive` > `historical_baseline`.

- `official_hard`: Ministry notice, annexes and the national competition site.
- `official_dynamic`: current official announcements that may change by stage.
- `local_execution`: school or provincial notices for their own rounds.
- `interpretive`: policy briefs and explainers that cannot override official sources.
- `historical_baseline`: earlier rubrics, training material and historical cases.

Preserve a conflict instead of silently choosing the more convenient source. Record an owner and confirmation deadline when it affects eligibility.

## Confirmed 2026 boundary

Primary sources are the Education Ministry notice, 教高函〔2026〕26号, and the national service site:

- <https://www.moe.gov.cn/srcsite/A08/s5672/202607/t20260731_1445670.html>
- <https://cy.ncss.cn/>

The notice covers the event framework, tracks, registration and integrity requirements. Track-specific details include venture-group entity and equity conditions, mandatory red-tour participation, and industry-group rules. The main notice and industry annex differ on teacher membership; keep that item `conflicting` until the track system or organizer confirms it.

The 2026 evaluation rules are published separately. They were still pending at the last check recorded here. Do not fix page limits, presentation time, templates or scoring weights from historical material.

## 2025 fallback for 2026

When the 2026 rubric is unavailable, resolve the same track and group against `rubrics-2025.json` and propagate all three fields:

```yaml
rubric_version: 2025-05-20
rubric_status: historical_baseline
current_year_rubric_status: pending
```

Call the result `rubric_alignment_score`. It is a GPS evidence-readiness mapping over the 2025 top-level weights, not an official 2026 score.

The authoritative 2025 release is the 19-page rule set published on 2025-05-20. A conflicting 17-page attachment bearing a 2025 title uses the older structure. The registry marks it `superseded`; it must not override the official release.
