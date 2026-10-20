---
name: address-debt
description: Address existing technical debt through the selected employer work-item operation. Use when explicitly asked to resolve identified work debt.
kind: utility
domain: work
profile: core
applicability: work repositories
requires: employer context, engineering, work-items
provenance: house
---

# Address work debt

Load `work:item`, then follow its **Address** procedure with expected kind `debt`. Pass the named
canonical identity to the selected Addressing operation. It verifies the persisted item and its mapping,
reconciles its existing repair owner, then enters `engineering:address-debt`.

Do not reclassify or recreate the item. Missing facts, context, mapping or backend access leave it pending
with no fallback.

```text
Input: a named persisted debt item is explicitly selected for resolution.
Action: work:address-debt verifies it through the selected Addressing operation and enters engineering:address-debt.
Result: missing context, mapping or access leaves the item pending.
```
