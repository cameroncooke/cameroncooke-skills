# Slop Swatter Code Pattern Catalogue

Shared pattern taxonomy for slop-swatter roles. Read this file only when a role reference explicitly requires it.

This file defines what counts as AI slop. Concrete examples live in `code-pattern-examples.md`; load that file only when the role reference requires examples or when a catalogue rule is ambiguous.

## Evidence rules

A pattern claim is valid only when backed by full-file evidence:

- Read the changed file in full.
- Read the canonical pattern file in full.
- Review the complete effective PR diff, not staged/unstaged sides separately.
- Name the divergence from project precedent.
- State the smallest behavior-preserving or behavior-restoring change.
- Trace changed public/user-facing surfaces to tests, snapshots, routes, commands, or callers when the PR touches them.
- State expected impact: fewer slop lines, lower complexity proxy, restored feature coverage, or stricter public-contract validation.

Invalid evidence:

- Search snippets, grep results, or filename inference.
- Generic style advice without project-local precedent.
- “Safer” without tests/callers/docs/business rules proving the state is expected.
- “Clearer” without reduced complexity, fewer changed lines, restored behavior coverage, or project convention.
- Lower line count that omits feature behavior, public-surface wiring, or required tests.

## Pattern taxonomy

### 1. Existing project pattern ignored

Failure: the PR introduces a new shape for something the codebase already solves.

Look for wrappers around directly used APIs, custom result objects beside shared error handling, new hook/component/data-loading shapes, new config styles, or local serializers beside project serializers.

Action: remove the local variant and reuse the project-native call/error/state/config/serialization pattern.

### 2. Similar-but-different local variant

Failure: the PR does roughly the same thing as existing code but changes names, object shape, branching, or flow.

Look for duplicate mappers, formatter variants, one-off option objects, parallel state names, or adapter objects that mirror existing domain objects.

Action: align names, shapes, and control flow with existing project evidence. Prefer small duplication over premature abstraction when fewer than three consumers exist.

### 3. Defensive programming without same-path precedent

Failure: the PR tolerates states the project does not otherwise tolerate.

Requires same-path precedent: `try/catch`, `??` defaults, optional chaining on required data, broad null checks, retries, coercion/normalization, and `safe*`/`ensure*`/`guard*` wrappers.

Allowed only when all are true:
1. Same kind of code path already uses the same technique.
2. Tests, callers, API docs, or business rules prove the input state is expected.
3. The branch does not hide an invariant violation.

Action: remove speculative fallback/guard/wrapper or replace it with the project’s existing invariant/error style.

### 4. Premature helper or DRY abstraction

Failure: helper indirection exists mainly to make a call site read like English or avoid tiny duplication.

Hard rules:
- One- or two-line readability helpers are slop unless required by public API/framework shape.
- Utility functions need three or more real consumers after cleanup.
- With fewer than three consumers, non-DRY duplication is preferred when it reduces indirection and stays readable.

Action: inline simple helpers; delete low-consumer utilities unless an exception applies.

### 5. Boilerplate TypeScript type surface

Failure: explicit types/interfaces restate obvious local object structure without preserving a real contract.

Look for local-only aliases, one-use interfaces, ceremonial return annotations, trivial one-use Props types where not project-required, or widened type surfaces between nearby functions.

Keep explicit types for exported/public APIs, JSON encode/decode boundaries, persistence/network payloads, large shared domain objects, non-obvious generics or inference hazards, and project-required conventions.

Action: prefer inferred local object types; shrink interfaces to the minimum contract shape.

### 6. Verbose branch or clever syntax

Failure: code is longer or harder to follow than the project pattern for the same decision.

Look for multi-line boolean assignment branches, if/switch chains for simple binary values, nested ternaries, and dense one-liners hiding multiple concerns.

Action: use direct booleans for boolean results, simple ternaries for simple binary values, and explicit branches for multiple cases or side effects.

### 7. Wholesale rewrite instead of surgical cleanup

Failure: the PR changes unrelated structure, names, flow, tests, or abstractions beyond the original behavior.

Look for unrelated file churn, renamed concepts with no behavior need, new framework/layer boundaries, rewritten tests that bless implementation churn, or broad cleanup inside a focused feature/fix.

Action: restore the smallest implementation surface that preserves intended behavior; split, revert, or remove unrelated churn.

### 8. Net growth in slop lines or complexity

Failure: cleanup increases slop-specific changed-line footprint or the selected complexity proxy, or hides growth by deleting required behavior.

Look for added helpers/types/branches, test/docs scaffolding unrelated to behavior, moving code without reducing total slop footprint, or deleting feature files/tests just to make metrics smaller.

