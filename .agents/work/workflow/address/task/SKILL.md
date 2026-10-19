---
name: address-task
description: Address an existing work task through the selected employer work-item operation. Use when explicitly asked to complete an identified work task.
kind: workflow
domain: work
profile: core
applicability: work repositories
requires: employer context, engineering, work-items
provenance: house
---

# Address a work task

Load `work:work-item`, then follow its **Address** procedure with expected kind `task`. Pass the named
canonical identity to the selected Addressing operation. It verifies the persisted item and its mapping,
reconciles its existing delivery owner, then follows the task's declared workflow. Use
`engineering:feature` for an authorized scoped new or changed behavior.

Do not reclassify or recreate the item. Missing facts, context, mapping or backend access leave it pending
with no fallback.
