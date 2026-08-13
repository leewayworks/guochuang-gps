# GPS material schema

Normalize a project before judging it. Keep facts, assertions, hypotheses and missing inputs separate.

```yaml
project:
  name: string
  year: 2025|2026
  track: string
  group: string
  category: string
  stage: idea|school|provincial|network-review|final-defense
  deadline: ISO-8601|null
team:
  members: integer|null
  leader_status: string
  leader_age_or_birth: string
  leader_is_legal_representative: boolean|null
  leader_equity: number|null
  team_equity: number|null
claims:
  - id: C-001
    text: string
    status: verified|supported|conditional|hypothesis|missing|contradicted
    limitation: string
evidence:
  - id: E-001
    type: experiment|ip|customer|financial|survey|team_contribution|policy|honour
    source: relative/path-or-url
    page_or_slide: string
    status: missing|user_asserted|located|inspected|verified|contradicted
    claim_ids: [C-001]
    rubric_dimensions: [project_innovation]
    evidence_role: problem|mechanism|result|independent_validation|persistence
    independence_group: string
    baseline: string
    condition: string
    date: ISO-8601|null
    owner: string
    maturity_stage: assertion|prototype|test|field|repeat
    ownership_scope: string
    customer_stage: none|contact|intent|pilot|contract|paid|repeat
    privacy_flag: public|redacted|confidential
gates:
  red_tour_participation: missing|verified|failed
rubric_anchors:
  dimension_id: 0|1|2|3|4
```

Anchor meanings are GPS readiness states:

- `0`: no relevant claim or evidence;
- `1`: assertion only;
- `2`: inspectable but partial evidence;
- `3`: verified evidence with a relevant result and limitations;
- `4`: closed loop with independent or field validation and student ownership.

Outputs carry `rubric_version`, `rubric_status`, `current_year_rubric_status`, `generated_at` and source identifiers or hashes when available. Keep `rubric_alignment_score`, GPS readiness and evidence coverage as separate objects.
