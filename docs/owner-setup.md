# Repository owner setup

Repository files cannot enforce pull-request-only merging by themselves. Configure the following settings in GitHub
after the validation workflow has run successfully at least once.

## GitHub ruleset checklist

- Open **Settings → Rules → Rulesets → New branch ruleset**.
- Target the default branch.
- Enable **Require a pull request before merging**.
- Require at least one approval if you want review by another person; otherwise leave the approval count at zero.
- Enable **Require status checks to pass** and select the `validate` job from the `Validate` workflow.
- Enable **Require branches to be up to date before merging**.
- Enable **Block force pushes** and **Restrict deletions**.
- Do not add yourself to a bypass list if direct updates must be impossible for administrators too.
- Save and enable the ruleset.

Confirm the policy with a test pull request. The merge control should remain blocked when generated plugin copies are
stale or another required validation fails.
