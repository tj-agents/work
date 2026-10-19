---
name: address-mistake
description: Address an existing process or agent mistake through the selected employer work-item operation. Use when explicitly asked to reconcile an identified work mistake.
kind: workflow
domain: work
profile: core
applicability: work repositories
requires: employer context, engineering, work-items
provenance: house
---

# Address a work mistake

Load `work:work-item`, then follow its **Address** procedure with expected kind `mistake`. Pass the named
canonical identity to the selected Addressing operation. It verifies the persisted item and its mapping,
reconciles its existing correction owner, then enters `engineering:address-mistake`.

Do not reclassify or recreate the item. Missing facts, context, mapping or backend access leave it pending
with no fallback.
