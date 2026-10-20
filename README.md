# Work

Employer-agnostic communication, review and work-item entry points for work repositories. Authored
skills live in `.agents/work`; Template generates the Claude and Codex payloads from that source.

`work:ask-person`, `work:ask-the-team` and `work:ask-infra` share `work:ask`: load the exact employer context identified at session start, read available recipient context, draft briefly, and verify the copy through `machine:clip`. The team route exhausts requirements evidence before asking; the infrastructure route establishes the relevant capabilities. Chat drafts are never sent without explicit current-message authorization.

`work:draft-comment`, `work:respond-comments` and `work:explaining-code` provide review and explanation workflows. Pasteable review drafts are plain prose. Explanations never annotate source code.

`work:item` is the shared employer-neutral work-item boundary. `work:bug`, `work:debt`,
`work:mistake`, `work:feature` and `work:task` record an already-known kind without starting work.
`work:address-item` and its typed address workflows reconcile a persisted item before entering its
shared engineering lifecycle. They load the exact employer context selected at session start. That context
supplies the explicit recording and addressing operations plus supported-kind mapping; Work never guesses
an employer, backend or kind mapping. `work-items:manage` supplies shared neutral schema and provider
mechanics while the employer retains its process, transport and delivery gates.

`work:confluence` writes Confluence pages as HTML with native pieces and Mermaid diagrams readable in dark mode, and verifies the stored and rendered result. It ships `render_mermaid.py`, which renders `.mmd` sources into the site's own Mermaid macro, copied from an existing page, with a fresh id each run.

The ask workflows were restored from recovered skill loads and feedback memories, then separated from employer-specific routing and provider procedures. Employer plugins supply that context; this repository contains no employer identities or private chat data.

Install only for work repositories through the employer plugin's repository-local installation procedure.
Enable `work-agents/work`, `work-items-agents/work-items`, `base-agents/base`,
`base-agents/engineering` and `base-agents/machine` together. Do not enable this plugin at user scope.
Its version 3 tier requires the reserved `employer` fact established by employer detection.

After authored changes, run `pwsh .agents/sync-generated.ps1`, `pwsh .agents/sync-generated.ps1 -Check`, and `template:check`. Run `python -B .agents/tests/test_packaging.py` for packaging isolation and dependency checks.
