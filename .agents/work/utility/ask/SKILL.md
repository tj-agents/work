---
name: ask
description: Shared rules for drafting human chat messages in work repositories. Load before any work:ask-person, work:ask-the-team or work:ask-infra draft, including a message embedded in another answer such as let X know, tell Kate, or Message for Yan.
kind: utility
domain: work
profile: core
applicability: work repositories
requires: employer context, available connectors
provenance: house
---

# Ask

## Employer and recipient context

Before drafting, load the exact employer context skill identified by SessionStart employer detection. Use its qualified skill name and routing instructions; do not guess an employer from the request. Employer context supplies chat tool names, teams, roles, provider procedures and recipient routing. Prefer the available tools it names.

Resolve a named human using the available chat connector and read relevant recent conversation context before choosing wording. Check enough context to know what they already know and avoid repeating settled questions. If multiple employers or people remain plausible, ask only for the recipient detail needed to disambiguate. Do not pick a person or employer by guesswork.

If the context skill or connector is unavailable, say so briefly and draft using the conversation and repository evidence already available. Never invent directory matches, successful lookups, messages read, roles or access checks. Missing connector access does not prevent a useful draft.

## Voice and handover

Write a few plain sentences in Tommy's voice, with at most one supporting reason. Keep normal sentence case and his register; do not manufacture typos or polish supplied wording into corporate English. Backtick identifiers, types, files, services, roles and flags. No headings, lists, bold, blockquotes, em dashes or wrapping code fences in the draft.

Every human chat draft goes through `machine:clip`, including one produced during an investigation, review explanation or implementation answer. Write the exact draft to a UTF-8 scratch file, load `machine:clip`, and use its file-based copy procedure. Verify the copy succeeded through its read-back result before reporting success. Preserve identifier backticks. Copy as the final handover action so a later clipboard item does not replace the message.

Reply in one or two lines naming the recipient or purpose and confirming the verified copy. Do not print the draft inline or append the analysis as a second deliverable. If copying fails, report that failure plainly and keep the draft file available; never claim it is on the clipboard.

## Sending

Draft and clip by default. Do not send through a chat connector, create a ticket, or post into a review as a side effect. Sending requires an explicit instruction to "send it" in the current user message with the target and content clear. "Let X know", "tell Kate", "Message for Yan", "sort that message out" and a general instruction to finish work authorize a draft, not a send. A previous send authorization does not carry forward.

## Routes

Use `work:ask-person` for a named person, `work:ask-the-team` for a genuine requirement fork, and `work:ask-infra` for a capability or infrastructure blocker. Review findings use `work:draft-comment`; replies on Tommy's PR use `work:respond-comments`.
