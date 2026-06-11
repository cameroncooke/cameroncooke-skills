---
name: agent-change-walkthrough
description: Produces a single-story walkthrough of AI-authored code changes from runtime trigger to final behavior, weaving changed and unchanged code into one narrative with annotated diffs, trade-offs, alternatives, and risk analysis. Use when asked to "explain what changed", "walk me through this diff", "summarize agent edits", "show how this feature works", or "explain this implementation step by step".
allowed-tools: Read, Grep, Glob, Bash
---

Generate one coherent implementation story that explains how the code works end-to-end after the change.

## Step 1: Capture implementation intent

Restate the requested change in plain language.

Include:
- User problem being solved
- Scope boundaries
- Explicit non-goals

If requirements are ambiguous, state assumptions before proceeding.

## Step 2: Build evidence from conversation + git

Collect both sources before writing:

1. Conversation context (planning input only)
   - Requested outcome
   - Constraints and acceptance criteria
   - Domain context needed to interpret the code correctly

2. Git-based evidence (source of truth for output)
   - Changed file list
   - Diff per changed file (analyze full diffs locally, but only quote the minimum needed hunks in output)
   - Relevant unchanged context needed to explain behavior
   - The **before** version of every changed behavior — including logic that was moved, extracted, or rewritten across files. Recover it from the base revision; never settle for "this is new" without checking whether equivalent logic existed elsewhere before.

Use commands such as:

```bash
git status --short
git diff --name-only
git diff -- <file>
git show -- <file>
git show <base>:<path/to/file>      # recover the before version of a file
git log -p -S '<symbol or phrase>' # find where moved/extracted logic previously lived
```

Use history only when needed to disambiguate intent:

```bash
git log --oneline -- <file>
```

Never include conversation process, investigation history, or request negotiation as walkthrough steps. The walkthrough must describe implementation behavior only.
Never include full file dumps, raw secrets, credentials, tokens, private keys, or copied production payloads in the final output.

## Step 3: Build the story stack

Order story steps by **dependency-first causality**:
1. Introduce contracts/types/schemas/interfaces before showing call sites that use them
2. Introduce function/class definitions before showing new call paths that invoke them
3. Then continue in runtime flow order from trigger to final behavior

If runtime order and dependency order conflict, prefer dependency order and add one short transition sentence that reconnects to runtime flow.

Skip non-essential detail while preserving causal clarity.

## Step 4: Write each step as natural developer narrative

For each story step:
- Use a clear step title that describes behavior (no file path in the heading)
- Mark the step as `UNCHANGED CONTEXT` or `CHANGED` in the heading
- For `UNCHANGED CONTEXT` steps, open the body with the literal note line `> Unchanged — pre-existing code shown for flow context only; nothing in this snippet was touched by this change.` so unchanged code can never be mistaken for new or modified work
- Place `Filename: `<relative/path/to/file.ext:start_line>`` immediately above each snippet
- Optionally place `Symbol: `<function/method/class>`` above each snippet when useful
- Show the code following the before/after rules below
- Explain the logic in prose **below** the code blocks it describes — a one-sentence framing line above a snippet is fine, but the substantive explanation of how the code works always follows the code, never replaces or precedes it
- Explain what this step causes next in the flow
- Avoid forward references: do not use a field/type/function in a step before showing where it is defined or introduced

Avoid rigid template labels such as `Why this step exists:` or `Impact:`. Write readable, connected prose instead. Keep headings and narrative readable; put precise location in the snippet header.

### Write for a reader new to the codebase

Write every explanation in plain English for a competent developer who has never seen this repository. Knowing the language is assumed; knowing the codebase, its internal tools, or its domain vocabulary is not.

- Explain every project-specific term at first mention, in the same sentence — internal frameworks, config conventions, repo/service names, and domain vocabulary. Write "gated behind a new feature flag (`organizations:example-flag`); flags are switched on per customer from a separate configuration repo, so merging this change activates nothing by itself" — not "registered via FlagPole with rollout in options-automator".
- Anchor project-specific mechanisms to the general concept they implement (feature flag, database migration, background job, cache layer) so the reader has something familiar to hold on to.
- When behavior involves an interaction between builds, branches, requests, or services, walk a short numbered concrete scenario first (1. `main` has a full build, 2. PR1 uploads a partial one, 3. PR2 is opened on top of PR1, ...) and only then describe the mechanism in the abstract.
- State the problem in plain language before the solution mechanism — in the setup paragraph and within each step.
- Keep identifiers verbatim in and around code, but never let an identifier's name carry the explanation on its own.

### Before/after rules for changed code

Every `CHANGED` step must show both the before and the after. Never show only the new code:

