---
name: evidence
description: Use when collecting, classifying, validating or cross-checking sources for Guochuang claims across documents, data, tests, IP, customer, finance and team records.
---

# Evidence

Apply the shared policies in `gps-common`. When saving a Markdown report, use the common project-name rule with topic `证据`.

Build a material map that lets another person find and inspect the support for every important claim. A polished slide and a path string are leads until their contents are checked.

## Own this work

Own source status, claim links, file existence, locators, evidence roles, independence, contradictions and redaction. Do not decide the project's positioning or improve a weak claim by rewriting it more confidently.

## Validate sources

Use this state sequence:

`missing -> user_asserted -> located -> inspected -> verified | contradicted`

For a local source, resolve a relative path against the project JSON file or declared project root. Give it no verified credit if the file does not exist. For a URL, record when and how it was inspected; a `verified` string does not prove that a page was opened.

A file that exists is `located`, not automatically `verified`. For image-only PDF or PPTX pages, record `visual_review_required` and the page or slide.

## Build the ledger

Use one row per claim and include:

`id`, `claim`, `source`, `page_or_slide`, `source_level`, `status`, `date`, `owner`, `metric_unit`, `baseline`, `condition`, `limitation`, `evidence_role`, `independence_group`, `ownership_scope`, `customer_stage`, `privacy_flag`.

Use evidence roles `problem`, `mechanism`, `result`, `independent_validation` and `persistence`. Two records from the same `independence_group` count as one corroborating source. A quantitative claim needs a claim ID plus a locator or test condition before it can reach high evidence quality.

## Cross-check

Compare numbers, units, dates, names, IP ownership, customer stage, team roles and project titles across the project book, deck, script and raw records. Return the contradiction instead of selecting the nicer value.

Keep `contact`, `intent`, `pilot`, `contract`, `paid` and `repeat` separate. Do not turn a logo, invitation or intention letter into a paid customer result. Do not use a patent or paper as proof of product performance, adoption or student ownership without the corresponding links.

## Deliver

Return the claim-to-evidence ledger, evidence-role coverage, independence groups, contradiction list, missing-proof queue, status changes and redaction list. Keep original competition files and confidential material outside the public repository.
