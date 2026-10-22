# Security policy

## Supported versions

Only the latest version of playbook gets security fixes.

## Reporting a vulnerability

Please don't open a public issue for security problems. Use GitHub's private
reporting instead: go to the **Security** tab of this repo and click
**Report a vulnerability**.

Include what you found, how to reproduce it, and what an attacker could do with
it. You should hear back within a week.

## Scope

playbook is instructions for an AI agent plus a small validator script. Issues
that are in scope include:

- Wording in `SKILL.md`, the framework or the templates that leads an agent to
  act beyond what the user authorized, follow instructions found in task data,
  or self-approve a playbook
- Guidance that would put secrets or personal data into a reusable playbook or
  evidence record
- `scripts/validate.py` reading or writing outside the directory it is given
