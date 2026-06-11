# Holdout Set

Reserved for validating the skill after edits. Do not tune SKILL.md wording directly against these
records; move one into `working-set.md` first if it must drive an edit.

To validate: construct the described change in a scratch repo (or present it as a diff), run the
skill, and check the output against each record's pass criteria.

## HX-001: Moved validation helper with a tightened boundary

- Label: negative
- Kind: regression
- Origin: synthetic
- Source: authored 2026-06-11 to exercise the moved-code rules on a non-set-logic, non-Python case
- Status: holdout
- Expected behavior: see pass criteria below.
- Observed behavior: PASS on 2026-06-11 against the same-day SKILL.md revision, run by a fresh agent blind to these criteria in a staged scratch repo. All four criteria met; the `>` → `>=` change was flagged as a likely accidental off-by-one with a below/at/above-limit example table. Minor deviation: the Before block elided lines with `// ...` but was not labeled `Before (simplified)`.
- Skill delta: n/a — validation only.
- Anonymization: fully synthetic.

### Content

The change: an inline guard in an HTTP route handler is extracted to a shared util, and during the
move the boundary condition tightens from `>` to `>=`.

Removed from `routes/upload.ts`:

```ts
if (file.sizeBytes > MAX_UPLOAD_BYTES) {
  return reject("too_large")
}
```

Added to new file `lib/limits.ts`:

```ts
export function exceedsUploadLimit(sizeBytes: number): boolean {
  return sizeBytes >= MAX_UPLOAD_BYTES
}
```

with the route handler now calling `exceedsUploadLimit(file.sizeBytes)`.

Pass criteria:

1. One step shows both locations — Before from `routes/upload.ts`, After from `lib/limits.ts` —
   never the new util alone.
2. The walkthrough explicitly calls out the `>` → `>=` change as a behavior change (a file of
   exactly `MAX_UPLOAD_BYTES` is now rejected), not as a mechanical move.
3. Example data covers the three distinct inputs: below limit, exactly at limit (the changed
   outcome), above limit.
4. The unchanged route-handler plumbing around the call site, if shown, opens with the literal
   unchanged note line.

## HX-002: Config precedence merge with branch-bearing fallbacks

- Label: negative
- Kind: edge-case
- Origin: synthetic
- Source: authored 2026-06-11 to exercise branch-complete examples on dict-merge precedence logic
- Status: holdout
- Expected behavior: see pass criteria below.
- Observed behavior: n/a until run.
- Skill delta: n/a — validation only.
- Anonymization: fully synthetic.

### Content

The change: a new function replaces a naive `{...defaults, ...fileConfig}` spread.

New code in `config/resolve.ts`:

```ts
export function resolveConfig(
  defaults: Config,
  fileConfig: Partial<Config>,
  envOverrides: Partial<Config>,
  strict: boolean,
): Config {
  const merged = { ...defaults, ...fileConfig, ...envOverrides }
  if (strict) {
    const unknown = Object.keys(fileConfig).filter((k) => !(k in defaults))
    if (unknown.length > 0) throw new ConfigError(unknown)
  }
  return merged
}
```

Pass criteria:

1. The old one-line spread appears as Before (diff block acceptable — the prior code is 1 line),
   and the walkthrough does not present `resolveConfig` as having no predecessor.
2. Example data enumerates the precedence and strictness outcomes as distinct scenarios, minimum:
   key only in defaults; key in defaults+file; key in all three (env wins); unknown key with
   `strict: false` (passes through); unknown key with `strict: true` (throws); empty
   `envOverrides`.
3. Scenarios are presented as a table or labeled list with concrete values, and the explanation of
   precedence order sits below the code block, not only above it.
