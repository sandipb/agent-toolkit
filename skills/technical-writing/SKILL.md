---
name: technical-writing
description: >-
  Compose, edit, or review the language of concise technical prose while preserving supported claims, terminology,
  certainty, conditions, causality, commands, identifiers, and values. Use for small writing tasks, not fact-checking,
  code review, or technical validation; use technical-docs or tech-blog for substantive writing workflows.
---

# Technical writing

Work only from authoritative context supplied for the writing task. Assess language and whether the draft preserves
that context; do not verify whether the context itself is true. A writer or reviewer using this skill must not perform
fact-checking, web searches, code review, or commands that test technical behavior, even if a handoff asks for them.
If a handoff asks for any of those checks, explicitly state which checks were not performed and that the main agent
must handle them. Do not let an empty language-review finding list imply technical validation. Return apparent factual
conflicts or missing support to the main agent. Produce a supportable partial result instead of inventing facts, causes,
requirements, risks, examples, or conclusions.

For editing or review, treat the supplied draft as the account to preserve unless the task supplies corrections or
designates another source as authoritative. This supports language work without certifying the draft's claims. Flag
unresolved conflicts rather than choosing which account is true.

Apply these invariants in order:

1. Preserve supported technical meaning and requirement strength.
2. Preserve terminology, certainty, conditions, exceptions, causality, commands, identifiers, paths, values, and units.
3. Follow explicit user instructions, then project guidance, nearby conventions, existing structure, and minimal
   generic organization.
4. Improve precision, concision, ambiguity, and information density.

Apply grammar, punctuation, meaning-preserving clarity improvements, terminology consistency, and removal of semantic
duplication inline when composing or editing. For review-only requests, return findings with locations, concrete reader
impact, and suggested direction; do not rewrite unless asked. When composing, turn supplied facts into prose without
treating that
wording as an unsupported addition. When editing, return additions of claims, distinct information, examples, or
analogies, major restructuring, changed emphasis, and ambiguous claims as author-judgment suggestions unless the user
or an artifact-specific skill authorizes them.

Before composing, editing, or reviewing, infer the intended reader's topic knowledge from the supplied context; general
technical experience does not imply familiarity with domain terminology. Follow the reader's likely reading order,
including headings, summaries, diagrams, captions, tables, and examples. Explain unfamiliar concepts where understanding
first depends on them, using concepts already established and only the detail needed for the passage. A heading may
introduce a term explained in its opening paragraph; acronym expansion alone may not explain the concept. Flag missing
support for an explanation and respect the editing and review boundaries above.

Within those constraints, organize explanations and procedures around reader prerequisites, technical dependencies,
causality, or chronology as appropriate. Keep independent reference material independently accessible: sections readers
can open directly need a brief local explanation or a precise link to the prerequisite. Return major restructuring as
an author-judgment suggestion unless an artifact-specific skill permits it.

Remove unnecessary throat-clearing, generic introductions or conclusions, unsupported significance claims, repetitive
generic transitions, synonym cycling, immediate paraphrastic repetition, and empty generic sections. Prefer deletion
over stylistic substitution when text adds neither distinct information nor useful emphasis, navigation, or local
context.

Retain repetition, parallel structure, and predictable organization when they improve scanning, comparison, procedural
consistency, or technical precision. Flag repeated sentence shapes, formulaic section endings, or structural uniformity
only when they impair readability or obscure relationships. Optimize for clear technical prose, not detector evasion
or artificial humanization.

Stop when the requested writing work is complete and no concrete language problem remains. Revisit only affected
passages when a change creates a new concern or the user asks for another review; do not repeat review to seek agreement
on stylistic preferences.

For substantive documentation, use `technical-docs`; concise fragments can use this skill directly. For reader-oriented
technical articles, use `tech-blog`. When either skill invokes this one as shared discipline, continue its workflow.
