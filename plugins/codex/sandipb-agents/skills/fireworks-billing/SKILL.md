---
name: fireworks-billing
description: >
  Export and summarize Fireworks AI billing usage by date range, model, and
  usage type with the official firectl CLI. Use for Fireworks billing metrics,
  token usage, accelerator usage, or spend-related investigation. This reports
  usage rather than currency charges.
---

# Fireworks AI billing usage

Use the bundled script to export Fireworks billing metrics and summarize prompt
tokens, completion tokens, accelerator seconds, models, and usage types. Do not
describe these usage totals as currency spend.

## Prerequisites

- `firectl` installed using the [official instructions](https://docs.fireworks.ai/tools-sdks/firectl/firectl)
- `uv` installed to run the bundled Python script
- An authenticated Fireworks profile; use `firectl signin`

Never ask the user to paste an API key into chat or place one directly on a
command line. Let `firectl` use its authenticated profile.

## Workflow

1. Run the bundled `fireworks-billing.py` from this skill directory.
2. Use `usage` for a billing-usage summary. `spend` remains as a compatibility
   alias, but the result contains usage quantities, not dollar costs.
3. Explain that start dates are inclusive and end dates are exclusive.
4. Split ranges longer than 31 days into separate calls.
5. For credit balance or monetary charges, direct the user to the Fireworks
   billing dashboard; the documented CLI does not expose a stable balance query.

## Commands

```bash
# Previous UTC calendar day
./fireworks-billing.py usage

# Explicit inclusive-start/exclusive-end range
./fireworks-billing.py usage \
  --start-time 2026-02-17 \
  --end-time 2026-02-18
```

The script exports into a private temporary directory, validates the current CSV
schema, summarizes it, and removes the temporary data. It does not retain raw
billing records.

## Troubleshooting

- Missing `firectl`: follow the official installation instructions.
- Authentication failure: run `firectl signin`, then retry.
- Missing CSV columns: update `firectl` and this skill before trusting results.
- No rows: report that no usage was recorded for the requested interval.
- More than 31 days: split the interval; Fireworks limits each export to 31 days.

Current skill version: 1.1.0.
