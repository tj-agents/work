---
name: task
description: Record a known task through the selected employer work-item operation. Use when a work repository has verified task facts to capture; completing an existing item uses work:address-task.
kind: utility
domain: work
profile: core
applicability: work repositories
requires: employer context, engineering, work-items
provenance: house
---

# Record a work task

Load `work:item`, then load `work-items:write-task` and fix the kind to `task`. Use the selected
Recording operation only when the employer context explicitly supports that kind. Preserve the canonical
identity, scope, dependencies, completion condition and existing delivery owner.

Record only. An explicit request to complete an existing task belongs to `work:address-task`. Missing
facts, context or mapping leave the request pending; do not invent facts or use another backend.

```text
Input: migrate the billing export caller; the employer maps task to Task.
Action: work-items:write-task records the concrete work and completion condition through that operation.
Result: verify the native Task identity and preserve its existing owner.
```
