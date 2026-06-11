# Working Set

Examples used while editing the skill. Tuning against these is allowed.

## EX-001: Extracted categorization shown as brand-new code

- Label: negative
- Kind: false-negative
- Origin: human-verified
- Source: user feedback on a real walkthrough, 2026-06-11
- Status: working
- Expected behavior: when logic is removed from one file and equivalent logic appears in another, the walkthrough shows the removed code from its original location as Before (simplified allowed, labeled) and the new code verbatim as After, then states what is identical and what changed.
- Observed behavior: walkthrough showed only the new file's function, presenting moved logic as if written from scratch; the removed inline version was never shown.
- Skill delta: "Before/after rules for changed code" section in SKILL.md; `git show <base>:<path>` and `git log -p -S` added to evidence gathering; matching exit criteria.
- Anonymization: domain renamed from a snapshot/image-manifest system to a generic manifest; function and field names generalized; docstring rewritten. Algorithmic structure preserved exactly.

### Content

Removed from `tasks.py` (inline in a larger task function):

```python
head_by_name = {key: meta.content_hash for key, meta in head_manifest.entries.items()}
base_by_name = {key: meta.content_hash for key, meta in base_manifest.entries.items()}

declared_names = head_manifest.declared_names

matched = head_by_name.keys() & base_by_name.keys()
added = head_by_name.keys() - base_by_name.keys()

if declared_names is not None:
    declared_set = set(declared_names)
    removed = base_by_name.keys() - declared_set
    skipped = (declared_set - head_by_name.keys()) & base_by_name.keys()
elif head_manifest.selective:
    removed = set()
    skipped = base_by_name.keys() - head_by_name.keys()
else:
    removed = base_by_name.keys() - head_by_name.keys()
    skipped = set()
```

Added to new file `categorize.py`:

```python
def categorize_entries(
    head_manifest: Manifest, base_manifest: Manifest
) -> tuple[set[str], set[str], set[str], set[str]]:
    """Categorize entry names into (matched, added, removed, skipped) by selective mode.

    The base is the authoritative complete set. Only the head's selective flags drive
    classification:
      - declared_names given: removals are names in base but not in the declared set.
      - selective, no list: nothing removed; base names not uploaded are skipped.
      - full: base names not in head are removed.
    """
    head_names = set(head_manifest.entries.keys())
    base_names = set(base_manifest.entries.keys())

    matched = head_names & base_names
    added = head_names - base_names

    declared_names = head_manifest.declared_names
    if declared_names is not None:
        declared_set = set(declared_names)
        removed = base_names - declared_set
        skipped = (declared_set - head_names) & base_names
    elif head_manifest.selective:
        removed = set()
        skipped = base_names - head_names
    else:
        removed = base_names - head_names
        skipped = set()

    return matched, added, removed, skipped
```

A correct walkthrough must show both blocks as one step and call out: branch logic is mechanically
identical; the new version keys sets off entry names directly instead of content-hash dicts, gains
a signature/return contract, and a docstring codifying the business rules.

## EX-002: Single illustrative example for branchy set logic

- Label: negative
- Kind: false-negative
- Origin: human-verified
- Source: same walkthrough as [EX-001], 2026-06-11
- Status: working
- Expected behavior: for the `categorize_entries` change, one scenario per distinct outcome — full mode with a dropped name, selective mode with a not-uploaded name, declared set excluding a base name, declared set including a not-uploaded name, and a head-only addition — so each branch's output is verifiable by inspection.
- Observed behavior: a single happy-path example that exercised only one branch, proving nothing about the other arms.
- Skill delta: "Branch-complete example data" section in SKILL.md; branch-table demonstration in the output example; matching exit criterion.
- Anonymization: shares EX-001's generalized domain.

### Content

Minimum scenario set for EX-001's function (head entries, base entries, declared/selective →
matched/added/removed/skipped):

| head | base | declared / selective | matched | added | removed | skipped |
|---|---|---|---|---|---|---|
| {a} | {a, b} | — / false | {a} | {} | {b} | {} |
| {a} | {a, b} | — / true | {a} | {} | {} | {b} |
| {a} | {a, b} | [a] | {a} | {} | {b} | {} |
| {a} | {a, b} | [a, b] | {a} | {} | {} | {b} |
| {a, c} | {a} | — / false | {a} | {c} | {} | {} |

