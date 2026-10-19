---
name: mistake
description: Record a known process or agent mistake through the selected employer work-item operation. Use when a work repository has verified incident facts to capture; reconciling an existing item uses work:address-mistake.
kind: utility
domain: work
profile: core
applicability: work repositories
requires: employer context, engineering, work-items
provenance: house
---

# Record a work mistake

Load `work:work-item`, then load `engineering:write-mistake` and fix the kind to `mistake`. Use the
selected Recording operation only when the employer context explicitly supports that kind. Preserve the
canonical identity, observation, evidence, cause status, prevention rule and existing correction owner.

Record only. An explicit request to reconcile an existing mistake belongs to `work:address-mistake`.
Missing facts, context or mapping leave the request pending; do not invent facts or use another backend.
