---
name: teams-message
description: Write a Teams or chat message Tommy will paste, with clickable link text instead of raw URLs and backticked identifiers, then hand it over verified through cli:clip. Use for any Teams message, status update, ready-for-review note or reply he will send, including every work:ask draft and a message embedded in another answer.
kind: utility
domain: work
profile: core
applicability: work repositories
requires: cli:clip
provenance: house
---

# Teams message

Owns a Teams message's markdown and its clipboard handover. `work:ask` owns recipient context, voice
and sending; load it too when the message is for a named person or team.

Phrase every link into the sentence as `[link text](https://...)`, never a raw URL. Backtick identifiers, types,
files, services, roles and flags. No headings, lists, bold, blockquotes, em dashes or a fence around the
message; fence only a command the reader will run. Keep it to a few sentences.

```text
Request: tell the team the two Orders pages are ready for review.
Draft:   I've been working on [these two pages](https://dev.azure.com/org/proj/_git/web/pullrequest/412), they're ready for review. The main change is the `OrderSummary` grid.
Clip:    Copied 164 chars, 1 code spans, 1 links, HTML + plain verified on the clipboard.
```

Write the exact message to a UTF-8 scratch file and copy it with `cli:clip` as the final action, so
nothing later replaces it. Reply in one or two lines naming the recipient or purpose and the verified
copy; do not print the draft inline. If the copy fails, say so, keep the file, and never claim it is
on the clipboard.
