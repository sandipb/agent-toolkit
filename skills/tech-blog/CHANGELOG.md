# Changelog

## 1.3.1 - 2026-09-25

- Require the `avoid-ai-writing` detect pass for substantive prose, including review-only work; report when unavailable.

## 1.3.0 - 2026-09-23

- Let the main thread choose direct work, editor reuse, or new delegation based on the task.
- Require a fresh reviewer only when a review is presented as independent.
- Allow supported restructuring in the draft and keep delegated reviews focused on language findings.
- Keep technical verification out of writing-review handoffs, including mixed requests.

## 1.2.0 - 2026-09-09

- Limit optional specialist findings to concrete clarity, coherence, or readability problems.
- Preserve supported author voice and purposeful narrative pacing during specialist review.
- Reject findings that conflict with shared invariants or lack a concrete reader benefit.

## 1.1.0 - 2026-08-15

- Require a fresh, isolated editor for every task, with no same-context fallback.
- Fail closed when isolation is unavailable, including in Pi without the official extension.
- Keep the `avoid-ai-writing` review optional.

## 1.0.0 - 2026-08-11

- Added source-bounded composition, editing, review, and flexible editorial orchestration for technical articles.
