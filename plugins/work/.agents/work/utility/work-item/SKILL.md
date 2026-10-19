---
name: work-item
description: Record, read and coordinate work items through the exact employer operation selected for this work repository. Use when handling a work item, backlog record or tracker item in an employer repository; known kinds use work:bug, work:debt, work:mistake, work:feature or work:task.
kind: utility
domain: work
profile: core
applicability: work repositories
requires: employer context, engineering, work-items
provenance: house
---

# Work items

Load the exact employer context identified by SessionStart employer detection before doing any work-item
operation. It must provide a **Work-item operations** section with exactly one qualified **Recording
operation**, one qualified **Addressing operation**, and a **Supported-kind mapping** for `bug`, `debt`,
`mistake`, `feature` and `task`. The mapping states the employer-native representation and lifecycle for
each supported kind, or explicitly marks it unsupported.

Do not infer an employer from the repository path, choose an unqualified operation, derive an operation
name from an employer name, or substitute another provider. Missing, ambiguous or unavailable context
blocks the request. An unsupported kind remains pending with the employer context as its resolver; never
reclassify it or use a personal or local backend.

Use `work-items:manage` for the shared record shape, factual validation, identity and provider mechanics.
The selected Recording operation owns its employer tracker, native type mapping, creation, readback and
process rules. The selected Addressing operation owns persisted-item lookup, ownership reconciliation,
progress updates and employer commit, push and delivery gates.

## Record

For a known kind, load the matching Engineering recording convention, preserve its facts and use the
selected Recording operation with the explicit mapping. Reconcile an existing canonical item, goal,
session, branch or repair owner before recording. Recording is only backlog work: it does not start
implementation, create a branch, commit, push or publish.

An untyped report loads `engineering:write-issue` to classify once, then follows this procedure with the
resulting supported kind. If the classification or mapping cannot be established, retain the evidence and
report the resolver instead of creating a substitute item.

## Address

For an explicit implementation or repair request, use the selected Addressing operation. Give it the
named canonical identity and expected kind when a typed address workflow supplied one. It must read the
persisted item, verify its mapping and state, reconcile its existing goal, session, branch, PR and writer,
then enter the lifecycle for that persisted kind. Never infer a kind from an item title, recreate an item
or independently select a different record.

Closed, removed, blocked and already-owned items retain their history. Keep factual progress and verified
closure evidence in the selected employer backend. Employer process and delivery gates continue to apply.
