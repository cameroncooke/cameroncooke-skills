---
name: slop-swatter
description: Aggressively remove AI slop from effective PR-state code changes before merge while preserving or restoring intended behavior, public contracts, tests, and project-native patterns. Use when asked to simplify, clean up, de-slop, de-AI, reduce overengineering, review implementation quality, correct overzealous simplification, or align committed, staged, unstaged, and untracked work as one final changeset.
---

# Slop Swatter

Remove AI-generated implementation slop from code before it merges to the production branch.

This is a strict workflow skill, not a style checklist. The process is mandatory: route to the right reference, use the defined roles, enforce the gates, steer non-compliant subagents, and validate before handoff. If a requirement cannot be satisfied, report the workflow as blocked instead of weakening it.

## Prime directive

Make the original change surgical, project-native, and merge-ready without deleting or under-implementing intended behavior. Behavior wins over smaller diffs: restore missing feature code, public-surface wiring, and tests when cleanup exposed an incomplete or over-pruned implementation.

Core behavior means business rules, user-visible outcomes, public interfaces, CLI/help output, routing, persistence/network contracts, authorization/billing/data semantics, project-file mutations, and test-observable product requirements.

Core behavior does **not** include incidental AI-added implementation structure: speculative fallbacks, defensive branches without precedent, wrapper helpers, verbose abstraction layers, redundant comments, boilerplate types, PR-only compatibility wrappers, or local setup/process documentation unrelated to the requested change.

## Mandatory reference routing

Path rule: treat `<skill-dir>` as the directory containing this `SKILL.md`.

The orchestrator must read `<skill-dir>/references/orchestrator.md` in full before planning or delegating.

Each role has an explicit required reference set. Subagents must read `SKILL.md`, their canonical role reference, and any shared reference explicitly listed for that role. Do not read other role references.

Roles that must inspect project instructions/config still read those project files as directed by their canonical reference.

The orchestrator must pass either:
- this `SKILL.md` plus the required reference file contents verbatim, or
- absolute paths to this `SKILL.md` and the required reference files with explicit instructions to read each file in full before acting.

Reject any subagent output that does not confirm its full required reference set was read in full.

## Project instruction selection

Read exactly one project instruction file by default:

- Claude agents: prefer `CLAUDE.md`; fall back to `AGENTS.md` only when `CLAUDE.md` is absent.
- Non-Claude agents: prefer `AGENTS.md`; fall back to `CLAUDE.md` only when `AGENTS.md` is absent.
- If neither exists, use the nearest equivalent project instruction file if one is clearly present.

Do not read both `AGENTS.md` and `CLAUDE.md` just because both are available. Report which file was selected and why.

If the selected instruction file, project config, `SKILL.md`, or a required reference was already read in full during the current workflow, do not re-read it. Reuse the recorded evidence unless the file changed, the earlier read was partial, or a subagent must independently confirm its own required reference.

## Non-negotiable hard gates

Fail the workflow, reject the subagent output, or steer for correction if any gate is violated.

1. **Project instructions gate** — the single selected project instruction file was not read in full or recorded as already read in full, or both `AGENTS.md` and `CLAUDE.md` were read without an explicit user instruction to do so.
2. **Project config gate** — relevant project config was not read in full before choosing validation commands or conventions.
3. **Work-intent/domain-context gate** — the orchestrator did not capture product/domain area, user journey, domain entities, business rules, external contracts, feature boundaries, purpose, goals, intended behavior, non-goals, public/user-visible surfaces, and validation strategy before delegating.
4. **Behavior-comprehension gate** — the orchestrator did not code-review the effective PR change to produce a behavior model covering why the change exists, what behavior it implements, what feature coverage is required, how it is validated, and what regression boundaries must be preserved before assigning refactors.
5. **Feature-coverage gate** — cleanup deleted, skipped, or failed to restore behavior, routing, public-surface wiring, fixture/test coverage, help output, or project-file mutations required by the work intent and behavior model.
6. **Fallback gate** — fallback logic for old external/public contracts was kept when the old entrypoint was absent from the production base branch or only existed inside the current unmerged PR scope.
7. **Opportunity ledger gate** — all evidence-backed simplification, behavior-restoration, and test/public-surface coverage opportunities in effective PR scope were not inventoried and resolved as fixed, invalid, blocked, or explicitly deferred with evidence.
8. **Convergence gate** — after fixes, newly launched discovery/audit subagents were not rerun until no material simplification or behavior-coverage opportunities remained. Do not reuse or steer prior discovery/audit subagent sessions for convergence passes.
9. **Effective-PR-state gate** — staged, unstaged, committed-but-unmerged, and untracked changes were not collapsed into one final effective PR state against the production base before analysis.
10. **Full-file gate** — every changed, non-deleted source/test/config file was not read in full before proposing or applying changes.
11. **Full-diff gate** — the complete effective PR diff was not reviewed before proposing or applying changes.
12. **No-grep gate** — grep/search snippets were used as the basis for diagnosis, pattern claims, or fixes, except targeted fallback/base-branch candidate discovery that is followed by full-file reads.
13. **No-hidden-artifacts gate** — read-only roles created temp files, cached diffs, materialized artifacts, or hidden outputs anywhere, including `/tmp`, without explicit approval or a tool-required path reported before use and cleaned up after use.
14. **Pattern-reuse gate** — a new pattern was kept or introduced when an existing project pattern could have been reused.
15. **Defensive-code gate** — defensive programming was kept or added without matching local precedent and evidence that callers/tests/business rules require it, except narrow parsing/idempotence guards for external user/project-file formats that are covered by tests.
16. **Helper gate** — a one- or two-line readability helper was kept or added, or a utility with fewer than three real consumers was kept without public/framework/complexity justification.
17. **Type-boilerplate gate** — explicit TypeScript object/interface/type boilerplate was kept or added where inference or a smaller local shape preserves correctness.
18. **Unrelated process-docs gate** — setup, contributing, workflow, or validation-environment documentation was changed to paper over local tool friction without user request or direct product-behavior need.
19. **Orchestrator-edit gate** — the orchestrator edited code directly instead of delegating implementation to a slop implementer.
20. **Validation gate** — required checks did not pass, were skipped, or were replaced with weaker checks without reporting the workflow as blocked.
21. **Net-slop gate** — baseline changed-line and complexity metrics were not captured before work, slop-specific footprint did not decrease for cleanup-only work, or any total-line increase from behavior restoration/tests was not explicitly justified by feature coverage evidence.
22. **Final-pass gate** — the final effective PR diff was not reviewed against this contract before handoff.

