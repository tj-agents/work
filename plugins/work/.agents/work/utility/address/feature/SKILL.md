---
name: address-feature
description: Address an existing work feature through the selected employer work-item operation. Use when explicitly asked to implement an identified work feature.
kind: utility
domain: work
profile: core
applicability: work repositories
requires: employer context, engineering, work-items
provenance: house
---

# Address a work feature

Load `work:item`, then follow its **Address** procedure with expected kind `feature`. Pass the named
canonical identity to the selected Addressing operation. It verifies the persisted item and its mapping,
reconciles its existing delivery owner, then resumes an authorized plan through
`engineering:plan-execution` or enters `engineering:feature`.

Do not reclassify or recreate the item. Missing facts, context, mapping or backend access leave it pending
with no fallback.

```text
Input: a named persisted feature is explicitly selected for implementation.
Action: work:address-feature verifies it through the selected Addressing operation and enters the declared engineering lifecycle.
Result: missing context, mapping or access leaves the item pending.
```
