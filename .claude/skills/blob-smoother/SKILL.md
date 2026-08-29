---
name: blob-smoother
description: Add coherency between the separately-generated blobs of a chapter JSON by running an ordered chain of OpenRouter edit calls that reconcile each blob against the ones before it, editing the file in place. Use when the user invokes "blob-smoother" or passes a chapter JSON whose blobs already have text and asks to make them flow together.
---

# blob-smoother

Smooth a chapter's blobs into one coherent narrative. A python script walks the blobs
in order and makes **synchronous** OpenRouter calls. Each call sees the chapter `outline`
plus a sliding window of consecutive passages and edits **only the last one** to flow from
and stay consistent with the passages before it. Edited text feeds forward into the next
call. Edits are written back into the file **in place**. You never edit the prose yourself.

A light pass: reconcile local conflicts and flow between adjacent blobs.

## Prerequisite input

A chapter JSON of the koschei-chapter format whose blobs already have `text` (i.e. run
through `blob-writer`) plus `mode`, `type`, and `tags`. The script also reads
`chapter.outline` and `chapter.context`.

## The sliding window

- **Blob 1 is the untouched anchor** and is never edited.
- Blob 2 is edited against blob 1 (window `[1,2]`).
- Every later blob N is edited against the previous two (window `[N-2, N-1, N]`), using their
  **already-edited** text.
- Only the last passage in each window is editable; the earlier ones are read-only reference.

## Setup (one time)

Copy `assets/.env.example` to `assets/.env` and paste your OpenRouter key, or set
`OPENROUTER_API_KEY` in the environment. `.env` is gitignored.

## The model pool

The `MODELS` array in `assets/smooth_blobs.py`. Each call picks one at random, with
replacement. The smoothing model is not recorded; the blob's `model` field is left untouched.

## Run it

From the project root (CorpLore), with Bash:

```bash
python .claude/skills/blob-smoother/assets/smooth_blobs.py <path-to-chapter.json>
```

## What the script does

- Runs cold (`temperature = 0.35`).
- Instructs each call to **prefer cutting or changing over adding**, never introduce new
  details/characters/objects/events, and never erase unique or idiosyncratic detail; fix only
  serious, otherwise-irreconcilable conflicts.
- Passes the target blob's `mode`/`type`/`tags` and preserves its form.
- **Never lets a blob grow**: a revision longer than the original is rejected and retried.
- **On failure, keeps the original text unchanged.**
- Flushes to disk after every edit.
- Prints a per-blob table and a summary listing any blobs KEPT unchanged.

## Hard rules

- **Do not edit any blob prose by hand.** All edits come from the API via the script.
- **Do not modify** `prompt`, `mode`, `type`, `tags`, `number`, `model`, or any chapter-level
  field. Only `text` changes.
- **Do not commit** any `.env` or key, and never print the key.

## Procedure

1. Confirm the input blobs have non-empty `text` (run `blob-writer` first if not) and that a
   key is reachable (`assets/.env`, blob-writer's `.env`, or the env var).
2. Run the script on the chapter file.
3. Relay the summary. If any blobs were KEPT unchanged, offer to re-run to retry just those.
4. Do not edit the file by hand.

## Final check before finishing

- [ ] Blob 1 is unchanged; every other blob is either smoothed or reported as KEPT.
- [ ] No blob's word count exceeded its original.
- [ ] Only `text` changed; no other fields, no new keys, no hand-written prose.
- [ ] The JSON still parses and keeps its original structure and formatting.
- [ ] The API key was never printed or committed.
