# Slop Swatter Code Pattern Examples

Examples for applying `code-pattern-catalogue.md`. Use these examples to classify findings; still require full-file project evidence before making a claim.

## Existing project pattern ignored

Failing shape:

```ts
const result = await safeExecute(() => client.projects.create(input));
```

If nearby full files call `client.projects.create(input)` directly and rely on the shared API error layer, remove the wrapper and reuse the direct API pattern.

## Similar-but-different local variant

Failing shapes:

```ts
const displayName = `${user.name} <${user.email}>`;
const userLabel = `${member.fullName} (${member.emailAddress})`;
```

If these represent the same domain concept, align naming and object shape with the existing domain pattern. Do not introduce a helper unless there are three or more real consumers or a contract boundary requires it.

## Defensive programming without same-path precedent

Failing shape:

```ts
const region = account.region ?? "us-east-1";
```

If same-path code treats missing `region` as invalid, the fallback hides an invariant violation. Remove it or use the project-native error/invariant pattern.

Also suspect:

```ts
try {
  return await loadProject(slug);
} catch {
  return null;
}
```

Keep only when same-path code catches the same failure mode and tests/callers/docs prove null is an expected business outcome.

## Premature helper or DRY abstraction

Failing shape:

```ts
function isEnabled(flag: boolean) {
  return flag === true;
}

if (isEnabled(settings.enabled)) {
  start();
}
```

Preferred:

```ts
if (settings.enabled) {
  start();
}
```

Failing one-consumer helper:

```ts
function buildUserLabel(user: User) {
  return `${user.name} (${user.email})`;
}

const label = buildUserLabel(user);
```

Preferred until there are three real consumers or meaningful contract complexity:

```ts
const label = `${user.name} (${user.email})`;
```

## Boilerplate TypeScript type surface

Failing local ceremony:

```ts
type Payload = {
  id: string;
  name: string;
};

const payload: Payload = {id, name};
send(payload);
```

Preferred when there is no exported, JSON, persistence, network, or inference boundary:

```ts
send({id, name});
```

Keep explicit types for public APIs, JSON encode/decode boundaries, persistence/network payloads, large shared domain objects, non-obvious generics, or project-mandated conventions.

## Verbose branch or clever syntax

Failing verbose boolean:

```ts
let shouldShow = false;
if (count === limit) {
  shouldShow = true;
} else {
  shouldShow = false;
}
```

Preferred:

```ts
const shouldShow = count === limit;
```

Acceptable simple ternary:

```ts
const label = isSaving ? "Saving" : "Save";
```

Failing nested ternary:

```ts
const label = isSaving ? "Saving" : hasError ? "Retry" : "Save";
```

Use explicit branches when there are multiple distinct cases or side effects.

## Wholesale rewrite instead of surgical cleanup

Failing signals:

- renamed concepts with no behavior need
- new framework/layer boundary introduced for one PR
- rewritten tests that bless implementation churn instead of preserving behavior
- broad cleanup inside a focused feature or fix

Preferred response: restore the smallest implementation surface that preserves intended behavior. Split, revert, or remove unrelated churn.

## Net growth in slop lines or complexity

Failing cleanup:

```text
baseline: +120 -20, helper count 1
final:    +150 -30, helper count 3
```

Even if code feels cleaner, slop-swatter did not complete for a cleanup-only workstream. Steer implementers to reduce slop-specific changed-line footprint and the selected complexity proxy, or report blocked if further reduction changes core behavior.

Allowed restoration shape:

```text
baseline after over-pruned cleanup: +80 -10, missing route tests
final:                          +120 -10, route/help tests restored
slop proxy: wrapper count 2 -> 0, public-surface coverage missing -> covered
```

A larger total diff is acceptable only when the added code/tests restore behavior or public contracts required by the behavior model.

## Codified project standard bypassed

Failing signal: the selected instruction file says imports must stay at top, but the PR adds inline imports.

Preferred response: follow selected project instructions and local full-file pattern evidence. Do not apply generic TypeScript/Sentry preferences when project evidence says otherwise.

## Unclear names, obvious comments, scattered logic

Failing shape:

```ts
// Check if the user is active
const userActivityEvaluationResult = user.status === "active";
```

Preferred when it matches local domain language:

```ts
const isActive = user.status === "active";
```

Remove comments that narrate obvious code. Keep comments only for non-obvious constraints, business rules, or external-contract reasons.

## Under-implementation masked as simplification

Failing shape:

```text
- adds a new integration enum value
- adds a switch case
- omits the wizard implementation, help snapshot, routing test, and setup smoke test
```

Preferred response: restore the smallest implementation and focused tests that make the new public surface usable. Do not delete feature files or tests only because they increase the line count.

## PR-only compatibility wrapper

Failing shape:

```ts
export async function lookupProjectOnly(input: Input) {
  const { project } = await lookupProjectAndTarget(input);
  return project;
}

export async function lookupProjectAndTarget(input: Input) {
  // target selection mixed into project lookup
}
```

Preferred when all callers are inside the current PR:

```ts
export async function lookupProject(input: Input) {
  return new Project(input.path);
}

export async function selectTarget(project: Project) {
  return choose(project.getTargets());
}
```

Update current callers to the clearer API. Keep wrappers only for published/base-branch contracts or explicit migrations.

## Flattened result or state contract

Failing shape:

```ts
return { changed: false };
```

If callers must distinguish already-linked from unable-to-link, preserve that state:

```ts
return { changed: false, linked: false };
```

Remove ceremonial exported type aliases around the result when inference is enough, but keep fields that drive user messaging or follow-up behavior.

## Unrelated process or setup churn

Failing signal: a product feature PR adds CONTRIBUTING instructions about local package-manager setup because validation was difficult locally.

Preferred response: remove the documentation churn and report the local validation issue as a blocker unless the user asked for setup docs or the product behavior requires user-facing documentation.

## Mis-scoped shared extraction

Failing shape: a new generic package-linking helper is added for one feature, but the existing package-linking path keeps its older parallel implementation.

Preferred response: either migrate both paths and preserve the old behavior with tests, or keep the new helper local until real reuse exists.

## Over-compression or mixed concerns

Failing shape:

```ts
const label = isSaving ? "Saving" : hasError ? retryLabel(error) : canSubmit ? "Save" : "Disabled";
```

Preferred:

```ts
if (isSaving) {
  return "Saving";
}

if (hasError) {
  return retryLabel(error);
}

return canSubmit ? "Save" : "Disabled";
```

Do not combine data loading, branching, transformation, and side effects into dense one-liners to satisfy the line-reduction metric.