Action: reduce changed lines and the selected complexity proxy for cleanup-only work. If restoring behavior or public-contract tests increases total lines, keep the restoration and report the slop-specific reduction separately.

### 9. Codified project standard bypassed

Failure: the PR ignores the selected project instruction file or consistent full-file local evidence.

Relevant standards include import style/order/extensions, function declaration style, component structure, error handling style, naming, file organization, colocated tests, and formatting conventions not automated.

Superseded generic simplifier guidance:
- Explicit return types and React Props types are not automatically preferred.
- “Proper error handling” does not justify defensive wrappers or `try/catch` without same-path precedent.

Action: follow selected project instructions and observed local patterns, not generic external preferences.

### 10. Unclear names, obvious comments, or scattered related logic

Failure: the PR makes code harder to understand through names, comments, placement, or tiny wrappers that diverge from local domain language.

Look for renamed concepts with no behavior need, comments narrating obvious code, stale comments, related logic split without boundary value, or duplicated local logic using inconsistent names/shapes.

Action: use existing domain terms, remove obvious/stale comments, and keep related simple logic together unless consolidation reduces lines/complexity without premature helpers.

### 11. Over-compression or mixed concerns

Failure: cleanup reduces lines by making code denser, harder to debug, or less maintainable.

Look for nested ternaries, dense one-liners combining multiple concerns, functions/components that mix responsibilities, removed public/framework/contract boundaries, or branches merged despite distinct business cases.

Action: keep minimal syntax for simple cases; use explicit branches for distinct cases or side effects; preserve real boundaries.

### 12. Under-implementation masked as simplification

Failure: the PR looks smaller because required behavior, route wiring, tests, fixtures, help output, or public-surface updates are missing.

Look for new enum/route/CLI/API entries without dispatch tests, public help snapshots, focused unit tests, integration/smoke coverage, or implementation files that make the feature usable.

Action: restore the smallest project-native behavior and validation coverage before optimizing for line count. Do not classify missing feature files or tests as slop.

### 13. PR-only compatibility wrapper

Failure: the PR preserves an internal API shape that exists only in the current unmerged work by adding wrapper functions, aliases, or duplicate entrypoints.

Look for helpers named `*Only`, `legacy*`, `compat*`, aliases for newly split functions, or wrappers kept only so current PR callers need not change.

Action: update all local callers to the clearer canonical API. Keep compatibility only for published/base-branch contracts or explicit migration requirements.

### 14. Flattened result or state contract

Failure: cleanup collapses distinct runtime states into a boolean, optional, or ambiguous return shape even though callers need to distinguish success, no-op, skipped, failed, linked, changed, or included.

Look for APIs returning only `changed`, `success`, `undefined`, or broad `false` when downstream behavior or user messaging differs by state.

Action: preserve the smallest result contract that carries the states needed by callers and tests; remove only ceremonial type aliases around that contract.

### 15. Unrelated process or setup churn

Failure: the PR changes setup, contributing, CI, package-manager, or workflow documentation to solve local validation friction instead of the requested product behavior.

Look for docs about local tool installation, lockfile policy, environment setup, or validation workarounds when the feature/fix does not require those docs.

Action: remove unrelated process/documentation churn and report the validation or environment issue as a blocker. Keep docs only when the user requested docs or the product behavior has a user-facing documentation requirement.

### 16. Mis-scoped shared extraction

Failure: code either keeps parallel same-contract implementations or extracts constants/helpers without enough real reuse.

Look for a new generic mechanism beside an older same-purpose implementation, or a new public helper/type with one internal consumer and no contract-boundary need.

Action: if the abstraction is genuinely shared by existing and new behavior, migrate both paths and tests to it. If it is not shared, inline it or keep it local. Domain constants and external package specs may be extracted with fewer than three consumers when they encode a public or third-party contract.

## Allowed exceptions

An exception is valid only when evidence-backed and explicitly reported.

Allowed:
- Public API, framework, serialization, persistence, or network boundary requires the shape.
- Project instruction file or existing local pattern mandates the structure.
- Tests, callers, API docs, or business rules prove defensive behavior is expected.
- Narrow defensive parsing protects external user files, project metadata, lockfiles, manifests, generated configs, or tool output that legitimately varies, and tests cover no-op/failure states.
- Idempotent project-file mutation requires existence checks, de-duplication, or version normalization to avoid corrupting user projects.
- Helper has at least three real consumers or centralizes contract-boundary behavior.
- Removing code would change business behavior, user-visible outcome, public interface, route/CLI/help behavior, test-observable requirement, or persisted/network contract.

Invalid:
- “It is safer.”
- “It is more readable.”
- “It keeps the diff smaller.”
- “It might be useful later.”
- “This is common TypeScript style.”
- “The helper name documents intent.”
