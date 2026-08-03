# Changelog — fireworks-billing

## [1.1.0] - 2026-08-02

### Changed in 1.1.0

- Reframed spend reporting as billing usage because exported metrics do not
  provide authoritative currency charges.
- Updated authentication guidance to use `firectl signin`.
- Updated model grouping for the current `model_bucket` and `base_model_name`
  export columns.
- Made date boundaries explicit, validated ranges, and enforced the documented
  31-day export limit.
- Replaced undocumented stdout export behavior with a private temporary CSV.
- Simplified skill metadata and commands for Codex and Claude Code portability.

### Removed in 1.1.0

- Removed the unsupported CLI credit-balance lookup. Use the Fireworks billing
  dashboard for credits and monetary charges.

### Added in 1.1.0

- CSV schema validation, accelerator usage, usage-type summaries, safer errors,
  and offline fixture-based tests.

## [1.0.1] - 2026-02-18

### Changed in 1.0.1

- Improved `balance` output and added `--verbose` for full account details.
- Reported empty billing metrics as no recorded usage.
- Refactored argument parsing with `argparse`.

## [1.0.0] - 2026-02-18

### Added in 1.0.0

- Initial skill using the official `firectl` CLI.
- Balance and spend-analysis commands.
- Custom date ranges and per-model token totals.
- Authentication check and CSV parsing.
