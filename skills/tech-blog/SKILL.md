---
name: tech-blog
description: >-
  Compose, edit, or review the language of reader-oriented technical articles from supplied authoritative context. Use
  for articles needing stronger restructuring, pacing, explanation, or information selection than work-oriented
  documentation permits; not technical validation.
---

# Technical blog

Use `technical-writing` as the shared discipline. Infer composition, editing, or review from the request. Work from an
existing draft or authoritative context already present or explicitly supplied. Do not research or invent missing
facts, causes, evidence, motivations, examples, analogies, risks, or conclusions.

Preserve support for technical claims, terminology, certainty, conditions, causality, commands, identifiers, and
values. Optimize for understanding and sustained reading. Unlike the shared default, you may reorder and restructure
the draft when supported claims and emphasis remain intact. Return unsupported claims, examples, analogies, removal of
material claims, changed emphasis, and unresolved gaps as author-judgment suggestions. Produce a supportable partial
draft when context is incomplete. Omit empty suggestion sections.

## Coordinate editorial work

The main thread owns source selection, user and objective decisions, the authoritative draft, and user-facing rendering.
It may write or review directly, reuse an existing editor, or start a new subagent. Choose based on task size, useful
continuity, context cost, and the need for independent judgment. If a request also calls for technical verification,
the main thread handles that separately and sends only the language task to the editor. Never ask a writing reviewer to
search, inspect code, or validate technical claims. When delegating, provide the current draft and authoritative
context required by the source and editorial contracts. State the language-only scope and keep unrelated context out
of a new subagent's packet.

Use a fresh reviewer when presenting a review as independent. A reused editor retains earlier context, so describe its
review accordingly.

For substantive prose—more than a few sentences, such as a multi-paragraph article—run `avoid-ai-writing` in
detect-only mode on the current draft before returning composition or edits, and as part of review-only work. Run it
even when the main thread sees no obvious pattern. Use a sibling reviewer when available; otherwise run the pass in
the main thread. For
short text, run it when requested or when a concrete language pattern warrants it. Ask for structured critique, not
rewriting. Require each finding to identify a concrete problem with clarity, coherence, or readability.
Vocabulary, sentence length, punctuation, and conversational tone are not independent acceptance criteria. Preserve
supported author voice and purposeful narrative pacing. Deduplicate findings. Fix specific filler, formulaic phrasing,
ornamental wording that adds no information or purposeful emphasis, awkward rhythm, or unclear passages when the change
preserves technical meaning and voice. Reject mechanical-only flags and changes that conflict with the shared
invariants. Send remaining findings to an editor for reconciliation
or handle them in the main thread. If the skill is unavailable, report that the pass was not run and continue the core
workflow. Repeat the pass only after material revisions introduce new prose.

For composition or editing, return the draft and only material suggestions or missing-context questions. The main
thread adopts delegated results as appropriate and renders them for the user.
