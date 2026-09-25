# Technical writing

`technical-writing` provides shared precision, concision, terminology, source-boundary, and prose-hygiene rules. Use it
directly for small artifacts such as technical notes, issue text, comments, and explanations. Use `technical-docs` for
substantive work-oriented documentation or `tech-blog` for reader-oriented articles.

Examples:

- `$technical-writing Tighten this deployment note without changing its requirements.`
- `Rewrite this issue summary using only the supplied findings.`

The skill uses supplied context to improve language and preserve meaning. It does not verify facts, inspect code, or
research missing information. If asked to do so, it reports which checks it did not perform and identifies the main
agent as responsible for those checks. Follow-up review focuses on passages changed in ways that create a concrete
language concern.

For editing and review, the supplied draft establishes the account to preserve unless the task supplies corrections or
designates another authoritative source. Unresolved conflicts are flagged without certifying the draft's claims.
