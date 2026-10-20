---
name: bug
description: Record a known bug through the selected employer work-item operation. Use when a work repository has verified defect facts to capture; fixing an existing item uses work:address-bug.
kind: utility
domain: work
profile: core
applicability: work repositories
requires: employer context, engineering, work-items
provenance: house
---

# Record a work bug

Load `work:item`, then load `work-items:write-bug` and fix the kind to `bug`. Use the selected
Recording operation only when the employer context explicitly supports that kind. Preserve the canonical
identity, factual evidence, unknown cause, impact and existing repair owner.

Record only. An explicit request to investigate or fix an existing bug belongs to `work:address-bug`.
Missing facts, context or mapping leave the request pending; do not invent facts or use another backend.

```text
Input: the selected employer context maps `bug` to a supported native type; the export request returns HTTP 500.
Action: work-items:write-bug gathers the observed defect facts; the selected employer operation persists them.
Result: read back the same native Bug identity; recording does not begin its repair.
```
