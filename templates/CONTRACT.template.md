# Workflow contract: [job]

- **Owner/approver:** [person or role]
- **Trigger / frequency:** [what starts it and how often]
- **Business outcome:** [why it matters]
- **Scope / exclusions:** [in scope | explicitly out]
- **Complexity:** [one of S / V / E]
- **Lane:** [script / prompt / skill / skill + scripts / bounded agent / multi-agent (only with FRAMEWORK §5 evidence)]
- **Risk:** [one of L / M / H] (risk independent of complexity)
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
- **Playbook version:** [git revision once committed; until then none (uncommitted)]
- **Evidence snapshot:** [project revision the examples were taken from; "no commits" if none, "no repo" if the job belongs to none]
- **State:** DRAFT

<!-- State is one of: DRAFT, TRIAL, RELEASED. Only the owner moves it forward. -->

## Facts
- [confirmed by the owner or an artifact]

## Assumptions (need a yes)
- A1: [default chosen while the owner could not answer]

## Open questions (not guessed)
- [question, who answers it]
