---
name: technical-docs
description: >-
  Compose, edit, or review the language of work-oriented technical documentation from supplied authoritative context
  while preserving technical meaning and distinct information. Use for READMEs, runbooks, procedures, reports, design
  documents, API documentation, PR descriptions, commit messages, warnings, and code comments; not technical validation.
---

# Technical documentation

Use `technical-writing` as the shared discipline. Infer whether to compose, edit, or review from the request. Existing
prose is optional; every resulting claim must map to authoritative context already present or explicitly supplied.
Return a supportable partial draft plus author-judgment questions when information is missing. The main thread may
assemble sources separately; editorial work stays within the supplied context.

## Preserve documentation

Preserve every distinct fact, relationship, condition, exception, reason, consequence, warning, risk, sequence, scope
limit, cross-reference, command, identifier, value, unit, technical term, requirement level, and certainty. Remove only
semantic duplication that carries no distinct information.

Use the project's structure. With no convention, add only enough organization for task completion and lookup. Prefer
explicit conditions, one operation per step, and consistent terms. Flag long sentences only when they obscure meaning.

Apply safe language corrections inline. When editing, return new claims or distinct information, examples, removal of
distinct information, major restructuring, changed emphasis, and unresolved ambiguity as author-judgment suggestions.
Use native comments or suggestions when practical; otherwise separate suggestions from revised prose. Omit empty
suggestion sections.

## Coordinate editorial work

The main thread owns source selection, user and objective decisions, the authoritative draft, and user-facing rendering.
It may write or review directly, reuse an existing editor, or start a new subagent. Choose based on task size, useful
continuity, context cost, and the need for independent judgment. If a request also calls for technical verification,
the main thread handles that separately and sends only the language task to the editor. Never ask a writing reviewer to
search, inspect code, or validate technical claims. When delegating, provide the current authoritative draft, accepted
decisions, relevant sources, and applicable invariants. State the language-only scope and keep unrelated context out of
a new subagent's packet.

Use a fresh reviewer when presenting a review as independent. A reused editor retains earlier context, so describe its
review accordingly.

Use the optional `avoid-ai-writing` pass only when requested or when a concrete unresolved language pattern warrants
it. Send only the current edited draft to a sibling reviewer. Ask it to critique, not rewrite, and return location,
pattern, severity, `safe-fix` or `author-judgment`, rationale, and suggested direction.
Require each finding to identify a concrete problem with clarity, coherence, or readability. Vocabulary, sentence
length, punctuation, and conversational tone are not independent acceptance criteria. Deduplicate findings. Reject
findings that conflict with the shared invariants or lack a concrete reader benefit. Send substantive remaining
findings to an editor for reconciliation or handle them in the main thread. Its absence never blocks the core workflow.

For composition or editing, return the draft and only material suggestions or missing-context questions. The main
thread adopts delegated results as appropriate and renders them for the user.
