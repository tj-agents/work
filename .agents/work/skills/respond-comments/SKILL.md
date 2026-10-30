---
name: respond-comments
description: Draft replies to reviewers on Tommy's own PR, acknowledging changes, answering questions, conceding, disagreeing or deferring. Use for respond to a review, answer a reviewer, reply to comments, or pasteable reviewer wording. Findings on others' code use work:draft-comment.
kind: operation
domain: work
profile: core
applicability: work repositories
requires: employer context, available connectors
provenance: house
---

# Respond to review comments

## Read the whole review

Read the review summary and every inline thread using the available review provider, including pagination. Check the stored body when a comment looks truncated. One comment may contain several requests or a direct question alongside a requested change; answer every point. Use the live code and diff to establish what changed before saying it is done.

## Keep the reply short

Default to under 15 words: done, removed, updated to constants, or the precise change. A concession gets one short clause and the change. A disagreement gets the concrete reason and position, with one option if useful; stop without a defensive tail. A deferral names the actual follow-up, never an invented ticket.

Extra length earns its place when code moved from the commented location, a direct question needs answering, an ask remains undone, or the comment is ambiguous. Say what remains outstanding plainly. Do not narrate why every accepted change was made; the diff shows it.

Draft in plain prose with backticked identifiers. No headings, lists, bold, blockquotes, em dashes or wrapping fences. Preserve supplied wording and register without manufacturing typos. Provide the draft and only the notes needed to explain an unresolved point. Say whether any review point remains unanswered.

## Posting

Draft by default; he posts. Explicit authorization must identify the final wording and destination before using a review connector. Never infer posting permission from a request to rewrite or finish the review. Do not resolve threads, approve, request changes or submit reviews as a side effect. Use the provider's threaded reply for an inline comment and its PR conversation for a review-summary reply only when authorized.

Findings on someone else's code use `work:draft-comment`. Human chat messages produced while answering a review load the matching `work:ask-person`, `work:ask-the-team` or `work:ask-infra` member and copy through `cli:clip`.

```text
Reviewer: Can this return early when the order is missing?
Verified change: the missing-order guard now returns before reading order.Total.
Draft: Added the early return for a missing order.
Posting: only with authorization for this wording and destination.
```