- **Small changes (one or two changed lines in a hunk):** use a git-style mini-diff:

  ```diff
  - old behavior
  + new behavior
  ```

- **Larger changes:** show two separate code blocks, clearly labeled **Before** and **After**, each with its own `Filename:` header pointing at where that version lives (or lived).
- **The before must be shown even when it lived in a different file or had a different shape.** If code was extracted, moved, or rewritten, recover the prior logic from the base revision and present it as the Before block under its original filename. A simplified or pseudocode Before is acceptable when the original is long or noisy — label it `Before (simplified)` — but the **After block must always be verbatim** from the new code.
- **Moved or refactored code is never presented as brand-new.** When code is removed from one file and equivalent logic appears in another, treat that as one step: Before from the old location, After from the new location, followed by prose stating exactly what is mechanically identical and what actually changed — renamed variables, different data sources, revised conditions, or adjusted business rules, however subtle.

Call out the semantic effect of every changed hunk in the prose below its snippet.

### Branch-complete example data

When a changed step contains conditional branches, set/collection operations, or merge/categorization logic, the example block must *prove* the behavior, not just illustrate it:

- Provide one concrete example per distinct logic branch or input combination that produces a different result — every arm of an `if/elif/else`, and every meaningful membership combination (in A but not B, in B but not A, in both, in/out of a declared set, empty input).
- Present the scenarios as a compact table or a labeled scenario list, with sanitized synthetic values, so a reader can verify each branch's output by inspection.
- For simple single-path data-shape changes, a single before/after payload example remains sufficient.

Do not copy verbatim payloads from logs, production data, or repository fixtures that may contain sensitive information.

## Step 5: Integrate analysis inline

Embed analysis at the relevant story step:
- Trade-offs chosen at that step
- Viable alternatives and why not chosen
- Performance implications
- Failure modes and compatibility risk

Use natural language callouts in prose; keep them concise and specific.

## Step 6: End with concise close-out

After the final story step, add a short close-out with:
- What changed overall
- Why behavior is now different
- What to monitor or validate next

## Output contract

Return this structure:

1. `# Implementation Walkthrough`
2. One brief setup paragraph — the problem in plain language, then intent and scope
3. Numbered story steps (`## Step 1`, `## Step 2`, ...)
4. `## Final Outcome`

## Output example

Use this structure:

````markdown
# Implementation Walkthrough

Today, results produced by an agent and results produced by a human render identically, so users cannot tell which is which. This change makes the service record where each result came from and makes the UI render agent results differently. The flow from button click to render is otherwise untouched.

## Step 1 — User click enters the feature entrypoint [UNCHANGED CONTEXT]
> Unchanged — pre-existing code shown for flow context only; nothing in this snippet was touched by this change.

Filename: `src/ui/button.ts:42`
Symbol: `onClick`
```ts
button.onClick = () => startFeature(input)
```

The runtime trigger is still the button click. That handler forwards the input into the existing feature path, so the change does not alter how execution begins. From here, control moves into `startFeature()`.

## Step 2 — Entrypoint forwards to service [UNCHANGED CONTEXT]
> Unchanged — pre-existing code shown for flow context only; nothing in this snippet was touched by this change.

Filename: `src/feature/entry.ts:10`
Symbol: `startFeature`
```ts
export function startFeature(input: Input) {
  return run(input)
}
```

The orchestration layer continues to delegate work to `run()`, which means the new behavior is introduced deeper in the service layer, not at the boundary. That keeps the original control flow intact and localizes the behavior change.

## Step 3 — Sync categorization extracted into its own module and revised [CHANGED]
The categorization logic that previously lived inline in `run()` now lives in a dedicated module. The extraction is mostly mechanical, but one business rule changed, so both versions are shown.

Before (simplified) — inline logic removed from the old location:

Filename: `src/feature/service.ts` (base revision)
```ts
const matched = intersect(headIds, baseIds)
const added = diff(headIds, baseIds)
const removed = head.selective ? new Set() : diff(baseIds, headIds)
```

After (verbatim) — new module:

Filename: `src/feature/categorize.ts:12`
Symbol: `categorize`
```ts
export function categorize(head: Manifest, base: Manifest) {
  const headIds = new Set(Object.keys(head.items))
  const baseIds = new Set(Object.keys(base.items))
  const matched = intersect(headIds, baseIds)
  const added = diff(headIds, baseIds)
  let removed: Set<string>
  let skipped: Set<string>
  if (head.declaredIds) {
    removed = diff(baseIds, head.declaredIds)
    skipped = intersect(diff(head.declaredIds, headIds), baseIds)
  } else if (head.selective) {
    removed = new Set()
    skipped = diff(baseIds, headIds)
  } else {
    removed = diff(baseIds, headIds)
    skipped = new Set()
  }
  return { matched, added, removed, skipped }
}
```

