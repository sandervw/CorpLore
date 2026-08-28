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

`blob-data.json` also contains `functions` and `situations` arrays. **This skill does not use them.** Ignore them.

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
- **Maximize distinct types.** Use as many different types as possible (with 15-ish blobs and unique pairs required, aim for a distinct type per blob).
- **Favor detail variety.** Prefer using as many distinct details as possible; avoid reusing any one detail more than twice.

## Re-rolls

Each `types`/`details`/`tags` call returns a fresh random sample. If a blob's sample contains nothing that fits the blob and satisfies the rules (unique pair, tag-reuse cap, good fit), **re-run `pick.py` for that blob** until it does.

## Procedure

Work one blob at a time where noted, in blob `number` order.

1. **Read the input** chapter file. Absorb `chapter.outline`, `chapter.type`, and each blob's `number` + `prompt`. Read nothing else.

2. **Modes.** Run `pick.py modes` once (returns all 7). Assign each blob the `mode` that best fits what its `prompt` is doing (e.g. a fight beat -> `action`; a monologue -> `dialogue`; grief/reflection -> `interiority`; the opal descent -> `description`; a warning made real -> `exposition`; a scene-to-scene bridge -> `connective tissue`; a framed/listed artifact -> `documents & frames`). Spread modes to cover as many of the 7 as the narrative allows, and set up for unique `mode`+`type` pairs. Write each blob's `mode`.

3. **Types.** For each blob, one at a time, run `pick.py types 20`. From that blob's 20-item sample, pick the 1 `type` that best fits the blob (its prompt, its mode, the outline), keeps every `mode`+`type` pair unique, and increases type variety. Re-roll if the sample offers nothing suitable. Write each blob's `type`.

4. **Validate.** Confirm: every `mode`+`type` pair is unique; modes and types are as varied as feasible; each assignment fits the blob and the chapter `type`; and the blobs in order still read as one coherent path through `outline`. Fix violations by re-rolling types or reassigning modes.

5. **Details.** For each blob, one at a time, run `pick.py details 2`. Append the better-fitting of the 2 details to that blob's `tags` array (as the first item). Favor detail variety; if neither fits or both would push a detail past two uses, re-roll.

6. **Tags.** For each blob, one at a time, run `pick.py tags 20`. Append 2 tags that fit the blob's mode, type, prompt, and the outline. Enforce the cap: **no single tag value in more than 2 blobs total.** Re-roll if the sample lacks 2 usable, non-cap-violating, fitting tags. Each blob's `tags` now reads `[detail, tag, tag]` (3 items).

7. **Write in place.** Save the updated chapter JSON to the same path. Change only `mode`, `type`, `tags`. Preserve the existing JSON structure, key order, 2-space indentation, and trailing newline. Add no new fields and no other text.

## Final check before finishing

- [ ] Every blob has a non-empty `mode` and `type`, and a `tags` array of exactly 3 items (`[detail, tag, tag]`).
- [ ] All `mode`+`type` pairs are unique.
- [ ] No tag value appears in more than 2 blobs.
- [ ] Modes and types are as varied as the narrative allows.
- [ ] Read in `number` order, the blobs track `chapter.outline` and `chapter.type`.
- [ ] Only `mode`, `type`, `tags` changed; no fields added; no prose written.
