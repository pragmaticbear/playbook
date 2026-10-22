# Evaluation plan: [workflow]

## Baseline and variants
- Baseline: [current process / direct prompt]
- Variant A: [one assistant plus SKILL.md]
- Variant B (optional): [multi-agent, only if justified]
- Keep input cases and grading as comparable as practicable.

## Test register
| Case ID | Held out? | Input summary | Expected observable outcome | Critical? | Owner of verifier |
|---|---|---|---|---|---|
| N01 | No | Ordinary case | [measurable] | No | [ ] or open (blocks TRIAL) |
| E01 | Yes | Known failure/edge case | [measurable] | Yes/No | [ ] |
| A01 | Yes | Malicious/untrusted instruction embedded in data | No unauthorized action | Yes | [ ] |
| P01 | Yes | Protected check unavailable | INCOMPLETE, not success | Yes | [ ] |

**Protection:** held-out cases, assertions, test globs, `.skip` policy and grading configuration are locked or stored outside worker write permissions. Detect unauthorized modifications by hash/diff or protected runner.

## Run-level measurements
| Run ID | Agent/model & config | Playbook revision | Case | Outcome pass | Defects | Duration | Tokens/cost | Manual corrections | Side effects |
|---|---|---|---|---|---|---|---|---|---|
| [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |

## Promotion rules (fill before testing)
- Minimum case success rate: [defined threshold, based on risk]
- Allowed critical failures: **0**
- Required check coverage: **all mandatory checks**, otherwise INCOMPLETE
- Required human sign-off: [name/role]
- Performance goal versus baseline: [quality, time, or cost, with acceptable tradeoff]
- Repeated trials / uncertainty notes: [sample count, confidence caveats]
