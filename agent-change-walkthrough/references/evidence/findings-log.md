# Findings Log

Maintenance-only file. Not loaded at runtime. Records why the skill's rules exist so future
revisions don't regress them. Examples live in `working-set.md`; reserved validation cases in
`holdout-set.md`.

## 2026-06-11 — Walkthrough depth revision (user feedback)

Five failure patterns reported from real walkthrough output, each mapped to a rule now in
`SKILL.md`:

| # | Failure pattern | Root cause | Skill delta |
|---|----------------|------------|-------------|
| 1 | Example data illustrated one path through branchy logic instead of proving every branch | Example guidance only asked for "concrete example data" | "Branch-complete example data" section: one scenario per branch/membership combination, table or labeled list ([EX-002]) |
| 2 | Moved/extracted code presented as brand-new; only the new file shown | No rule forced recovering the before version across files | "Before/after rules": Before recovered from base revision even across files; simplified Before allowed (labeled), After verbatim; moved code is one step with identical-vs-changed prose ([EX-001]) |
| 3 | Logic explained only above snippets, or not at all | Bullet order implied but did not require placement | Explicit rule: substantive explanation below the code blocks it describes ([EX-003]) |
| 4 | Large rewrites rendered as unified diffs (unreadable) or new-only blocks | Single "prefer mini-diff" rule regardless of change size | Size rule: 1–2 changed lines → diff block; larger → separate labeled Before/After blocks ([EX-004]) |
| 5 | Unchanged context steps mistakable for new work | `[UNCHANGED CONTEXT]` heading tag alone too subtle | Mandatory literal blockquote note line opening every unchanged step ([EX-005]) |

Secondary fixes from the same pass: exit criterion for `Filename:` headers narrowed so base-revision
Before blocks may omit `:start_line`; orphaned "semantic effect per hunk" rule re-homed under the
before/after rules.

Holdout validation, same day: HX-001 staged in a scratch repo and run by a fresh agent blind to
the pass criteria — PASS on all four criteria (details in the HX-001 record). One observation, not
yet promoted to a rule change: an elided Before block was not labeled `Before (simplified)`,
suggesting the labeling rule may be stated too far from the Before/After formatting examples to
reliably fire. Revisit if it recurs. HX-002 remains unexercised.

Unresolved risks:

- Branch-completeness for combinatorial logic could explode table size; the skill does not yet cap
  or sample scenarios. Watch for bloated walkthroughs on functions with many independent flags.
- "Verbatim After" conflicts with the existing no-full-file-dumps rule for very large new
  functions; no explicit reconciliation rule yet.
- No automated check exists; compliance rests on the exit-criteria checklist.
