# Workflow contract: [job]

- **Owner/approver:** [person or role]
- **Trigger / frequency:** [what starts it and how often]
- **Business outcome:** [why it matters]
- **Scope / exclusions:** [in scope | explicitly out]
- **Complexity:** [S / V / E]
- **Risk:** [L / M / H] (risk independent of complexity)
- **Baseline solution:** [manual/script/direct prompt/current agent]
- **Why a playbook:** [specific repeatability or errors reduced]
- **Inputs + source-of-truth:** [data, location, trust classification, privacy]
- **Permissions:** [read/write, allowed tools, prohibited side effects]
- **Outputs + exact destination:** [what and where]
- **Ordered steps:** [numbered]
- **Decision table:** [if / then / escalate]
- **Known edge cases:** [cases that previously failed]
- **Definition of done (outcome):** [externally observable state]
- **Verifier:** [trusted human/CI/test runner]
- **Required checks:** [must-run checks and protected location]
- **Approval boundary:** [what requires an explicit yes]
- **Fallback / rollback / time budget:** [what happens on failure]
- **Owner-reviewed examples:** [good / bad]
- **Open questions:** [not guessed]
- **Playbook version:** [Git revision once committed; until then "uncommitted draft"]
- **State:** DRAFT

<!-- State is one of: DRAFT, APPROVED FOR TRIAL, VERIFIED, RELEASE APPROVED. Only the owner moves it forward. -->
