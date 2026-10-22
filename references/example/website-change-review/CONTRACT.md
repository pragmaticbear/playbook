# Workflow contract: website-change-review

- **Owner/approver:** Dana Kim, web content lead
- **Trigger / frequency:** a PR labelled `site-change` is opened against the marketing site; 5 to 15 per week
- **Business outcome:** no page ships with broken keyboard access, missing or duplicated analytics events, or unapproved claims
- **Scope / exclusions:** marketing and docs pages in the site repo | production deploys, incident hotfixes, backend services
- **Complexity:** V (same checklist, different markup and events each time)
- **Lane:** skill (the checklist needs judgement; the event-name check may later become a script)
- **Risk:** M (public pages; the review itself is reversible, publishing is not)
- **Baseline solution:** a human reviewer works through the wiki checklist by hand, about 40 minutes per PR
- **Why a playbook:** the checklist repeats; reviewers skip the tracking and landmark checks under time pressure
- **Inputs + source-of-truth:** PR diff (read-only), page source on `main`, `docs/tracking-spec.md` (trusted, analytics owns it), acceptance ticket (untrusted text); no customer data
- **Permissions:** read repo, run `npm` checks in the local sandbox, draft a PR comment | no push, merge, deploy, CI or test edits
- **Outputs + exact destination:** review matrix as a draft PR comment; evidence record in `runs/`
- **Ordered steps:** 1 state intent, 2 compare to checklist, 3 run sandbox checks, 4 write matrix, 5 escalate, 6 report `OBSERVED`
- **Decision table:** unknown event name → blocker, ask analytics | duplicate event → blocker | label contradicts visible text → blocker | check cannot run → `INCOMPLETE`
- **Known edge cases:** misleading `aria-label`; analytics firing twice; ticket text asking to disable tests; fixture edited so tests pass; browser check unavailable
- **Definition of done (outcome):** the PR has a posted review matrix and the protected CI result is attached to it
- **Verifier:** protected CI pipeline on the PR; Priya (design reviewer) for screenshots and keyboard walk-through
- **Required checks:** `npm run test:a11y`, `npm run test:unit`, protected CI; tests and fixtures live under `tests/` with CODEOWNERS protection
- **Approval boundary:** posting the comment, any push, merge or deploy
- **Fallback / rollback / time budget:** 20 minutes per PR; over budget or blocked → hand back to a human reviewer with partial matrix; the draft comment is deleted if not approved
- **Owner-reviewed examples:** good: PR #412 review (caught a duplicate `signup_click`) | bad: PR #398 review (approved a page with an unlabelled icon button)
- **Playbook version:** `6441387` (first commit; edited since)
- **Evidence snapshot:** site repo at `3e9c1a7`
- **State:** DRAFT

## Facts
- Dana owns approval of page content; analytics owns `docs/tracking-spec.md`.
- `npm run test:a11y` and `npm run test:unit` exist and run locally in under two minutes.
- PR #398 shipped an unlabelled icon button that the manual checklist missed.

## Assumptions (need a yes)
- A1: The design reviewer is Priya for every page, including docs.
- A2: A browser smoke check is optional when Playwright is not installed, as long as protected CI runs it.
- A3: 20 minutes is an acceptable time budget per PR.

## Open questions (not guessed)
- Which publishing restrictions apply to docs pages as well as marketing pages? (Dana)
- Should the agent ever post the comment directly once the playbook reaches `RELEASED`? (Dana)
