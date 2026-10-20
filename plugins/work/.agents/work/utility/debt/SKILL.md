---
name: debt
description: Record known technical debt through the selected employer work-item operation. Use when a work repository has verified debt facts to capture; resolving an existing item uses work:address-debt.
kind: utility
domain: work
profile: core
applicability: work repositories
requires: employer context, engineering, work-items
provenance: house
---

# Record work debt

Load `work:item`, then load `work-items:write-debt` and fix the kind to `debt`. Use the selected
Recording operation only when the employer context explicitly supports that kind. Preserve the canonical
identity, factual evidence, deliberate deferral, resolution condition and existing repair owner.

Record only. An explicit request to resolve existing debt belongs to `work:address-debt`. Missing facts,
context or mapping leave the request pending; do not invent facts or use another backend.

```text
Input: the owning team deliberately defers export paging and its context maps debt to Technical Debt Item.
Action: work-items:write-debt records the compromise and observable exit condition through that operation.
Result: preserve the native debt identity and the decision; no alternate tracker is selected.
```
