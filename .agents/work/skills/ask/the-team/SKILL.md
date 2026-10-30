---
name: ask-the-team
description: Draft a question to the team that owns a genuinely undecided requirement, behaviour, copy, scope or design. Use for ask the team, ask product, check with the owner, let the team know, or an embedded message for a decision maker. Load work:ask and clip with cli:clip before the ambiguous part is built.
kind: operation
domain: work
profile: core
applicability: work repositories
requires: employer context, available connectors
provenance: house
---

# Ask the team

Load `work:ask` and follow its employer context, recipient lookup, short voice, verified clipboard and sending rules. Employer context identifies the owning team and available story, design and chat tools.

## Exhaust available evidence first

Read the story and acceptance criteria, its parent and relevant siblings, available design frames, source code and repository conventions, design decisions, story discussions and git history. Render available designs when layout, copy, controls, states or flow are the question. An answer already recorded in these sources is not an ambiguity. Do not assert that an unavailable source was checked.

Naming, structure, layering, test shape and other routine engineering decisions are yours to make. The test for asking the owning team is whether two reasonable people could build different observable behaviour from the remaining requirements. Route behaviour, copy and scope to their owner; visual decisions to the design owner; a genuinely open technical direction to its owner. Asking Tommy to choose the requirement is not asking its owner.

## Draft the decision

Lead with the user-visible screen, field or action and the decision needed. Give two concrete options and a recommendation when both are genuinely open. Use at most one supporting reason. Keep to a few sentences and one story per draft. Backtick any machine identifiers.

If the specification never requests an addition, do not build it and invite a veto. Ask whether it belongs in scope without defending a prior implementation or inventing a recommendation. Never turn the ask into a report about branches or review state.

## Continue safe work

Draft before building the ambiguous part. Continue everything the answer cannot change and leave the undecided behaviour unbuilt. If it already exists, hold that part from delivery while the decision is outstanding. Do not select an option merely to avoid waiting, or add source comments as a substitute for getting the decision.

Keep the checked evidence and costs available for follow-up; the handover remains the one or two lines required by `work:ask` after `cli:clip` verifies the copy. Capability blockers use `work:ask-infra`. Review findings use `work:draft-comment`.

```text
Open requirement: should an empty results page show a create action?
Draft: Should the empty results page show Create, or only the empty-state message?
Handover: clip the question and continue work that cannot change with the answer.
```
