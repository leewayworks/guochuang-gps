# GPS material schema

Normalize a project before judging it. Keep facts, assertions, and missing inputs separate.

```yaml
project:
  name: string
  year: 2026
  track: string
  group: string
  category: string
  stage: idea|school|provincial|network-review|final-defense
  deadline: ISO-8601
team:
  members: integer
  leader_status: string
  leader_age_or_birth: string
  leader_is_legal_representative: boolean|null
  leader_equity: number|null
  team_equity: number|null
claims:
  - id: C-001
    text: string
    status: verified|user_asserted|missing|contradicted
evidence:
  - id: E-001
    type: experiment|ip|customer|financial|survey|team_contribution|policy|honour
    source: relative/path-or-url
    page_or_slide: string
    status: primary|verified|secondary|unverified|missing
    condition: string
    owner: string
```

Output artifacts should carry `notice_version`, `rubric_version`, `generated_at`, and `source_hashes`.
