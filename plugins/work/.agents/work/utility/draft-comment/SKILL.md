---
name: draft-comment
description: Draft findings on someone else's code, review comments or PR feedback Tommy will paste under his name. Use for a comment, feedback on a PR, reviewer wording, and every code-review finding. Own-PR replies use work:respond-comments.
kind: utility
domain: work
profile: core
applicability: work repositories
requires: employer context, available connectors
provenance: house
---

# Draft a review comment

## Verify the finding

Read the actual code, callers, data shape and repository conventions before asserting a defect. Enumerate the relevant search space for negative claims; a search hit alone is not evidence. Verify the proposed fix against the PR's purpose and observable behaviour. Separate confirmed facts from inference and do not invent measurements, corpus counts or source access.

## Write the point and one option

Plain prose, no headings, lists, blockquotes or wrapping fences in the draft. State the concrete problem and one option, then stop. Use a user-visible field, action or screen when it explains the defect more clearly than a class name. Backtick identifiers, types, files and flags. Add one fact and its consequence only if the finding otherwise cannot be understood. Do not append a defence, an invitation to ignore it or a tail explaining what the option buys.

A definite defect gets a statement. A genuine choice may get a question. Keep the normal short register and supplied wording; do not manufacture typos. Avoid em dashes, corporate polish and gratuitous compliments. Do not attach code blocks to a pasteable prose draft unless Tommy explicitly requests a code suggestion.

Group repeated instances of the same mistake in one comment. Anchor to the line that makes the point understandable and link the actual design evidence when needed; never invent a design URL. Review bodies are short: a verdict and one steer.

## Handover and posting

Provide each pasteable draft as plain prose. If Tommy needs evidence, put a short explanation separately after it, opening with the reviewed code verbatim in a fenced block under each clickable path and line (the base code for a removal), then the proposed replacement if there is one. Once a finding has been explained, a request for its wording gets the draft alone. Present the consequential findings first and say plainly if nothing blocks.

````text
Draft: `GetOrder` no longer returns 404 for an unknown id; it throws on `order.Total`. Restore the null guard.

Evidence, src/Orders/OrderService.cs:42 at the base (the PR removed it):
```csharp
if (order is null) return NotFound();
```
Proposed replacement: put the guard back before `order.Total` is read.
````

Draft by default; he posts. Posting requires explicit authorization for the exact final wording and destination. Post with `python -B "<skill-directory>/scripts/post_pending_review.py" <owner/repo> <pr> <payload.json>`; it only creates a new pending review and verifies GitHub kept it pending. If a pending review already exists, the script refuses; add or edit comments on it directly in the GitHub UI instead. Never submit a review, approve, request changes, or resolve a thread. Before changing an existing pending review, read the live bodies and preserve his edits; do not reconstruct them from stale drafts.

Replies on Tommy's own PR use `work:respond-comments`. Human chat drafts, including a message embedded in review analysis, load the matching `work:ask-person`, `work:ask-the-team` or `work:ask-infra` member and use `machine:clip`.
