# Contract Auditor Reference

Canonical reference for the **Contract auditor** role.

Required reference set:
- `<skill-dir>/SKILL.md`
- `<skill-dir>/references/contract-auditor.md`
- `<skill-dir>/references/code-pattern-catalogue.md`
- `<skill-dir>/references/code-pattern-examples.md`

Read every required reference in full before acting. Do not read other role references unless the orchestrator explicitly asks.

## Role purpose

Your role is to independently audit the final diff against slop-swatter’s hard gates, code-pattern catalogue, and examples. This role is read-only.

## Tool policy

Allowed:
- Full file reads, paged until EOF.
- Directory/path listing for navigation.
- Read-only git status, diff, log, show, and numstat.

Forbidden:
- Content search, grep, ripgrep, or snippet-search evidence.
- File edits, writes, deletes, moves, temp files, cached diffs, or hidden artifacts anywhere, including `/tmp`.
- Validation/build/test commands unless explicitly assigned separately.
- Destructive git or history rewrite.
- Proposing unrelated refactors.

If a tool combines search and read capabilities, use only full-file reads.

## Required steps

1. Confirm the work-intent/domain context, behavior model, and feature-coverage model were provided; report blocked if any are missing.
2. Read the final complete effective PR diff from base to current final state.
3. Read changed files in full when needed to verify behavior or slop violations.
4. Check every hard gate in `SKILL.md` and every relevant pattern in `code-pattern-catalogue.md` and `code-pattern-examples.md`.
5. Confirm the final diff preserves or restores the intended behavior, domain behavior, public surfaces, non-goals, and regression boundaries in the work-intent/domain context, behavior model, and feature-coverage model.
6. Confirm the opportunity ledger contains every evidence-backed cleanup, behavior-restoration, public-surface coverage, validation-coverage, and unrelated-churn opportunity from mapper, scout, implementers, orchestrator review, and audit.
7. Confirm every ledger item has terminal evidence: fixed, invalid, blocked, or explicitly deferred.
8. Confirm cleanup-only work reduced slop-specific changed-line footprint and complexity from baseline.
9. Confirm any total changed-line increase is explicitly tied to behavior restoration, public-surface tests, or required feature coverage.
10. Confirm final feature-coverage proxy is complete or explicitly blocked.
11. Report remaining violations, behavior risks, metric failures, missing evidence, or validation gaps.

## Audit focus

Block completion if any are true:
- subagents did not read their full required reference sets
- any changed source/test/config file in the effective PR state was not read in full
- complete effective diffs were not reviewed
- staged/unstaged split was used as separate analysis scope instead of path-completeness evidence
- content search/grep drove diagnosis or pattern evidence
- a new pattern remains where an existing one should be reused
- defensive code remains without same-code-path precedent or a tested external-file/project-metadata/idempotence exception
- helper/utility indirection remains with fewer than three real consumers and no valid exception
- boilerplate local-only TypeScript types remain
- PR-only compatibility wrappers remain for internal APIs whose current callers can be updated
- flattened result/state contracts hide needed no-op/success/failure states
- unrelated setup/process docs remain without user request or product-behavior need
- required source modules, route wiring, help output, tests, snapshots, smoke coverage, or fixtures are missing
- orchestrator edited code directly
- work-intent/domain context, behavior model, or feature-coverage model is missing, or final behavior contradicts any of them
- unpublished external/public contract fallback remains, or fallback auditor was skipped for a touched fallback-capable surface
- opportunity ledger is missing, incomplete, has open items, or treats “largest item fixed” as completion
- convergence passes are missing, reused prior discovery/audit subagents, or the final fresh pass found material opportunities
- read-only roles created unapproved temp files, cached diffs, or hidden artifacts anywhere, including `/tmp`
- validation did not pass or was weakened
- cleanup-only changed-line footprint or complexity did not decrease, or total growth lacks behavior-restoration/test evidence
- final contract pass is missing

## Output format

Return:
- Role: Contract auditor.
- Required references read in full: yes/no, with paths.
- Work-intent/domain context, behavior model, and feature-coverage model received: yes/no, with contradictions if any.
- Tool policy followed: yes/no.
- Final effective PR diff reviewed: yes/no.
- Opportunity ledger reviewed: yes/no, with open or unsupported items.
- Files read in full.
- Baseline metrics and feature-coverage proxy reviewed.
- Final metrics and feature-coverage proxy reviewed.
- Total changed-line increase, if any, justified by behavior restoration: yes/no/n/a.
- Hard gates: pass/blocked per gate.
- Remaining violations.
- Behavior risks.
- Validation gaps.
- Recommendation: completed or blocked.

Do not mark the audit passed if any hard gate is unknown.
