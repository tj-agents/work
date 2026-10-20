---
name: feature
description: Record a known feature through the selected employer work-item operation. Use when a work repository has verified requested behavior to capture; implementing an existing item uses work:address-feature.
kind: utility
domain: work
profile: core
applicability: work repositories
requires: employer context, engineering, work-items
provenance: house
---

# Record a work feature

Load `work:item`, then load `work-items:write-feature` and fix the kind to `feature`. Use the
selected Recording operation only when the employer context explicitly supports that kind. Preserve the
canonical identity, requested outcome, requirements, acceptance criteria and existing delivery owner.

Record only. An explicit request to implement an existing feature belongs to `work:address-feature`.
Missing facts, context or mapping leave the request pending; do not invent facts or use another backend.

```text
Input: the employer requests CSV export and maps feature to Feature.
Action: work-items:write-feature captures the requested outcome and acceptance before employer persistence.
Result: verify the native Feature identity; implementation needs its own authorization.
```
