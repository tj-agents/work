# Teams message rules

`teams_message.py` rejects every rule marked **checked**; the rest are the writer's.

| Rule | Why |
| --- | --- |
| One link per target, its text naming that target: `[AuthZ design](https://...) and [Worker rollout](https://...)`. **Checked:** raw URLs, a URL as link text, and generic or plural link text such as `here`, `this`, `these pages` or `both docs`. | Teams shows only the link text, so a shared or vague link hides which page is which, and a raw URL becomes a preview card. |
| Backtick only identifiers that exist: types, files, services, roles, flags. Never invent one for an example. | Code formatting tells the reader the name is real and searchable. |
| No headings, lists, bold, blockquotes or em dashes. **Checked.** | Teams chat renders them as clutter in a chat bubble. |
| Fence only a command the reader will run, never the whole message. **Checked**, including unclosed fences. | The copy renders a fence as a code block; a fenced message becomes one block. |
| A few sentences, leading with what the reader needs. | A chat message is read at a glance. |
