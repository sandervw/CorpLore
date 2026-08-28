---
name: blob-metadata
description: Assign organizing metadata (mode, type, and tags) to every blob in a scaffolded chapter JSON so the blobs form a coherent, writable narrative sequence. Use when the user invokes "blob-metadata" or passes a chapter JSON and asks to fill in blob mode/type/tags metadata. Only fills metadata, never prompt or text.
---

# blob-metadata

Assign metadata to each blob in a chapter JSON so the blobs form a coherent, writable sequence that tracks the chapter `outline` and `type`. You fill only three things per blob: the `mode` field, the `type` field, and the `tags` array (which ends holding exactly 3 items: 1 detail + 2 tags). You never touch `prompt`, `text`, `number`, or any chapter-level field, and you never write prose.

## Input

A single chapter JSON file, passed by the user (e.g. `Stories/.../some-chapter.json`). Its shape:

```
chapter.outline      -> the narrative you must make the blobs track
chapter.type         -> the chapter's dominant mode of action
chapter.blobs[]      -> each has: number, prompt, mode (""), type (""), tags ([]), text
```

## Output

The **same input file, edited in place**. Only `mode`, `type`, and `tags` change on each blob. No copy to `Output/`.

## The data source: pick.py

All metadata values come from `blob-data.json` via `pick.py`. **Never read `blob-data.json` directly** while using this skill; only ever reach it through `pick.py`. Run from the project root (CorpLore) with Bash:

```bash
python .claude/skills/blob-metadata/assets/pick.py <array_name> [number]
```

- `modes`  -> returns all 7 modes (no number).
- `types 20`   -> returns 20 random types (fresh sample per call).
- `details 2`  -> returns 2 random grounding-detail labels.
- `tags 20`    -> returns 20 random tags (fresh sample per call).

Ignore the `functions` and `situations` arrays in `blob-data.json`.

## Hard rules

- **Do not read any other files** beyond the input chapter file (and never `blob-data.json` directly).
- **Do not add any field, key, or extra text to any file, ever.** Fill only `mode`, `type`, `tags`.
- **Do not modify** `prompt`, `text`, `number`, `chapter.outline`, `chapter.type`, `chapter.context`, or any other existing content.
- **Every `mode`+`type` pair must be unique** across all blobs. No two blobs may share the same combination.
- **Any single tag value may appear in at most 2 blobs** across the whole chapter.
- Each blob's `tags` array ends with **exactly 3 items**: `[1 detail, 2 tags]`, in that order.

## Goals (optimize while satisfying the hard rules)

- **Coherence first.** The sequence of blobs, read in order by `number`, must form a coherent narrative path faithful to `chapter.outline` and `chapter.type`. Every mode/type/detail/tag choice should fit that blob's `prompt` and its place in the arc.
- **Maximize distinct modes.** Use as many of the 7 modes as you can (aim to use all 7).
- **Maximize distinct types.** Use as many different types as possible; aim for a distinct type per blob.
- **Favor detail variety.** Prefer using as many distinct details as possible; avoid reusing any one detail more than twice.

## Re-rolls

Each `types`/`details`/`tags` call returns a fresh random sample. If a blob's sample contains nothing that fits the blob and satisfies the rules (unique pair, tag-reuse cap, good fit), **re-run `pick.py` for that blob** until it does. Re-rolls apply only to the current, not-yet-committed blob.

## Commit as you go (no takebacks)

This skill is **forward-only**: you make each decision once, write it into the chapter file the moment you make it, and never reopen it.

- **Persist immediately.** The instant you choose a blob's `mode`, `type`, detail, or tags, write that value into the file. Do not accumulate pending decisions to save all at once at the end.
- **Committed means frozen.** Any value already in the file is final. You may not revise an earlier blob's `mode`, `type`, or `tags`; later context never reopens an earlier decision.
- **Adapt only the blob you are on.** Satisfy every constraint (unique `mode`+`type` pair, the 2-blob tag cap) by shaping the current blob against what is already frozen. If the current blob cannot satisfy a hard rule, re-roll the current blob; leave committed blobs untouched.
- **No look-ahead.** Pull a blob's `types`/`details`/`tags` sample only once you have reached that blob and are ready to decide it. Never batch-pull samples for many blobs at once.

Modes are assigned up front in one pass (step 2); once written they freeze like everything else.

## Procedure

Work strictly forward, in blob `number` order, writing each decision into the file the moment you make it (see **Commit as you go (no takebacks)** above).

1. **Read the input** chapter file. Absorb `chapter.outline`, `chapter.type`, and each blob's `number` + `prompt`. Read nothing else.

2. **Modes.** Run `pick.py modes` once (returns all 7). Assign each blob the `mode` that best fits what its `prompt` is doing. Spread modes to cover as many of the 7 as the narrative allows, and set up for unique `mode`+`type` pairs. Write every blob's `mode` into the file now, in a single pass. From this point the modes are frozen.

3. **Types.** Handle the blobs strictly one at a time in `number` order. **Do not sample more than one blob at a time.** Only once you reach a blob, run `pick.py types 20` for it; from that single sample pick the 1 `type` that best fits the blob (its prompt, its mode, the outline), keeps its `mode`+`type` pair unique against every pair already frozen in the file, and increases type variety; then **write that `type` into the file before you touch the next blob.** Re-roll (re-run `pick.py types 20`) only for the current blob if its sample offers nothing suitable. Never pre-pull a later blob's sample, and never revise a `type` you have already written.

4. **Validate (confirmation only).** Re-read the file and confirm: every `mode`+`type` pair is unique; modes and types are as varied as feasible; each assignment fits its blob and the chapter `type`; and the blobs in `number` order read as one coherent path through `outline`. Do not rewrite a frozen `mode` or `type`. If a violation appears, flag it to the user and leave the frozen decision as written.

5. **Details.** Again strictly one blob at a time in `number` order. **Do not sample more than one blob at a time.** Only at the current blob, run `pick.py details 2`, append the better-fitting of the 2 details as the first item of that blob's `tags`, and **write it into the file before moving on.** Favor detail variety; re-roll the current blob if neither fits or both would push a detail past two uses. A written detail is frozen.

6. **Tags.** Again strictly one blob at a time in `number` order. **Do not sample more than one blob at a time.** Only at the current blob, run `pick.py tags 20`, append 2 tags that fit its mode, type, prompt, and the outline and keep every tag value within the cap (**no single tag value in more than 2 blobs total**) against what is already frozen, and **write them into the file before moving on.** Re-roll the current blob if its sample lacks 2 usable, non-cap-violating, fitting tags. Each blob's `tags` now reads `[detail, tag, tag]` (3 items); once written they are frozen.

7. **Confirm the file.** There is no final save-all step. Each write must have preserved the existing JSON structure, key order, 2-space indentation, and trailing newline, and changed only `mode`, `type`, `tags`, adding no new fields and no other text. Do a final read to confirm that; make no further changes beyond correcting your own formatting slips.

## Final check before finishing

- [ ] Every blob has a non-empty `mode` and `type`, and a `tags` array of exactly 3 items (`[detail, tag, tag]`).
- [ ] All `mode`+`type` pairs are unique.
- [ ] No tag value appears in more than 2 blobs.
- [ ] Modes and types are as varied as the narrative allows.
- [ ] Read in `number` order, the blobs track `chapter.outline` and `chapter.type`.
- [ ] Types, details, and tags were each chosen and written one blob at a time, in `number` order, and no committed value was revised after it was written.
- [ ] Only `mode`, `type`, `tags` changed; no fields added; no prose written.
