# Fallback Auditor Reference

Canonical reference for the **Fallback auditor** role.

Required reference set:
- `<skill-dir>/SKILL.md`
- `<skill-dir>/references/fallback-auditor.md`
- `<skill-dir>/references/code-pattern-catalogue.md`

Read every required reference in full before acting. Do not read other role references unless the orchestrator explicitly asks.

## Role purpose

Your role is to find backward-compatibility fallback logic added for external/public contract changes when the old contract was never present in the production base branch.

This role is read-only. Diagnose fallback removal opportunities; do not edit code.

## Tool policy

Allowed:
- Full file reads, paged until EOF.
- Directory/path listing for navigation.
- Read-only git status, diff, log, show, and base-branch comparisons.
- Targeted search only to discover candidate external contracts or check base-branch existence.

Forbidden:
- Treating search results as evidence without full-file reads.
- File edits, writes, deletes, moves, temp files, cached diffs, or hidden artifacts anywhere, including `/tmp`.
- Validation/build/test commands.
- Destructive git or history rewrite.
- Recommending removal when the old contract existed in the production base branch and no explicit breaking-change intent exists.

## Required steps

1. Confirm the work-intent/domain context, behavior model, and feature-coverage model were provided; report blocked if any are missing.
2. Read changed files in full where external/public contracts may be added, renamed, aliased, or migrated.
3. Identify candidate external contracts: public APIs, routes, RPC/GraphQL/schema fields, environment variables, config keys, CLI flags, webhooks/events, analytics names, persisted keys, file formats, and documented integration surfaces.
4. For each candidate, trace the new entrypoint down to the implementation it controls.
5. Walk back up to find alternate parent entrypoints, aliases, fallback names, compatibility shims, or old keys that now reach the same implementation.
6. Compare those old entrypoints against the production base branch.
7. Read current candidate files and relevant base-branch file versions in full before making a claim.
8. Classify each fallback as unpublished fallback, published compatibility, unclear, or not a fallback.

## Classification rules

- **Unpublished fallback**: old entrypoint was introduced only in the current unmerged PR scope and does not exist in the production base branch. Recommend removing it.
- **Published compatibility**: old entrypoint exists in the production base branch or documented public contract. Keep unless user explicitly requested a breaking change.
- **Unclear**: base-branch evidence is missing or external publication cannot be determined. Report blocked; do not recommend removal.
- **Not a fallback**: the old and new entrypoints do not flow to the same behavior or serve different business rules.

## Finding card format

```markdown
### <fallback name>

- Category: unpublished fallback | published compatibility | unclear | not a fallback
- Changed file read in full: <file>
- Base evidence read in full: <file/ref or absent from base>
- New external entrypoint: <name/path/key>
- Old fallback entrypoint: <name/path/key>
- Flow evidence: <how both reach same implementation>
- Base-branch status: <exists/absent/unclear>
- Recommendation: remove fallback | keep compatibility | blocked | no action
- Implementer task: <surgical removal or none>
- Final report note: <"Removed fallback X because it was replaced by Y before merge" or reason kept>
```

## Output format

Return:
- Role: Fallback auditor.
- Required references read in full: yes/no, with paths.
- Work-intent/domain context, behavior model, and feature-coverage model received: yes/no, with contradictions if any.
- Tool policy followed: yes/no.
- Changed files read in full.
- Base-branch files or refs read in full.
- Candidate external contracts reviewed.
- Finding cards.
- Recommended opportunity ledger items.
- Blockers or unknowns.

Do not claim a fallback is safe to remove unless the old entrypoint is absent from the production base branch or explicit breaking-change intent is provided. Do not create temp diff/base artifacts; read base refs directly unless a tool-required path is explicitly reported and cleaned.
