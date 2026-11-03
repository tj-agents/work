---
name: message
description: Write a Teams or chat message Tommy will paste, with clickable link text instead of raw URLs and backticked identifiers, check it with a deterministic script and copy it through cli:clip. Use for any Teams message, status update, ready-for-review note or reply he will send, in every repo, including every work:ask draft and a message embedded in another answer.
kind: utility
domain: work
profile: core
applicability: all projects
requires: python, cli:clip
provenance: house
---

# Teams message

Owns a Teams message's markdown and its clipboard handover. In work repositories `work:ask` owns
recipient context, voice and sending.

Phrase every link into the sentence as `[link text](https://...)`, never a raw URL. Backtick identifiers,
types, files, services, roles and flags. No headings, lists, bold, blockquotes, em dashes or a fence around
the message; fence only a command the reader will run. Keep it to a few sentences.

Write the exact message to a UTF-8 scratch file. Run `teams_message.py` beside this file, with `python3`
on Linux/macOS or `python` on Windows. It reports every rule a draft breaks by line and exits non-zero;
fix each line and rerun, never copy around it. When it passes, copy the same file with `cli:clip` as
the final action:

```text
python -B '<skill-directory>/scripts/teams_message.py' --path '<draft.md>'
  Teams message OK (164 chars).
python -B '<cli:clip skill-directory>/scripts/copy_draft.py' --path '<draft.md>'
  Copied 164 chars, 1 code spans, 1 links, HTML + plain verified on the clipboard.
Draft: I've been working on [these two pages](https://dev.azure.com/org/proj/_git/web/pullrequest/412), they're ready for review. The main change is the `OrderSummary` grid.
```

Reply in one or two lines naming the recipient or purpose and the verified copy; do not print the
draft inline. If either command fails, say so, keep the file, and never claim it is on the clipboard.
