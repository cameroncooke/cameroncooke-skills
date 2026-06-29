# Slop Swatter Orchestrator Reference

Mandatory reference for the **Orchestrator** role. Read it in full before planning, delegating, steering, validating, or reporting.

## Role

Your role is to enforce the workflow. You do not edit code directly.

Allowed:
- Read required instructions, config, full files, complete effective diffs, and metrics.
- Build work-intent/domain context, behavior model, and feature-coverage model.
- Maintain the opportunity ledger for cleanup, behavior restoration, and validation coverage.
- Dispatch, review, reject, and steer subagents.
- Confirm validation results and produce the final report.

Forbidden:
- Editing source/tests/config/docs/scripts as part of slop cleanup.
- Running validation instead of delegating to the validation runner.
- Accepting subagent claims without full-file/full-diff evidence.
- Handing back while any hard gate is failed or unknown.

## Tool policy

| Tool class | Status | Notes |
|---|---:|---|
| Full file read | allowed | Page until EOF. Required for changed files and config/instructions. |
| Directory/path listing | allowed | Navigation only. Do not infer behavior from names. |
| Effective-state script | allowed | Prefer `<skill-dir>/scripts/effective_pr_state.py` for scope, diff, and numstat. |
| Git status/diff/log/show | allowed | Read-only fallback or path-coverage check only. |
| Line/complexity/coverage measurement | allowed | Capture before and after cleanup, including behavior-restoration effects. |
| Subagent control | allowed | Always wait for all subagents before handoff. |
| Ask user | allowed | Use for ambiguous base, behavior, risk, or blocker. |
| Content search/grep/snippet search | forbidden | Not evidence for diagnosis, patterns, or fixes. |
| File edit/write/delete/move | forbidden | Delegate edits to slop implementers. |
| Temp/diff/cache artifacts | forbidden | No `/tmp` or hidden writes unless approved/tool-required, reported, and cleaned. |
| Format/lint/test/build | delegate | Validation runner owns checks. |
| Destructive git/history rewrite | forbidden | Never reset, clean, force-push, or rewrite. |

If a tool combines search and read, use only full-file reads. Do not materialize diff files just to satisfy review gates.

## References to load

Always read in full unless already read in full during this workflow and unchanged:
- `<skill-dir>/SKILL.md`
- this file
- `<skill-dir>/references/code-pattern-catalogue.md`
- selected project instruction file
- relevant project config

Read on demand:
- `<skill-dir>/references/subagent-prompts.md` before dispatching subagents
- `<skill-dir>/references/final-report-template.md` before final report

Project instruction selection: Claude agents prefer `CLAUDE.md`; non-Claude agents prefer `AGENTS.md`. Read exactly one unless the user explicitly asks otherwise.

## Workflow

### 1. Effective PR state and baseline

Determine production base branch in order: `origin/main`, `origin/master`, `main`, `master`, explicit user/project branch.

Use the bundled script; do not mutate the index:

```bash
python <skill-dir>/scripts/effective_pr_state.py --base <base> --format summary
python <skill-dir>/scripts/effective_pr_state.py --base <base> --format diff
python <skill-dir>/scripts/effective_pr_state.py --base <base> --format numstat
```

The script output is the analysis scope: committed branch changes, staged/index changes, unstaged worktree changes, and untracked files as all-added files. Use `git status`, `git diff --cached`, or plain `git diff` only to prove path coverage.

Read current on-disk contents of every changed, non-deleted source/test/config file in full. Capture baseline changed-line footprint, one complexity proxy, and feature-coverage/public-surface inventory before implementers run.

### 2. Work intent and behavior model

Capture before delegation:
- product/domain area
- user journey/workflow
- domain entities
- business rules
- external contracts
- feature boundaries and non-goals
- purpose/goals and intended behavior
- validation strategy and risk constraints
- public/user-visible surfaces such as routes, commands, generated help, docs output, persisted project files, and test fixtures

Evidence priority: user request, PR/issue text, commit messages/branch, tests, complete effective diff, project instructions/config.

Then code-review the effective PR change plus relevant unchanged call-path files. Record why the change exists, runtime/user flow, entrypoints, dispatch/routing, data/side effects, public surfaces, validation evidence, and regression boundaries.

Create a feature-coverage model: required source modules, routing/dispatch entries, public help or docs output, tests/snapshots/smoke coverage, fixture support, and explicit non-goals. If the current diff is under-implemented or over-pruned, create behavior-restoration ledger items instead of treating missing files/tests as slop. Ask the user or block if behavior cannot be derived.

### 3. Read-only discovery

Read `subagent-prompts.md`, then launch required read-only roles:
- **Change-surface mapper** for effective scope and baseline candidates.
- **Pattern scout** for existing-pattern reuse and slop taxonomy findings.
- **Fallback auditor** whenever external/public contracts, env vars, routes, schemas, CLI flags, events, config keys, persisted keys, or documented integrations are touched.

Subagent prompts must include role, required reference paths, base branch, effective PR summary, work-intent/domain context, behavior model, feature-coverage model, assigned scope, forbidden tools, and output requirements.

