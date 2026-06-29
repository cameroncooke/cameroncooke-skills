# Change-Surface Mapper Reference

Canonical reference for the **Change-surface mapper** role.

Required reference set:
- `<skill-dir>/SKILL.md`
- `<skill-dir>/references/change-surface-mapper.md`

Read every required reference in full before acting. Do not read other role references unless the orchestrator explicitly asks.

## Role purpose

Your role is to build the complete effective PR change inventory, baseline simplification metrics, feature-coverage inventory, and complete cleanup or behavior-coverage opportunity candidates before cleanup begins.

## Tool policy

Allowed:
- Full file reads, paged until EOF.
- Directory/path listing for navigation.
- Read-only bundled effective-state script execution.
- Read-only git status, diff, log, show, and numstat as fallback or path-coverage checks.

Forbidden:
- Content search, grep, ripgrep, or snippet-search evidence.
- File edits, writes, deletes, moves, temp files, cached diffs, or hidden artifacts anywhere, including `/tmp`.
- Validation/build/test commands.
- Destructive git or history rewrite.

If a tool combines search and read capabilities, use only full-file reads.

## Required steps

1. Confirm the work-intent/domain context, behavior model, and feature-coverage model were provided; report a blocker if any are missing or contradict the changed files.
2. Confirm the production base branch supplied by the orchestrator, or report ambiguity.
3. Build one effective changed-file set from the current final tree, as if `git add -A` happened now, without mutating the index.
4. Use `<skill-dir>/scripts/effective_pr_state.py --base <base> --format summary|diff|numstat` as the primary mechanism; raw Git is fallback only.
5. Use staged/unstaged status only to prove no path was missed; do not analyze them as separate categories.
6. Review the complete effective diff from base point to current final state.
7. Read current on-disk contents of every changed, non-deleted source/test/config file in full.
8. Capture baseline changed-line footprint using complete effective diff stats.
9. Identify at least one baseline complexity proxy and one feature-coverage proxy.
10. Identify risk areas: public APIs, CLI/help output, routing/dispatch, auth, billing, data, persistence, migrations, generated files, build/test config, project-file mutation, fixtures.
11. Map public/user-visible surfaces touched by the PR to implementation files and expected tests/snapshots/smoke coverage.
12. Identify every cleanup, under-implementation, behavior-restoration, public-surface coverage, and unrelated-churn candidate visible from the mapped effective PR scope. You may rank the largest opportunities first, but must not stop there.
13. Suggest narrow implementer workstreams.

## Baseline metrics

Changed-line footprint:
- Count additions plus deletions across the full effective PR source/test/config scope.
- Include committed-but-unmerged, staged/index, unstaged worktree, and untracked files as one final state.
- Use the same effective scope later for final comparison.

Recommended read-only command when git is available:

```bash
python <skill-dir>/scripts/effective_pr_state.py --base <base> --format numstat
```

The script includes untracked files as all-added rows.

Complexity proxy: identify at least one relevant count, such as:
- helper/utility count
- defensive branch count
- explicit local-only TypeScript type count
- branch count
- wrapper count
- new project-pattern variant count

Feature-coverage proxy: identify at least one relevant count, such as:
- public route/command/API entries with direct tests
- help snapshots updated for changed CLI choices
- required implementation modules present
- smoke tests for project-file mutations
- fixture support for new behavior paths

## Output format

Return:
- Role: Change-surface mapper.
- Required references read in full: yes/no, with paths.
- Work-intent/domain context, behavior model, and feature-coverage model received: yes/no, with contradictions if any.
- Tool policy followed: yes/no.
- Base branch used.
- Effective changed-file set and scope-completeness inputs checked.
- Files read in full.
- Complete effective diff reviewed.
- Baseline changed-line footprint.
- Baseline complexity proxy candidates.
- Baseline feature-coverage proxy candidates.
- Risk areas.
- Public/user-visible surfaces mapped to implementation and validation coverage.
- Complete cleanup, behavior-restoration, public-surface coverage, and unrelated-churn opportunity candidates for the mapped effective scope, with largest items marked only as priority hints.
- Suggested narrow implementer workstreams.
- Blockers or unknowns.

Do not present the mapping as complete if staged/unstaged were analyzed as separate scopes, any changed source/test/config file was not read in full, you only reported the largest opportunity instead of all evidence-backed cleanup or behavior-coverage candidates in scope, or you created unapproved temp/diff artifacts.
