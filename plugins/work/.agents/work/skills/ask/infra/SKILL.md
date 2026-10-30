---
name: ask-infra
description: Draft an infrastructure or access request when deployment, pipelines or environments are blocked by a capability we do not hold. Use for ask infra, ask DevOps, tell the infrastructure owner, let X know about access, or an embedded message requesting a grant. Load work:ask and clip with cli:clip.
kind: operation
domain: work
profile: core
applicability: work repositories
requires: employer context, available connectors
provenance: house
---

# Ask infrastructure

Load `work:ask` and follow its employer context, recipient lookup, short voice, verified clipboard and sending rules. Provider commands and infrastructure routing come from the employer context, not this skill.

## Establish the blocker

Distinguish an access or environment blocker from a defect we can fix. Establish Tommy's observed capability at the exact scope, including inherited and group roles and any eligibility he can self-activate. Establish that the proposed recipient can perform the requested action. Do not infer either capability merely from a job title, incomplete role list or someone having done it previously.

Use the available provider evidence and employer procedures to check both sides. If those checks are unavailable, state what is unverified and ask the owner to confirm or route the action; do not claim Tommy cannot do it or the recipient can. Identify a working comparable environment and the relevant difference where evidence is available.

## Draft four sentences maximum

Say what failed and where, identify the exact principal and scope, request the concrete grant or change, and state the verified capability blocker. A verified difference from a working environment can earn the single supporting reason when it helps action the request. Backtick machine identifiers. Use the existing permission shape where it meets the need; do not invent broader access.

Keep command walkthroughs, role dumps, pipeline mechanics and the full investigation out of the draft. Retain evidence for follow-up. Clip through `cli:clip` and acknowledge in one or two lines as `work:ask` requires.

## While waiting

Continue work the permission cannot change. Keep blocked deployments and approvals parked; do not repeatedly rerun a known failure without evidence the relevant state changed. Requirements forks use `work:ask-the-team`; findings on code use `work:draft-comment`.

```text
Evidence: the deployment identity lacks the registry pull role at the failing registry.
Draft: The deployment is blocked by image pulls from `registry-a`. Can you grant the deployment identity the registry pull role there?
Handover: verify the recipient and scope, then clip; sending needs an explicit instruction.
```
