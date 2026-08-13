---
name: evidence
description: Use when collecting, classifying, cross-checking, and mapping sources for Guochuang project claims, including PDFs, PPTX, DOCX, spreadsheets, images, videos, patents, tests, contracts, and media.
---

# Evidence

Maintain a material map that lets a reviewer reproduce every important statement. A polished slide without a source is a lead, not proof.

## Source levels

- L1: Education Ministry notices, annexes and the national contest site. These set hard rules.
- L2: national service announcements and university official notices. These provide implementation context.
- L3: local policy briefs and public-account explainers. Keep URL and date; they interpret but do not override L1.
- L4: historical winning materials. Use them for patterns and calibration, never as a current rule or guarantee.

## Ledger

Use one row per claim and keep these fields:

id, claim, source_path_or_url, page_or_slide, source_level, status, date, owner, metric_unit, condition, limitation, privacy_flag.

A source status moves through missing -> user_asserted -> located -> inspected -> verified or contradicted. Use primary for an inspectable first-party record and secondary for an interpretation. Do not call a claim verified because a file merely exists.

For image-only PDF or PPTX pages, set status to visual review required and record the page or slide. Lack of extracted text is not evidence that the content is absent.

## Cross-checks

Compare numbers, units, dates, team roles, IP names, customer names and project titles across the project book, deck, script and ledger. Return contradictions rather than choosing the nicer value. Record a privacy flag for student identity, customer confidentiality, personal contact information, unreleased IP or any document that should stay outside a public repository.

## Deliverables

Return the claim-to-evidence ledger, contradiction list, missing-proof queue, source-status changes and a redaction list. Keep original competition files and confidential project material outside the public repository.
