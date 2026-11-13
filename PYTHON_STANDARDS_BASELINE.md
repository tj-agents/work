# Python standards baseline

Existing violations at `bcfc1797f6e27c1c05bbcc9e51b34c663adab839` are baselined by exact authored file and rule. New files receive all enabled checks. Remove an exception when repairing its source. The tool configuration owns enforcement; this document records the rollout evidence and rationale.

## Ruff

Reason: preserve existing implementations during the standards rollout. Each row records the existing count and a representative required repair. No wildcard path or whole-rule ignores were added.

| File | Rule | Existing count | Required repair |
| --- | --- | ---: | --- |
| `.agents/teams/utility/message/scripts/teams_message.py` | `ANN401` | 9 | Dynamically typed expressions (typing.Any) are disallowed in `user32` |

## Custom checker

Reason: preserve exact pre-existing custom-checker findings during the standards rollout. Each entry maps to one authored path and rule; repair the stated design issue and remove its exception. No generated or vendored path is included.

| File | Rule | Existing count | Required repair |
| --- | --- | ---: | --- |
| .agents/teams/utility/message/scripts/teams_message.py | PY016 | 1 | Inject process state or confine the read to an entry-point main. |
| .agents/work/utility/draft-comment/scripts/post_pending_review.py | PY001 | 1 | Rewrite the nested comprehension as named loops or one generator. |

## Expanded authored-source scope

The previous source allowlist skipped authored implementations and tests. Broad directory scopes now cover future sibling files. The following additional findings are unchanged from the recorded base commit and use exact file/module and diagnostic exceptions.

| File | Ruff rule | Existing count | Required repair |
| --- | --- | ---: | --- |
| `.agents/tests/test_packaging.py` | `E501` | 2 | Line too long (124 > 120) |
| `.agents/tests/test_packaging.py` | `I001` | 1 | Import block is un-sorted or un-formatted |
| `.agents/tests/test_packaging.py` | `PT009` | 29 | Use a regular `assert` instead of unittest-style `assertEqual` |
| `.agents/tests/test_packaging.py` | `TID251` | 1 | `unittest.TestCase` is banned: Use plain pytest functions and bare assertions. |
| `.agents/tests/test_post_pending_review.py` | `I001` | 1 | Import block is un-sorted or un-formatted |
| `.agents/tests/test_post_pending_review.py` | `PT009` | 17 | Use a regular `assert` instead of unittest-style `assertEqual` |
| `.agents/tests/test_post_pending_review.py` | `TID251` | 2 | `importlib.util.spec_from_file_location` is banned: Import the installed public API; do not load another checkout by path. |
| `.agents/tests/test_render_mermaid.py` | `I001` | 1 | Import block is un-sorted or un-formatted |
| `.agents/tests/test_render_mermaid.py` | `PT009` | 17 | Use a regular `assert` instead of unittest-style `assertEqual` |
| `.agents/tests/test_render_mermaid.py` | `TID251` | 2 | `importlib.util.spec_from_file_location` is banned: Import the installed public API; do not load another checkout by path. |
| `.agents/tests/test_teams_clipboard.py` | `E501` | 1 | Line too long (133 > 120) |
| `.agents/tests/test_teams_clipboard.py` | `I001` | 1 | Import block is un-sorted or un-formatted |
| `.agents/tests/test_teams_clipboard.py` | `PLR6301` | 1 | Method `_read_clipboard` could be a function, class method, or static method |
| `.agents/tests/test_teams_clipboard.py` | `PT009` | 134 | Use a regular `assert` instead of unittest-style `assertEqual` |
| `.agents/tests/test_teams_clipboard.py` | `RUF059` | 1 | Unpacked variable `paste_kwargs` is never used |
| `.agents/tests/test_teams_clipboard.py` | `SIM117` | 1 | Use a single `with` statement with multiple contexts instead of nested `with` statements |
| `.agents/tests/test_teams_clipboard.py` | `TID251` | 20 | `importlib.util.spec_from_file_location` is banned: Import the installed public API; do not load another checkout by path. |
| `.agents/tests/test_teams_clipboard.py` | `UP012` | 2 | Unnecessary UTF-8 `encoding` argument to `encode` |
| `.agents/tests/test_teams_message.py` | `E501` | 2 | Line too long (139 > 120) |
| `.agents/tests/test_teams_message.py` | `I001` | 1 | Import block is un-sorted or un-formatted |
| `.agents/tests/test_teams_message.py` | `PT009` | 16 | Use a regular `assert` instead of unittest-style `assertEqual` |
| `.agents/tests/test_teams_message.py` | `TID251` | 3 | `importlib.util.spec_from_file_location` is banned: Import the installed public API; do not load another checkout by path. |
| `.agents/work/utility/draft-comment/scripts/post_pending_review.py` | `I001` | 1 | Import block is un-sorted or un-formatted |

Additional exact legacy formatter paths:

