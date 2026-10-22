---
name: workflow-name
description: Use when [concrete trigger and conditions]; not when [clear exclusion]. Triggers only — no summary of the steps.
---

# Workflow Name

## Purpose and triggering conditions
[One-paragraph description.]

## Preconditions and permitted actions
[Trusted input sources, required permissions, side effects not permitted.]

## Inputs
[Names, types, source location, and trust boundary.]

## Procedure
1. [Step and observable outcome.]
2. [Step and conditional branch.]
3. [Step and explicit escalation/approval boundary.]

## Decision and edge cases
- If [case], then [action]; otherwise [safe fallback].

## References and tools
- Read `references/[name].md` only when [condition].
- Use `assets/[name].md` as a template if approved.
- Run `scripts/[name].py` only when available and authorized.

## Done means
[Objective acceptance criteria and independent verifier.]

## Do not
- [Unauthorized actions, secret handling, changes to trusted tests, self-approval.]

## Reporting
State whether work was observed, independently verified or owner-approved, with evidence and blockers.