These gates are non-negotiable. Do not trade them off for speed, politeness, or perceived safety.

## Role routing

Use these role names exactly:

- **Orchestrator** — main agent. Read `<skill-dir>/references/orchestrator.md` and `<skill-dir>/references/code-pattern-catalogue.md`; read `<skill-dir>/references/subagent-prompts.md` before delegation and `<skill-dir>/references/final-report-template.md` before final report. Do not edit code.
- **Change-surface mapper** — subagent. Read `<skill-dir>/references/change-surface-mapper.md`. Build the complete effective PR change inventory, baseline metrics, and feature-coverage inventory.
- **Pattern scout** — subagent. Read `<skill-dir>/references/pattern-scout.md`, `<skill-dir>/references/code-pattern-catalogue.md`, and `<skill-dir>/references/code-pattern-examples.md`. Identify existing project patterns, PR-introduced variations, under-implementation, and coverage gaps.
- **Fallback auditor** — subagent. Read `<skill-dir>/references/fallback-auditor.md` and `<skill-dir>/references/code-pattern-catalogue.md`. Identify unpublished backward-compatibility fallbacks for external/public contracts by comparing current PR changes with the production base branch.
- **Slop implementer** — subagent. Read `<skill-dir>/references/slop-implementer.md`, `<skill-dir>/references/code-pattern-catalogue.md`, and `<skill-dir>/references/code-pattern-examples.md`. Apply scoped cleanup or behavior-restoration/test-coverage fixes only after full-file/full-diff reading.
- **Validation runner** — subagent. Read `<skill-dir>/references/validation-runner.md`. Run required checks and report exact results. The orchestrator may coordinate and review validation, but must not execute validation commands directly.
- **Contract auditor** — optional read-only subagent for broad/risky work. Read `<skill-dir>/references/contract-auditor.md`, `<skill-dir>/references/code-pattern-catalogue.md`, and `<skill-dir>/references/code-pattern-examples.md`. Audit the final diff against this contract.

## Required process summary

The detailed process lives in `<skill-dir>/references/orchestrator.md`; this summary is still binding.

