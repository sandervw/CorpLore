---
name: blob-plotter
description: Break a scaffolded chapter's outline into one writing prompt per blob, filling each blob's prompt field in the JSON. Use when the user mentions "blob-plotter" or asks to plot/prompt blobs from a chapter outline.
---

The user invokes this skill with a scaffolded chapter JSON file (the output of blob-scaffold) as input. That file has a full `outline` and an array of N blobs whose fields are empty. Fill the `prompt` field of every blob, then overwrite the same file.

## What a prompt is

Each `prompt` is a writing instruction handed to an LLM to write that one chunk of prose, e.g. `"Write a chunk of prose about..."`. It carries only what that specific chunk needs. It is not a summary, not context, and not a plan.

## Rules

- **Fill only `prompt`.** Write one prompt into every existing blob, in order (1..N). Never add, remove, or renumber blobs. Never touch `mode`, `type`, `tags`, `text`, or any field outside `blobs`; leave them exactly as they are.
- **Cover the whole outline, in order.** The N prompts together walk the `outline` from its first beat to its last with no gaps and no reordering of events. Blob 1 opens the chapter, blob N closes it. Divide the outline's events as evenly as the beats allow.
- **Local only.** A prompt gives just the material for its own chunk. No broader story context, no recap of earlier blobs, no setup for later ones.
- **Length.** 40 words or fewer. Complete English sentence(s).
- **Vary the phrasing.** Do not open every prompt the same way. Rotate the verb and framing ("Write a chunk about...", "Describe...", "Render the moment when...", "Show...", "Narrate...").
- **No meta.** No POV or person, no dialogue/format directions, no tone labels, no word counts. Those are supplied elsewhere.
- **Names as-is.** Use proper names exactly as the outline gives them (Gneiss, Joiyuss, Phansy, the mulchers, the butler). The chapter's `context` array carries global identity; do not re-explain it.
- No em-dashes anywhere; use spaced hyphens, commas, or semicolons.

## Steps

1. Read the JSON file the user passed. Note N (the blob count) and read the full `outline`.
2. Segment the outline into N sequential spans that cover it start to finish.
3. Write one prompt (40 words or fewer, worded distinctly) into each blob's `prompt` field, in order. Leave every other field untouched.
4. Overwrite the same file in place, pretty-printed with 2-space indent. Report the path.
