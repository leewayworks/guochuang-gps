---
name: evidence
description: Use when collecting, classifying, cross-checking, and mapping sources for Guochuang project claims, including PDFs, PPTX, DOCX, spreadsheets, images, videos, patents, tests, contracts, and media.
---

# Evidence

Maintain a material map that lets a reviewer reproduce every important statement. A polished slide without a source is a lead, not proof.

## Evidence levels

- `L1` Education Ministry notice/annexes and the national contest site: hard rules.
- `L2` national service announcements and university official notices: implementation context.
- `L3` local policy briefs and public-account explainers: interpretation; retain URL/date and never override L1.
- `L4` historical winning materials: pattern and calibration only, never a current rule or guarantee.

## Ledger fields

`id, claim, source_path_or_url, page_or_slide, source_level, status, date, owner, metric_unit, condition, limitation, privacy_flag`.

Use `verified` only when the source is inspectable and the claim matches it. For image-only PDFs or PPTX, say `visual review required`; absence of text extraction is not absence of content.

## Output

Return a claim–evidence ledger, contradiction list, missing-proof queue, and a redaction list for confidential or personal information. Preserve original files outside the public repository.
