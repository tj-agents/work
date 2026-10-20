---
name: address-item
description: Address an existing work item through the selected employer operation after reading its persisted kind. Use when explicitly asked to implement or fix a work item whose kind is not yet known; recording alone uses work:item or a work kind entry.
kind: utility
domain: work
profile: core
applicability: work repositories
requires: employer context, engineering, work-items
provenance: house
---

# Address a work item

Load `work:item` and follow its **Address** procedure without an expected kind. Pass the named
canonical identity to the selected Addressing operation. It reads the persisted kind through the selected
employer backend, validates its supported-kind mapping, reconciles the existing owner and enters the
matching shared engineering lifecycle.

Do not infer the kind from a title, reclassify, recreate or substitute an item. A missing, closed,
unsupported or already-owned item remains with its selected employer operation; do not fall back to a
personal or local backend.

```text
Input: a named persisted item is explicitly selected, but its kind is unknown.
Action: work:address-item reads its persisted kind through the selected Addressing operation and enters the matching engineering lifecycle.
Result: an unsupported or unavailable item remains pending with that operation.
```
