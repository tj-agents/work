---
name: message
description: Use when Tommy will paste a Teams or chat draft to check its formatting, render links and code, and verify the clipboard copy.
kind: utility
domain: work
profile: core
applicability: all projects
requires: python
provenance: house
---

# Teams message

Owns turning a drafted Teams message into a verified clipboard copy. In work repositories `work:ask` owns
what the message says and how it is worded.

Write the exact message as markdown to a UTF-8 scratch file and run `teams_message.py` beside this file as
the final action, with `python3` on Linux/macOS or `python` on Windows. It rejects a draft line by line for
a raw URL, a URL or generic word (`here`, `these pages`) as link text, a heading, list, blockquote, bold, em
dash, or a fence around the whole message or left unclosed; fix every line and rerun. A passing draft is
copied as HTML with each `[text](https://...)` as its own link, backticks as inline code and fences as code
blocks, beside a plain flavour that holds no URL, because Teams turns pasted-over text into one link when
the plain text carries one. The copy is read back and compared before it reports success.

```text
python -B '<skill-directory>/scripts/teams_message.py' --path '<draft.md>'
Draft:  I've finished [AuthZ design](https://example.atlassian.net/wiki/spaces/ENG/pages/101) and [Worker rollout](https://example.atlassian.net/wiki/spaces/ENG/pages/102), both ready for review.
Output: Copied 69 chars, 0 code spans, 2 links, HTML + plain verified on the clipboard.
```

Reply in one or two lines naming the recipient or purpose and the verified copy; do not print the draft
inline. If the command fails, say so, keep the file, and never claim it is on the clipboard.
