# Technical documentation

`technical-docs` composes, edits, or reviews substantive work-oriented prose. Use `technical-writing` for concise
fragments. State the outcome naturally; no mode name is required.

The skill writes only from existing or supplied authoritative context. When composing or editing, it applies
meaning-preserving grammar, clarity, terminology, and concision fixes inline. When editing, additions of claims,
distinct information, or examples, removal of distinct information, major restructuring, changed emphasis, and
unresolved ambiguity are returned as editorial suggestions or questions. Composition turns supplied facts into prose
directly. When suggestions need your judgment, the main agent incorporates your decisions into the next revision.

The main agent selects sources, records decisions, maintains the authoritative draft, and renders the result. It may
work directly, reuse an editor, or start a new one according to the task and context cost. A review presented as
independent uses a fresh reviewer without prior assessments or expected findings; unavoidable priming is disclosed.
A reused editor's review carries its earlier context. For substantive prose, the
main agent runs `avoid-ai-writing` in detect-only mode even when it sees no obvious pattern. For short text, the pass
runs when requested or warranted by a concrete pattern. If unavailable, the main agent reports that it was not run
and continues the workflow.
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
minimal generic structure. It supports reports, design documents, API documentation, and other substantive work prose
without imposing artifact-specific templates.
