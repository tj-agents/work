---
name: ask
description: Draft a human chat message in a work repository — telling a named person something, asking the owning team to decide an undecided requirement or a behaviour found while building or testing, or asking infrastructure for access a blocker needs. Use for let X know, tell Kate, Message for Yan, ask the team, check with the owner, ask infra or DevOps, including a message embedded in another answer, and before building anything undecided.
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

Resolve a named human using the available chat connector and read relevant recent conversation context before choosing wording. Use the recipient's own terminology, and check enough context to know what they already know and avoid repeating settled questions. If multiple employers or people remain plausible, ask only for the recipient detail needed to disambiguate. Do not pick a person or employer by guesswork.

If the context skill or connector is unavailable, say so briefly and draft using the conversation and repository evidence already available. Never invent directory matches, successful lookups, messages read, roles or access checks. Missing connector access does not prevent a useful draft.

## Voice and handover

Get to the point: the question or update first, then only what the reader needs to act on it. No waffle, restating or sign-off. Write like a person: plain words, short paragraphs separated by blank lines, never one dense block. Include at most one supporting reason. When Tommy supplies wording, keep it and change only what is wrong.

Quote the exact line when the point turns on what something says. Link each page, PR or ticket inline where it is named, never one link for several or a vague `here`. Backtick only identifiers that exist; never invent one for an example.

Every human chat draft, including one produced during an investigation, review explanation or implementation answer, is formatted and handed over through `teams:message`, not an inline Message for X block. Do not append the analysis as a second deliverable. Acknowledge the verified clipboard copy in one or two lines.

## Sending

Draft and clip by default. Do not send through a chat connector, create a ticket, or post into a review as a side effect. Sending requires an explicit instruction to "send it" in the current user message with the target and content clear. "Let X know", "tell Kate", "Message for Yan", "sort that message out" and a general instruction to finish work authorize a draft, not a send. A previous send authorization does not carry forward.

## Undecided requirements and behaviour

Read the story and acceptance criteria, its parent and relevant siblings, available design frames, source code and repository conventions, design decisions, story discussions and git history. Render available designs when layout, copy, controls, states or flow are the question. An answer already recorded in these sources is not an ambiguity. Do not assert that an unavailable source was checked.

Naming, structure, layering, test shape and other routine engineering decisions are yours to make. Ask the owning team when two reasonable people could build different observable behaviour from the remaining requirements, including a behaviour found while testing or investigating. Route behaviour, copy and scope to their owner, visual decisions to the design owner, and a genuinely open technical direction to its owner. Asking Tommy to choose is not asking the owner, and Tommy agreeing in chat does not authorize building it.

When the work has a Confluence page, record the question there first as a proposal with options and trade-offs. Then lead the draft with the user-visible screen, field or action and the decision needed. Give two concrete options and a recommendation when both are genuinely open. Keep to one story per draft. If the specification never requests an addition, do not build it and invite a veto; ask whether it belongs in scope without defending a prior implementation. Never turn the ask into a report about branches or review state.

Draft before building the ambiguous part. Continue everything the answer cannot change and leave the undecided behaviour unbuilt. If it already exists, hold that part from delivery while the decision is outstanding. Do not select an option merely to avoid waiting, or add source comments as a substitute for getting the decision.

## Infrastructure and access blockers

Provider commands and infrastructure routing come from employer context. Distinguish an access or environment blocker from a defect we can fix. Establish Tommy's observed capability at the exact scope, including inherited and group roles and any eligibility he can self-activate, and that the proposed recipient can perform the requested action. Do not infer either capability from a job title, incomplete role list or someone having done it before. If those checks are unavailable, state what is unverified and ask the owner to confirm or route the action. Identify a working comparable environment and the relevant difference where evidence is available.

Draft four sentences at most: what failed and where, the exact principal and scope, the concrete grant or change, and the verified capability blocker. A verified difference from a working environment can be the supporting reason. Use the existing permission shape where it meets the need; do not invent broader access. Keep command walkthroughs, role dumps, pipeline mechanics and the investigation out of the draft and retain them for follow-up.

While waiting, continue work the permission cannot change. Keep blocked deployments and approvals parked; do not rerun a known failure without evidence the relevant state changed.

Review findings use `work:draft-comment`; replies on Tommy's PR use `work:respond-comments`.

```text
"tell Kate the PR is ready"                      -> person; drafted and clipped, not sent
"testing shows locked-out users keep grants"     -> undecided behaviour; proposal on the Confluence page, then
                                                    a draft to the owning team; the fix stays unbuilt
"Tommy: yeah that makes sense?"                  -> not the owner's decision; still ask the owning team
"let Corbin know the AKS pull is failing"        -> infrastructure blocker; capabilities checked, drafted, not sent
```