The `matched` and `added` computations are mechanically identical to the old inline version — only their home moved. What actually changed: the old code knew only two modes (selective vs full), while the new code adds a third branch for an explicit `declaredIds` list, and selective mode now reports base-only names as `skipped` instead of silently dropping them.

Example input/output — one scenario per branch:

| Scenario | head items | base items | declaredIds / selective | matched | added | removed | skipped |
|---|---|---|---|---|---|---|---|
| Full mode, item dropped from head | `{a}` | `{a, b}` | — / `false` | `{a}` | `{}` | `{b}` | `{}` |
| Selective mode, item not uploaded | `{a}` | `{a, b}` | — / `true` | `{a}` | `{}` | `{}` | `{b}` |
| Declared list excludes `b` | `{a}` | `{a, b}` | `[a]` | `{a}` | `{}` | `{b}` | `{}` |
| Declared list includes `b`, not uploaded | `{a}` | `{a, b}` | `[a, b]` | `{a}` | `{}` | `{}` | `{b}` |
| New item only in head | `{a, c}` | `{a}` | — / `false` | `{a}` | `{c}` | `{}` | `{}` |

Rows 1–2 exercise the two pre-existing modes and confirm their behavior is preserved; rows 3–4 exercise the new `declaredIds` branch, showing that a name absent from the declared set is removed while a declared-but-not-uploaded name is merely skipped; row 5 confirms additions are mode-independent. Extracting rather than rewriting in place keeps `run()` readable and makes this branch table directly testable, at the cost of one extra module.

## Step 4 — Service return payload updated [CHANGED]

Filename: `src/feature/service.ts:88`
Symbol: `run`
```diff
- return { state: "pending" }
+ return { state: "ready", source: "agent" }
```

This one-line change is shown as a mini-diff. The service now includes source metadata in its return payload so downstream consumers can render source-specific UI behavior. The team chose to enrich the existing payload instead of creating a second metadata endpoint, which avoids an extra network hop, but there is a compatibility risk for legacy consumers that assume the old payload shape.

## Step 5 — UI consumes enriched payload [CHANGED]

Filename: `src/ui/render.ts:120`
Symbol: `renderState`
```diff
+ if (data.source === "agent") {
+   showAgentState()
+ }
```

Rendering now branches on the new `source` field, which is what makes the feature visible to users. This is purely additive (no prior branch existed here), and it is where the service-layer change becomes observable behavior.

## Final Outcome
The feature still starts at the same runtime trigger and follows the same orchestration path, but categorization now lives in its own module with a new declared-list mode, and the changed service payload drives source-aware rendering. Next validation should confirm that legacy consumers handle the added `source` field safely and that the declared-list branch is covered by tests.
````

## Validation and exit criteria

Complete only when all checks pass:

- Story begins at runtime trigger and ends at final observable behavior.
- Every changed file appears in at least one `CHANGED` story step.
- Every snippet header uses `Filename: relative/path/to/file.ext:start_line` format; Before blocks recovered from the base revision may omit `:start_line` but must name the original file and note the revision.
- No forward references: definitions/contracts appear before usages that depend on them.
- Unchanged-but-critical context appears in `UNCHANGED CONTEXT` steps, each opening with the literal unchanged note line.
- Every `CHANGED` step shows both before and after — never the new code alone. One-or-two-line changes use a `diff` block; larger changes use separate labeled Before/After blocks.
- Moved/extracted/refactored code shows the removed code from its original location as Before (simplified allowed, labeled) and the new code verbatim as After, with prose stating what is identical and what changed.
- Each changed hunk includes reason + behavioral effect.
- Substantive logic explanation appears below the code blocks it describes, not only above them.
- Data-shape/model/API changes include concrete example input/output with sanitized representative values.
- Branch-bearing changed logic (conditionals, set/collection operations, categorization/merge rules) includes one example scenario per distinct branch or input combination that yields a different result.
- Trade-offs, alternatives, performance notes, and risk notes appear at relevant steps.
- Every project-specific term, internal tool, or convention is explained in plain English at first mention; the prose stands alone for a developer with no prior knowledge of this codebase.
- Multi-actor or multi-build behavior is introduced with a concrete numbered scenario before the abstract mechanism.
- Facts are distinguished from inference.
- Unknowns are explicitly labeled.
- Conversation process/history does not appear as a walkthrough step.
- No claim of validation is made unless validation was actually performed.
- Snippets and examples contain no credentials, keys, tokens, or other sensitive values.

If any criterion fails, state what is missing and continue refining before finalizing.
