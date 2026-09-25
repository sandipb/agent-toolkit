# Technical blog

`tech-blog` composes, edits, or reviews reader-oriented technical articles. It shares technical precision rules with
`technical-docs` but allows stronger changes to structure, pacing, explanation, and information selection.

Use an existing rough draft or research already gathered by the main agent. The skill does not research independently.
It preserves support for technical claims. Reordering and restructuring may be applied when claims and emphasis remain
intact; proposed examples, analogies, material removals, changed emphasis, and missing context remain suggestions.

Examples:

- `$tech-blog Turn this rough draft into a tighter article while preserving its claims and emphasis.`
- `Write a technical article from these researched notes and flag unsupported gaps.`
- `Review this post for pacing and formulaic AI-writing patterns without rewriting it.`

The main agent selects sources, records decisions, maintains the authoritative draft, and renders the result. It may
work directly, reuse an editor, or start a new one according to the task and context cost. A review presented as
independent uses a fresh reviewer; a reused editor's review carries its earlier context. For substantive prose, the
main agent runs `avoid-ai-writing` in detect-only mode even when it sees no obvious pattern. For short text, the pass
runs when requested or warranted by a concrete pattern. If unavailable, the main agent reports that it was not run
and continues writing.
Reviewers assess language against supplied material; they do not fact-check, inspect code, or test technical behavior.
When a request needs both kinds of review, the main agent handles technical verification separately and delegates only
the language review.
Review-only requests return findings without a rewritten draft. Further review focuses on changed passages only when a
concrete language concern remains.
