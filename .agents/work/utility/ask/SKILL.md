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

Get to the point: the question or update first, then only what the reader needs to act on it. No waffle, restating or sign-off. Write like a person: plain words, short paragraphs separated by blank lines, never one dense block. When Tommy supplies wording, keep it and change only what is wrong.

Quote the exact line when the point turns on what something says. Link each page, PR or ticket inline where it is named, never one link for several or a vague `here`. Backtick only identifiers that exist; never invent one for an example.

```text
Hey, can I get some clarity on the `user_link` order? On the call we said removing `user_link` should happen before the migration, but the [target architecture page](https://...) §7 says the opposite: drop `user_link` only after the backfill is done in every estate.

Which one are we going with, and if it's before, how do existing users keep their roles until the backfill runs?

I'm a bit confused as Kate said things like this should go post go-live, but to me it makes sense to do it beforehand.
```

Every human chat draft, including one produced during an investigation, review explanation or implementation answer, is formatted and handed over through `teams:message`. Do not append the analysis as a second deliverable.

## Sending

Draft and clip by default. Do not send through a chat connector, create a ticket, or post into a review as a side effect. Sending requires an explicit instruction to "send it" in the current user message with the target and content clear. "Let X know", "tell Kate", "Message for Yan", "sort that message out" and a general instruction to finish work authorize a draft, not a send. A previous send authorization does not carry forward.

## Routes

Use `work:ask-person` for a named person, `work:ask-the-team` for a genuine requirement fork, and `work:ask-infra` for a capability or infrastructure blocker. Review findings use `work:draft-comment`; replies on Tommy's PR use `work:respond-comments`.

```text
"let Corbin know the AKS pull is failing" -> work:ask-infra, drafted and clipped, not sent
"tell Kate the PR is ready" -> work:ask-person, drafted and clipped, not sent
```
