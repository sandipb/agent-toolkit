# Technical documentation

`technical-docs` composes, edits, or reviews work-oriented prose. State the outcome naturally; no mode name is required.

The skill writes only from existing or supplied authoritative context. It applies certain grammar, clarity,
terminology, and concision fixes inline while preserving distinct technical information. When editing, new claims or
distinct information, examples, removals, major restructuring, changed emphasis, and ambiguity are returned as
editorial suggestions or questions. Composition turns supplied facts into prose directly.
Accept or reject those items in the next reply. The main agent combines your decisions with the current draft for the
next revision.

The main agent selects sources, records decisions, maintains the authoritative draft, and renders the result. It may
work directly, reuse an editor, or start a new one according to the task and context cost. A review presented as
independent uses a fresh reviewer; a reused editor's review carries its earlier context. An optional `avoid-ai-writing`
reviewer may critique the current draft, but its absence never blocks the workflow.
Reviewers assess language against supplied material; they do not fact-check, inspect code, or test technical behavior.
When a request needs both kinds of review, the main agent handles technical verification separately and delegates only
the language review.
Review-only requests return findings without a rewritten draft. Further review focuses on changed passages only when a
concrete language concern remains.

Examples:

- `$technical-docs Compose a runbook from these approved investigation notes.`
- `Edit this README for clarity without removing requirements or examples.`
- `Review this incident report and return findings without rewriting it.`
- `Draft a PR description from this diff summary and test results.`
- `Tighten this procedure while preserving commands, stop conditions, and rollback steps.`

The skill follows user instructions, repository guidance, nearby examples, and the existing document before adding
minimal generic structure. It supports reports, design documents, API documentation, commit messages, warnings, and
other technical prose without imposing artifact-specific templates.