- `.agents/tests/test_packaging.py`
- `.agents/tests/test_render_mermaid.py`
- `.agents/tests/test_teams_clipboard.py`
- `.agents/tests/test_teams_message.py`
- `.agents/work/utility/confluence/render_mermaid.py`

| File | Mypy module | Rule | Existing count | Required repair |
| --- | --- | --- | ---: | --- |
| `.agents/tests/test_packaging.py` | `test_packaging` | `no-untyped-call` | 8 | Call to untyped function "load" in typed context |
| `.agents/tests/test_packaging.py` | `test_packaging` | `no-untyped-def` | 7 | Function is missing a type annotation |
| `.agents/tests/test_packaging.py` | `test_packaging` | `union-attr` | 3 | Item "None" of "Match[str] \| None" has no attribute "group" |
| `.agents/tests/test_post_pending_review.py` | `test_post_pending_review` | `arg-type` | 1 | Argument 1 to "module_from_spec" has incompatible type "ModuleSpec \| None"; expected "ModuleSpec" |
| `.agents/tests/test_post_pending_review.py` | `test_post_pending_review` | `no-untyped-call` | 11 | Call to untyped function "load_script" in typed context |
| `.agents/tests/test_post_pending_review.py` | `test_post_pending_review` | `no-untyped-def` | 12 | Function is missing a return type annotation |
| `.agents/tests/test_post_pending_review.py` | `test_post_pending_review` | `union-attr` | 2 | Item "None" of "ModuleSpec \| None" has no attribute "loader" |
| `.agents/tests/test_render_mermaid.py` | `test_render_mermaid` | `arg-type` | 1 | Argument 1 to "module_from_spec" has incompatible type "ModuleSpec \| None"; expected "ModuleSpec" |
| `.agents/tests/test_render_mermaid.py` | `test_render_mermaid` | `no-untyped-call` | 39 | Call to untyped function "sample_element" in typed context |
| `.agents/tests/test_render_mermaid.py` | `test_render_mermaid` | `no-untyped-def` | 15 | Function is missing a type annotation |
| `.agents/tests/test_render_mermaid.py` | `test_render_mermaid` | `union-attr` | 2 | Item "None" of "ModuleSpec \| None" has no attribute "loader" |
| `.agents/tests/test_teams_clipboard.py` | `test_teams_clipboard` | `arg-type` | 1 | Argument 1 to "module_from_spec" has incompatible type "ModuleSpec \| None"; expected "ModuleSpec" |
| `.agents/tests/test_teams_clipboard.py` | `test_teams_clipboard` | `attr-defined` | 1 | "def run(argv: Any, **kwargs: Any) -> Any" has no attribute "calls" |
| `.agents/tests/test_teams_clipboard.py` | `test_teams_clipboard` | `no-untyped-call` | 110 | Call to untyped function "_assert_offsets_are_exact" in typed context |
| `.agents/tests/test_teams_clipboard.py` | `test_teams_clipboard` | `no-untyped-def` | 94 | Function is missing a return type annotation |
| `.agents/tests/test_teams_clipboard.py` | `test_teams_clipboard` | `union-attr` | 3 | Item "None" of "ModuleSpec \| None" has no attribute "name" |
| `.agents/tests/test_teams_message.py` | `test_teams_message` | `arg-type` | 1 | Argument 1 to "module_from_spec" has incompatible type "ModuleSpec \| None"; expected "ModuleSpec" |
| `.agents/tests/test_teams_message.py` | `test_teams_message` | `no-untyped-call` | 13 | Call to untyped function "messages" in typed context |
| `.agents/tests/test_teams_message.py` | `test_teams_message` | `no-untyped-def` | 17 | Function is missing a type annotation |
| `.agents/tests/test_teams_message.py` | `test_teams_message` | `union-attr` | 3 | Item "None" of "ModuleSpec \| None" has no attribute "name" |
| `.agents/work/utility/confluence/render_mermaid.py` | `render_mermaid` | `no-any-return` | 1 | Returning Any from function declared to return "dict[Any, Any]" |
| `.agents/work/utility/confluence/render_mermaid.py` | `render_mermaid` | `no-untyped-call` | 1 | Call to untyped function "BodiedMacros" in typed context |
| `.agents/work/utility/confluence/render_mermaid.py` | `render_mermaid` | `no-untyped-def` | 5 | Function is missing a return type annotation |
| `.agents/work/utility/confluence/render_mermaid.py` | `render_mermaid` | `type-arg` | 3 | Missing type arguments for generic type "dict" |
| `.agents/work/utility/draft-comment/scripts/post_pending_review.py` | `post_pending_review` | `no-untyped-call` | 7 | Call to untyped function "load_payload" in typed context |
| `.agents/work/utility/draft-comment/scripts/post_pending_review.py` | `post_pending_review` | `no-untyped-def` | 8 | Function is missing a type annotation |
