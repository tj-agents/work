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

Load `work:work-item`, then load `engineering:write-feature` and fix the kind to `feature`. Use the
selected Recording operation only when the employer context explicitly supports that kind. Preserve the
canonical identity, requested outcome, requirements, acceptance criteria and existing delivery owner.

Record only. An explicit request to implement an existing feature belongs to `work:address-feature`.
Missing facts, context or mapping leave the request pending; do not invent facts or use another backend.
