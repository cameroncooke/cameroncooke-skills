# Slop Swatter Final Report Template

Use this exact structure. Do not omit failed, blocked, or unknown gates.

```markdown
## Slop Swatter Report

### Status
- Result: completed | blocked; base branch: <branch>; convergence passes: <n>; final fresh pass clean: yes/no; orchestrator edited code directly: no

### Scope verified
- Effective PR changed files: <count/list>; untracked included: <list or none>; staged/unstaged used only for completeness: yes | no
- Changed files read in full: <list>; complete effective diff reviewed: yes | no

### Work intent and domain context
- Product/domain: <area>; user journey: <workflow>; entities: <domain objects>
- Purpose/goals: <what the change implements and expected outcomes>; behavior model: <why/runtime flow/regression boundaries>
- Business rules/external contracts: <rules, APIs, persistence, permissions, analytics, etc.>
- Intended behavior/non-goals: <preserved behavior and feature boundaries>
- Validation strategy/risk constraints: <checks/tests and auth/billing/data/API/build risks>
- Feature coverage model: <required modules/routes/help output/tests/fixtures/project-file mutations and non-goals>

### Opportunity ledger
| ID | Type | Files | Category | Status | Resolution evidence |
|---|---|---|---|---|---|
| <id> | cleanup/behavior-restoration/public-surface/validation/unrelated-churn | <files> | <category> | fixed/invalid/blocked/deferred | <evidence> |

### Simplification and coverage metrics
- Total changed-line footprint: baseline <n>; final <n>; delta <n/%>; behavior-restoration/test increase justified: yes/no/n/a
- Slop-specific footprint: baseline <n>; final <n>; reduction <n/%>
- Complexity proxy: <name>; baseline <n>; final <n>; reduction <n/%>
- Feature-coverage proxy: <name>; baseline <n/status>; final <n/status>; missing coverage: <none/list>

### Subagents
- Mapper: <status/files>; scout: <status/files>; fallback auditor: <status or n/a>; implementer(s): <status/files>; validation: <status>; contract auditor: <status or n/a>

### Slop removed and patterns reused
- Slop removed: <concrete simplifications>
- Existing patterns reused: <pattern> — evidence: <file/reference>
- Fallbacks removed: <fallback X replaced by Y before merge, or none>
- Behavior/public coverage restored: <route/help/tests/fixtures/project-file behavior restored, or none>
- Unrelated churn removed: <process/docs/setup churn removed, or none>

### Hard gates
| Gate | Status | Evidence |
|---|---|---|
| project-instructions | pass/blocked | <evidence> |
| project-config | pass/blocked | <evidence> |
| work-intent/domain-context | pass/blocked | <evidence> |
| behavior-comprehension | pass/blocked | <evidence> |
| feature-coverage | pass/blocked | <evidence> |
| fallback | pass/blocked | <evidence> |
| opportunity-ledger | pass/blocked | <evidence> |
| convergence | pass/blocked | <evidence> |
| effective-PR-state | pass/blocked | <evidence> |
| full-file | pass/blocked | <evidence> |
| full-diff | pass/blocked | <evidence> |
| no-grep | pass/blocked | <evidence> |
| no-hidden-artifacts | pass/blocked | <evidence> |
| pattern-reuse | pass/blocked | <evidence> |
| defensive-code | pass/blocked | <evidence> |
| helper | pass/blocked | <evidence> |
| type-boilerplate | pass/blocked | <evidence> |
| unrelated-process-docs | pass/blocked | <evidence> |
| orchestrator-edit | pass/blocked | <evidence> |
| validation | pass/blocked | <evidence> |
| net-slop | pass/blocked | <evidence> |
| final-pass | pass/blocked | <evidence> |

### Behavior, validation, risks
- Public interfaces changed: yes/no, details; business behavior changed/restored: no/yes, evidence; tests added/updated: <details or none>; public-surface coverage: <covered/missing>
- Validation: `<command>` — pass/fail/not run, reason
- Risks or blockers: <none or list>
```
