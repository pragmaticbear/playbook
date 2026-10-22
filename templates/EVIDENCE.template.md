# Evidence record: [run id: the ticket or task id, else the date's sequence number]

- **Date/time:** [ ]
- **Contract state and playbook revision:** [one of DRAFT/TRIAL/RELEASED; `git log -1 --format=%h -- <dir>`, none (uncommitted) or no repo]
- **Job and approver:** [ ]
- **Model/runtime/tool versions:** [ ]
- **Task input references (redact secrets):** [ ]
- **Permissions granted:** [ ]
- **Actions actually attempted:** [ ]
- **Artifacts/diffs + exact paths:** [ ]
- **Independent verifier and protected configuration:** [ ]
- **Check ID, command, runner, exit status, and actual captured output (secrets redacted, never the value):** [ ]
- **Outcome state proof (e.g. URL/record/CI artifact/screenshot):** [ ]
- **Unrun mandatory tests, anomalies, deviations (steps skipped on request) and side effects:** [ ]
- **Rollback location and instruction:** [ ]
- **Waivers:** [owner waivers of a required check, with who and why; the state stays INCOMPLETE]

## Three separate states
- [ ] `OBSERVED`: evidenced actions were taken (NOT equivalent to success).
- [ ] `VERIFIED`: independently required tests and outcome checks passed.
- [ ] `APPROVED`: authorized owner gave release/action permission.

**Overall:** `[one of OBSERVED / VERIFIED / APPROVED / INCOMPLETE / FAILED / BLOCKED]`

**Owner signature / approval reference:** [ ]

Do not fabricate links, commands, test output or completion status. A failed or unavailable required check is not verification.
