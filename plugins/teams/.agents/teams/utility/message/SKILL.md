---
name: message
description: Write a Teams or chat message Tommy will paste, check it with a deterministic script and copy it through cli:clip. Use for any Teams message, status update, ready-for-review note or reply he will send, in every repo, including every work:ask draft and a message embedded in another answer.
kind: utility
domain: work
profile: core
applicability: all projects
requires: python, cli:clip
provenance: house
---

# Teams message

Owns writing a Teams message and handing it over verified. In work repositories `work:ask` owns recipient
context, voice and sending.

1. Draft the message by the [Teams message rules](references/rules.md).
2. Write the exact message to a UTF-8 scratch file and run `teams_message.py` beside this file, with
   `python3` on Linux/macOS or `python` on Windows. Fix every reported line and rerun; never copy around it.
3. Copy the passing file with `cli:clip` as the final action.
4. Reply in one or two lines naming the recipient or purpose and the verified copy; do not print the draft
   inline. If either command fails, say so, keep the file, and never claim it is on the clipboard.

```text
Draft: I've finished [AuthZ design](https://example.atlassian.net/wiki/spaces/ENG/pages/101) and [Worker rollout](https://example.atlassian.net/wiki/spaces/ENG/pages/102), both ready for review.
python -B '<skill-directory>/scripts/teams_message.py' --path '<draft.md>'
  Teams message OK (187 chars).
python -B '<cli:clip skill-directory>/scripts/copy_draft.py' --path '<draft.md>'
  Copied 187 chars, 0 code spans, 2 links, HTML + plain verified on the clipboard.
```