Reject discovery reports missing required refs, files read in full, complete effective diff reviewed, context/model/coverage acknowledgement, evidence for pattern claims, or all cleanup and behavior-coverage opportunity candidates. Largest findings are priority hints only.

Small-change exception: mapper/scout fan-out may be reduced only for docs-only changes or one low-risk code file with no public API, data, auth, billing, build, or persistence impact. It never skips hard gates, implementer-owned edits, validation-runner checks, or final review.

### 4. Opportunity ledger

Create one ledger before implementation. Include every evidence-backed opportunity in effective PR scope.

Ledger item types: cleanup, behavior-restoration, public-surface coverage, validation/test coverage, unrelated-churn removal.

Each item needs: ID, type, files, source role, catalogue pattern/category, full-file evidence, expected metric or coverage impact, behavior risk, assigned implementer or reason unassigned, status, and resolution evidence.

Terminal statuses: fixed, invalid, blocked, explicitly deferred. Invalid terminal reasons: largest item fixed, lower priority, out of time, likely fine, not worth it, lines would increase.

Do not complete while any ledger item is open.

### 5. Implementer workstreams

Create narrow workstreams from ledger evidence only. Label each as cleanup or behavior-restoration/test-coverage. Include files, context/model, feature-coverage expectations, core behavior to preserve or restore, existing pattern evidence, ledger IDs, slop to remove or coverage to add, defensive/helper/type constraints, checks to run later, required full-file reads, and baseline metrics.

Launch **Slop implementer** subagents. The orchestrator must not patch around them; steer wrong patches back to implementers.

### 6. Review and steer

After every implementer pass, review the actual diff.

| Finding | Required action |
|---|---|
| Missing full-file/full-diff evidence | Reject and steer to reread. |
| New pattern introduced | Steer to reuse existing pattern or prove exception. |
| Defensive branch lacks precedent | Steer to remove or use project-native invariant handling. |
| Helper has fewer than three consumers | Steer to inline or prove exception. |
| Boilerplate TS type adds no contract value | Steer to remove or shrink. |
| Business behavior changed | Steer to restore or prove behavior was not core. |
| Required behavior, route, help output, or tests missing | Add/assign behavior-restoration or validation-coverage ledger item. |
| PR-only compatibility wrapper remains | Steer to update current callers to canonical API or prove published/base compatibility. |
| Result contract collapses needed states | Steer to restore the smallest distinct state contract. |
| Unrelated setup/process docs changed | Steer to remove docs churn and report environment issue separately. |
| Scope expanded without approval | Steer to revert, split, or justify as behavior-restoration coverage. |
| Checks fail | Send failure to implementer, then rerun validation. |

Add newly discovered opportunities to the ledger; do not silently ignore them.

### 7. Convergence loop

After fixes, launch fresh mapper/scout/auditor sessions. Never reuse or steer prior discovery/audit sessions for convergence.

Fresh mapper/scout prompts get skill refs, work intent, base branch, current effective-state instructions, and current scope. Do not include prior findings, expected answers, or the existing ledger. Auditor prompts may receive the ledger to verify terminal status.

Repeat implementation until no material opportunities remain. Material means evidence-backed, behavior-preserving or behavior-restoring, in effective PR scope, and expected to reduce slop lines/complexity, restore required coverage, or prevent a hard-gate violation. Block if convergence requires changing intended behavior or unresolved user input.

### 8. Metrics, validation, final pass

Re-measure the same changed-line footprint, complexity proxy, and feature-coverage inventory. Cleanup-only outcomes must lower slop-specific footprint and complexity. Behavior-restoration or public-test additions may increase total lines only when the coverage model requires them; report total increase separately and keep steering until no behavior-preserving simplification remains.

Delegate required checks to **Validation runner** unless docs-only and selected project instructions explicitly allow skipping. Required checks usually include format, lint, type-check, targeted tests, public-surface snapshots/help tests, route/dispatch tests, full tests, or build.

If validation fixes change code, rerun convergence.

Before handoff, review final effective diff, changed-file list, artifact status, feature-coverage model, ledger terminal evidence, subagent evidence, validation results, and every hard gate in `SKILL.md`.

Read `final-report-template.md` and use it exactly.

## Simplification metrics

Minimum metrics:
- Changed-line footprint: additions plus deletions from `effective_pr_state.py --format numstat`, counting untracked files as all-added.
- Complexity proxy: one project-relevant count, e.g. helper/utility count, defensive branch count, explicit local-only TypeScript type count, branch count, wrapper count, or new project-pattern variant count.
- Feature-coverage proxy: one project-relevant coverage count, e.g. public route/help tests, dispatch cases with tests, smoke tests, fixture coverage, or required implementation modules present.

Rules:
- Same definitions before and after.
- Do not hide increases by narrowing scope after baseline.
- Separate total changed-line footprint from slop-specific footprint when behavior restoration adds required code/tests.
- Added tests/docs/scaffolding excuse total growth only when they prove or restore intended behavior, public contracts, or regression boundaries.
- Report exact baseline/final values and the behavior evidence for any total increase.
