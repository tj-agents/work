---
name: address-bug
description: Address an existing work bug through the selected employer work-item operation. Use when explicitly asked to investigate or fix an identified work bug.
kind: workflow
domain: work
profile: core
applicability: work repositories
requires: employer context, engineering, work-items
provenance: house
---

# Address a work bug

Load `work:work-item`, then follow its **Address** procedure with expected kind `bug`. Pass the named
canonical identity to the selected Addressing operation. It verifies the persisted item and its mapping,
reconciles its existing repair owner, then enters `engineering:address-bug`.

Do not reclassify or recreate the item. Missing facts, context, mapping or backend access leave it pending
with no fallback.
