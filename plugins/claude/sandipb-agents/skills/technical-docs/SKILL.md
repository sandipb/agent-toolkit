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

For substantive prose—more than a few sentences, such as a multi-paragraph document—run `avoid-ai-writing` in
detect-only mode on the current draft before returning composition or edits, and as part of review-only work. Run it
even when the main thread sees no obvious pattern. Use a sibling reviewer when available; otherwise run the pass in
the main thread. For
short text, run it when requested or when a concrete language pattern warrants it. Ask for critique, not rewriting,
with location, pattern, severity, `safe-fix` or `author-judgment`, rationale, and suggested direction.
Require each finding to identify a concrete problem with clarity, coherence, or readability. Vocabulary, sentence
length, punctuation, and conversational tone are not independent acceptance criteria. Deduplicate findings. Fix
specific filler, formulaic phrasing, ornamental wording that adds no information or useful emphasis, awkward rhythm,
or unclear passages when the change preserves technical meaning. Reject mechanical-only flags and changes that
conflict with the shared invariants. Send remaining findings to an
editor for reconciliation or handle them in the main thread. If the skill is unavailable, report that the pass was not
run and continue the core workflow. Repeat the pass only after material revisions introduce new prose.

For composition or editing, return the draft and only material suggestions or missing-context questions. The main
thread adopts delegated results as appropriate and renders them for the user.
