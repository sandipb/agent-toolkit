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

Use the optional `avoid-ai-writing` pass only when requested or when a concrete unresolved language pattern warrants
it. Send only the current edited draft to a sibling reviewer for structured critique, not rewriting. Require each
finding to identify a concrete problem with clarity, coherence, or readability.
Vocabulary, sentence length, punctuation, and conversational tone are not independent acceptance criteria. Preserve
supported author voice and purposeful narrative pacing. Deduplicate findings. Reject findings that conflict with the
shared invariants or lack a concrete reader benefit. Send substantive remaining findings to an editor for
reconciliation or handle them in the main thread. Its absence never blocks the core workflow.

For composition or editing, return the draft and only material suggestions or missing-context questions. The main
thread adopts delegated results as appropriate and renders them for the user.
