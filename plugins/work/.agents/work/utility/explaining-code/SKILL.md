---
name: explaining-code
description: Explain existing code, a mechanism, PR, subsystem or confusing line. Use for how does X work, explain this, walk me through, manual review, or an answer becoming a wall of prose about code. Pasteable findings use work:draft-comment.
kind: utility
domain: work
profile: core
applicability: work repositories
requires: employer context, available connectors
provenance: house
---

# Explain existing code

## Read before explaining

Read the actual definitions, call sites and data shapes. A search locates candidates; it does not prove absence. Enumerate the search space before making a negative claim. Read the repository's conventions and use its vocabulary. Employer or repository context supplies any system-specific constraints; verify them against the current source rather than assuming they apply everywhere.

## Show state and mechanism

Lead with what is stored where: the record, fields or relevant persisted JSON. Then show the code that reads and writes it. Copy snippets from the actual files and trim irrelevant lines without rewriting the remaining code. Inline snippets or fenced excerpts in the explanation are allowed. Cite clickable file paths and lines.

Use a compact table for a sequence of writes, state machine, lifecycle or precedence chain when it makes the state changes easier to follow. Explain the specific mechanism that produces the behaviour. For a change, compare the actual before and after and identify the relevant behavioural difference. Avoid defending choices nobody asked about or inventing history.

A confusing line usually needs a paragraph and one snippet; a subsystem deserves enough detail to understand its mechanism. When Tommy is testing by hand, end with the few cases that distinguish correct behaviour and the resulting stored state. Skip a test tour for a simple understanding question.

## Explain without annotating

Keep the explanation in the answer. Do not add, improve or reword code comments while explaining. A wrong source comment can be reported as a finding without editing it as a side effect. The default for source comments remains zero.

If code changes are requested, make the authorized changes. Pasteable findings use `work:draft-comment`; own-PR replies use `work:respond-comments`. A human message inside this answer still loads the matching `work:ask-person`, `work:ask-the-team` or `work:ask-infra` member, follows `work:ask`, and uses `machine:clip` instead of printing a draft inline.
