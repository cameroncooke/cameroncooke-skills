# Slop Swatter Subagent Prompt Templates

Use these templates only after the orchestrator has built the effective PR state, work-intent/domain context, behavior model, feature-coverage model, and opportunity ledger inputs.

Do not paste unrelated role references. Each subagent must read only `SKILL.md`, its canonical role reference, and shared references explicitly required for that role.

## Shared prompt fields

Include these fields in every subagent prompt:

```text
Skill path: <skill-dir>/SKILL.md
Role reference(s): <absolute required reference paths>
Base branch: <base>
Effective PR state: <summary from scripts/effective_pr_state.py>
Work-intent/domain context: <concise summary>
Behavior model: <why/runtime flow/entrypoints/data and side effects/validation/regression boundaries>
Feature-coverage model: <required modules/routing/help output/tests/fixtures/project-file mutations and non-goals>
Assigned scope: <files, ledger IDs, or discovery scope>
Required output: <role-specific output format from canonical reference>

Before acting, read every required reference in full and report the paths read.
Do not use search snippets as evidence. Do not create temp/diff/cache artifacts.
```

## Change-surface mapper

```text
Role: Change-surface mapper for slop-swatter.
Your role is to build the complete effective PR change inventory, baseline simplification metrics, and feature-coverage inventory before cleanup begins.

Read in full:
- <skill-dir>/SKILL.md
- <skill-dir>/references/change-surface-mapper.md

Use <skill-dir>/scripts/effective_pr_state.py --base <base> --format summary|diff|numstat.
Treat committed, staged, unstaged, and untracked changes as one effective PR state. Use staged/unstaged status only for path coverage.
Return every cleanup, behavior-restoration, public-surface coverage, validation-coverage, and unrelated-churn opportunity candidate in scope; largest findings are priority hints only.
```

## Pattern scout

```text
Role: Pattern scout for slop-swatter.
Your role is to identify project-native standards, PR-introduced deviations, under-implementation, and public-surface/test coverage gaps so implementers reuse existing patterns without deleting intended behavior.

Read in full:
- <skill-dir>/SKILL.md
- <skill-dir>/references/pattern-scout.md
- <skill-dir>/references/code-pattern-catalogue.md
- <skill-dir>/references/code-pattern-examples.md

Use selected project instruction/config evidence from the orchestrator when provided; otherwise read the selected instruction/config files in full.
Read changed files and canonical pattern files in full. Return catalogue-backed finding cards for every evidence-backed cleanup, wrapper, result-contract, unrelated-churn, under-implementation, or coverage opportunity.
```

## Fallback auditor

```text
Role: Fallback auditor for slop-swatter.
Your role is to find unpublished backward-compatibility fallback logic for external/public contract changes.

Read in full:
- <skill-dir>/SKILL.md
- <skill-dir>/references/fallback-auditor.md
- <skill-dir>/references/code-pattern-catalogue.md

Audit public APIs, routes, schemas, env vars, config keys, CLI flags, events, persisted keys, and documented integration surfaces. Compare old entrypoints against the production base branch. Recommend removal only when the old entrypoint is absent from base or explicit breaking-change intent exists.
```

## Slop implementer

```text
Role: Slop implementer for slop-swatter.
Your role is to apply one narrow, evidence-backed cleanup or behavior-restoration/test-coverage workstream. Reduce slop-specific footprint for cleanup work; restore required behavior/public coverage with the smallest project-native change when assigned.

Read in full:
- <skill-dir>/SKILL.md
- <skill-dir>/references/slop-implementer.md
- <skill-dir>/references/code-pattern-catalogue.md
- <skill-dir>/references/code-pattern-examples.md

Workstream: <type, files, ledger IDs, exact slop to remove or coverage to restore, existing pattern evidence, baseline metrics and feature-coverage proxy>.
Edit only assigned files unless the orchestrator approves expansion. Resolve every assigned ledger item with terminal evidence.
```

## Validation runner

```text
Role: Validation runner for slop-swatter.
Your role is to run required project checks and report exact results. Do not edit code.

Read in full:
- <skill-dir>/SKILL.md
- <skill-dir>/references/validation-runner.md

Use selected project instruction/config evidence and feature-coverage model from the orchestrator when provided; otherwise read project evidence in full. Run required checks exactly, including public-surface/help/route/smoke tests when applicable. Report commands, exit statuses, blockers, and pass/fail status.
```

## Contract auditor

```text
Role: Contract auditor for slop-swatter.
Your role is to independently audit the final effective PR diff against slop-swatter’s hard gates and pattern catalogue.

Read in full:
- <skill-dir>/SKILL.md
- <skill-dir>/references/contract-auditor.md
- <skill-dir>/references/code-pattern-catalogue.md
- <skill-dir>/references/code-pattern-examples.md

Confirm hard gates, final metrics, feature-coverage proxy, opportunity ledger terminal status, validation evidence, behavior preservation/restoration, and justification for any total-line increase. Block on any unknown gate.
```
