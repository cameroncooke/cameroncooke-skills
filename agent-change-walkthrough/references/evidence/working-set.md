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
