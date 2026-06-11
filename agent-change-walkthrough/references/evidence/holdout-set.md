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

## HX-003: Jargon-saturated flag rollout must read as plain English

- Label: negative
- Kind: edge-case
- Origin: synthetic
- Source: authored 2026-06-11 to exercise the audience-calibration rules on a fixture whose repo
  conventions invite insider shorthand; domain deliberately differs from EX-006
- Status: holdout
- Expected behavior: see pass criteria below.
- Observed behavior: n/a until run.
- Skill delta: n/a — validation only.
- Anonymization: fully synthetic, including the internal framework names.

### Content

The fixture repo has its own internal conventions that a lazy walkthrough would name without
explanation: feature flags are registered through an in-house framework called **Switchboard**;
registrations carry an `expose_ui` field; flags are turned on per customer from a separate
repository called **config-deployer**, not from this repo.

The change: email digest sends gain a quiet-hours deferral, gated behind a new flag.

Base state, `flags/registry.py` (existing registrations, unchanged):

```python
register(Flag("orgs:digest-batching", expose_ui=True))
register(Flag("orgs:digest-reply-threading", expose_ui=False))
```

Working-tree change 1 — new registration appended in `flags/registry.py`:

```python
register(Flag("orgs:digest-quiet-hours", expose_ui=False))
```

Working-tree change 2 — `digests/scheduler.py`, the send loop:

Before:

```python
for digest in due_digests:
    send_digest(digest)
```

After:

```python
for digest in due_digests:
    org = digest.organization
    if flag_enabled("orgs:digest-quiet-hours", org) and in_quiet_hours(org, now):
        defer_to_next_window(digest, org)
    else:
        send_digest(digest)
```

with `in_quiet_hours` and `defer_to_next_window` added as small new helpers reading
`org.settings.quiet_hours` (an existing stored setting).

Staging note: give `flags/registry.py` a short module docstring stating the repo convention
("Flags are registered here via Switchboard; `expose_ui` controls frontend visibility; flags are
enabled per customer from the config-deployer repo"). The information must be discoverable in the
repo — the test is whether the walkthrough translates it into plain English, not whether it can
invent it.

Pass criteria (run with no extra audience instructions — the skill alone must produce these):

1. The setup paragraph states the problem in plain English (digests currently send at any hour,
   including the middle of the night for the recipient's organization) before naming any internal
   tool, flag, or file.
2. Switchboard, `expose_ui`, and config-deployer are each explained at first mention and anchored
   to the general concept they implement (feature-flag framework; whether a flag is visible to
   frontend code; per-customer rollout from a separate configuration repo — so merging activates
   nothing by itself).
3. The flag/setting/scheduler interaction is introduced as a numbered concrete scenario (e.g.
   1. an org sets quiet hours 22:00–07:00, 2. a digest comes due at 23:00, 3. the flag is on, so
   it is deferred to 07:00; flag off → sends immediately) before any abstract description, and the
   example data covers the distinct outcomes: flag off; flag on outside quiet hours; flag on
   inside quiet hours.
4. No step relies on an identifier name alone to carry meaning — a developer who has never seen
   this repository can follow every step without asking what a term refers to.