## EX-003: Explanation missing below code blocks

- Label: negative
- Kind: edge-case
- Origin: human-verified
- Source: user feedback, 2026-06-11
- Status: working
- Expected behavior: substantive logic explanation follows each code block; at most a one-sentence framing line above.
- Observed behavior: steps fronted all explanation before the snippet, leaving nothing tying the shown code back to behavior.
- Skill delta: explicit explain-below-code bullet in Step 4; matching exit criterion.
- Anonymization: pattern-level record; no code retained.

## EX-004: Large rewrite rendered as a unified diff

- Label: negative
- Kind: edge-case
- Origin: human-verified
- Source: user feedback, 2026-06-11
- Status: working
- Expected behavior: 1–2 changed lines → git-style diff block; larger changes → separate labeled Before and After blocks, each with its own Filename header.
- Observed behavior: multi-line rewrites shown either as long interleaved +/- diffs or as the new version only.
- Skill delta: size-based formatting rule in "Before/after rules for changed code".
- Anonymization: pattern-level record; no code retained.

## EX-005: Unchanged context mistakable for new work

- Label: negative
- Kind: false-positive
- Origin: human-verified
- Source: user feedback, 2026-06-11
- Status: working
- Expected behavior: every unchanged step opens with the literal note line "> Unchanged — pre-existing code shown for flow context only; nothing in this snippet was touched by this change."
- Observed behavior: only a heading tag marked unchanged steps; readers skimming code blocks took pre-existing code as part of the change.
- Skill delta: mandatory note line in Step 4 and in the output example; matching exit criterion.
- Anonymization: pattern-level record; no code retained.

## EX-006: Prose assumed reader knew the codebase

- Label: negative
- Kind: fix
- Origin: human-verified
- Source: user feedback on a real walkthrough produced by the revised skill, 2026-06-11; user supplied a corrected rewrite
- Status: working
- Expected behavior: explanations stand alone for a competent developer who has never seen the repository — project-specific terms explained at first mention, mechanisms anchored to general concepts, multi-actor behavior introduced via a numbered concrete scenario, problem stated before mechanism.
- Observed behavior: setup and step prose leaned on internal tool names, flag-framework conventions, and domain shorthand with no explanation, so the walkthrough was only readable by someone already working in the codebase.
- Skill delta: "Write for a reader new to the codebase" section in Step 4; setup paragraph contract now problem-first; two new exit criteria; output example's setup paragraph rewritten to model the style.
- Anonymization: real internal tool names, flag names, branch names, and product domain replaced with the generalized manifest/build domain used by EX-001; sentence structure of both versions preserved.

### Content

Failing prose (structure preserved, names generalized):

> A purely additive registration following the repo's Toggles convention. `api_expose=False` because
> no frontend code checks this flag — it only gates backend base-selection behavior. Rollout happens
> via the config-automator YAML, not in this repo, so merging this branch changes nothing for any
> customer until the flag is enabled.

This assumes the reader knows what the Toggles framework is, what `api_expose` controls, and what
the config-automator repo does.

User-supplied corrected style (same content, plain English):

> This branch fixes build comparisons for a common pull request setup.
>
> Sometimes a build uploads **all** entries. Other times it is **selective**, meaning it uploads
> only part of the set — for example, only entries from a certain module or platform.
>
> The problem happens when one pull request is built on top of another:
>
> 1. `main` has a full build with every entry.
> 2. PR1 has a selective build with only some entries.
> 3. PR2 is opened on top of PR1.
> 4. PR2 needs to compare against PR1's build.
>
> Before this change, the system ignored PR1's build because it was selective, so PR2 could not find
> a baseline. After this change, PR1's selective build can serve as the baseline: the system first
> rebuilds PR1's full entry set by starting from the nearest earlier full build, then applying the
> selective data on top.
>
> This is backend-only, behind the feature flag `organizations:selective-base-builds` — flags are
> switched on per customer from a separate configuration repo, so merging this changes nothing by
> itself. No frontend changes and no database migration.

The traits that make the rewrite work: problem first, numbered concrete scenario before mechanism,
key terms bolded and defined inline, the flag anchored to the general feature-flag concept, short
sentences.