1. Load this `SKILL.md`, the single selected project instruction file, project config, and the orchestrator reference in full.
2. Determine the production base branch and final effective PR state with `<skill-dir>/scripts/effective_pr_state.py`: committed-but-unmerged changes plus current worktree/index/untracked changes as if everything were staged now.
3. Capture concise work-intent and domain context: product/domain area, user journey, domain entities, business rules, external contracts, feature boundaries, purpose/goals, intended behavior, non-goals, public/user-visible surfaces, and validation strategy.
4. Produce a behavior and feature-coverage model from a code-review pass: why the change exists, what runtime/user behavior it implements, what routing/help/tests/fixtures/project-file behavior are required, how it is validated, and what regressions must be avoided.
5. Capture baseline changed-line, complexity, and feature-coverage metrics for the effective PR scope before cleanup begins.
6. Dispatch read-only mapper and pattern scout subagents for non-trivial changes; dispatch a fallback auditor whenever external/public contracts, environment variables, routes, schemas, CLI flags, events, config keys, persisted keys, or documented integration surfaces are touched.
7. Require subagents to read their full required reference set and report files/diffs read.
8. Inject the work-intent/domain context, behavior model, and feature-coverage model into every subagent prompt.
9. Build an opportunity ledger covering every evidence-backed simplification, behavior-restoration, public-surface, and validation-coverage opportunity in effective PR scope.
10. Create narrow implementer workstreams from the ledger and evidence, not preference; label each workstream as cleanup or behavior-restoration/test-coverage.
11. Delegate all code edits to slop implementers; the orchestrator must not patch directly.
12. Review actual diffs, reject non-compliant work, and steer subagents until every hard gate passes and every ledger item is fixed, invalid, blocked, or explicitly deferred with evidence.
13. Rerun fresh discovery/audit passes after fixes using newly launched subagents; repeat implementation until no material simplification or behavior-coverage opportunities remain.
14. Re-measure changed-line, complexity, and feature-coverage metrics. Cleanup-only outcomes must reduce slop footprint; behavior-restoration/test additions may increase total lines only when tied to explicit coverage evidence and no behavior-preserving simplification remains.
15. Delegate required validation from the selected project instruction/config evidence to a validation runner. Passing validation is mandatory unless an environmental blocker is reported.
16. If validation fixes change code, rerun the convergence pass.
17. Perform a final effective PR contract pass and produce the required final report.

## Small-change exception

A small-change exception may reduce role fan-out, but it does not weaken hard gates.

Allowed only when all are true:
- The change is docs-only, or a single low-risk code file with no public API, data, auth, billing, build, or persistence impact.
- The orchestrator still reads full files and complete diffs.
- The orchestrator explicitly reports which roles were skipped and why.
- Any code edit is still made by a slop implementer.
- Validation is still delegated to a validation runner unless the selected project instruction file explicitly allows skipping checks for docs-only changes.

Never use this exception to skip final contract review, hard gates, or blocker reporting.

## Completion criteria

Complete only when every statement is true:

- Each subagent read `SKILL.md` and its explicit required reference set, plus project instructions/config when that role requires them.
- The workflow steps were followed in order.
- Required roles were used, or a small-change exception was explicitly justified.
- The single selected project instruction file and project config were read in full or recorded as already read in full during the workflow.
- The orchestrator captured and injected concise work-intent and domain context before delegation.
- The orchestrator produced and injected a behavior model and feature-coverage model before assigning refactors.
- Fallback auditor ran for external/public contract changes, or the orchestrator documented why no fallback surface existed.
- The orchestrator maintained an opportunity ledger for all evidence-backed simplification, behavior-restoration, public-surface, and validation-coverage opportunities and resolved every item as fixed, invalid, blocked, or explicitly deferred with evidence.
- Fresh post-fix discovery/audit passes used newly launched subagents, never reused prior discovery/audit sessions, and repeated until no material simplification or behavior-coverage opportunities remained or the workflow was reported blocked for non-convergence.
- Effective PR state was identified against the production base; staged/unstaged split was treated only as scope-completeness noise, not as separate analysis scope.
- Every changed non-deleted source/test/config file was read in full.
- The complete effective PR diff was reviewed.
- No read-only role created unapproved temporary files, cached diffs, or hidden artifacts anywhere, including `/tmp`.
- Subagent outputs were reviewed and steered until compliant.
- Implementers made all code edits.
- The final diff satisfies every hard gate.
- Slop-specific changed-line footprint and complexity metrics are lower than the baseline for cleanup-only work, or any total increase is explicitly tied to behavior restoration, public-surface tests, or required feature coverage.
- Required checks passed, or the workflow is reported blocked with exact environmental reasons.
- The final report uses the template in `<skill-dir>/references/final-report-template.md`.

## Conflict resolution against generic simplifier guidance

These rules override generic code-simplifier instincts:

- “Explicit is better” does not justify boilerplate types, wrapper helpers, or verbose branches.
- “Readable helper” does not justify one- or two-line functions with fewer than three consumers.
- “Safer” does not justify defensive programming beyond codebase precedent, except narrow guards for external user/project-file parsing or idempotent project mutations with tests.
- “Project standard” means the selected project instruction file and observed local patterns, not generic external preferences.
- “Functionality” means core behavior, routing, public surfaces, tests, and contracts, not incidental defensive branches or AI-added implementation structure.
- “Smaller diff” does not justify deleting feature files, route wiring, help output, tests, or public-contract coverage required by the behavior model.
- “Backward compatible” does not justify wrappers for internal APIs that only existed inside the current unmerged PR when all callers can be updated.
- “Validation setup” does not justify unrelated process documentation changes; report environmental blockers separately.
- “Recently modified code” means the final effective PR state against the production base, including committed-but-unmerged, staged, unstaged, and untracked changes as one cohesive changeset.
- “Autonomous cleanup” still requires role separation, steering, validation, and final contract review.
