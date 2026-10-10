# Work

Employer-agnostic communication and review workflows for work repositories. Authored utility skills live in `.agents/work/utility`; kit generates the Claude and Codex payloads from that source.

`work:ask-person`, `work:ask-the-team` and `work:ask-infra` share `work:ask`: load the exact employer context identified at session start, read available recipient context, draft briefly, and verify the copy through `machine:clip`. The team route exhausts requirements evidence before asking; the infrastructure route establishes the relevant capabilities. Chat drafts are never sent without explicit current-message authorization.

`work:draft-comment`, `work:respond-comments` and `work:explaining-code` provide review and explanation workflows. Pasteable review drafts are plain prose. Explanations never annotate source code.

The ask workflows were restored from recovered skill loads and feedback memories, then separated from employer-specific routing and provider procedures. Employer plugins supply that context; this repository contains no employer identities or private chat data.

Install only for work repositories through the employer plugin's repository-local installation procedure. Enable `work-agents/work`, `base-agents/base` and `base-agents/machine` together. Do not enable this plugin at user scope. Its version 3 tier requires the reserved `employer` fact established by employer detection and its harness declares the clipboard dependency.

After authored changes, run `pwsh .agents/sync-generated.ps1`, `pwsh .agents/sync-generated.ps1 -Check`, and `kit:check`. Run `python -B .agents/tests/test_packaging.py` for packaging isolation and dependency checks.
