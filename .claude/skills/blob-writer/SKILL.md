---
name: blob-writer
description: Draft the prose for every blob in a fully-scaffolded chapter JSON by firing one parallel OpenRouter API call per blob, each on a randomly chosen model, and writing the returned text plus its model back into the file in place. Use when the user invokes "blob-writer" or passes a chapter JSON whose blobs have prompts/metadata and asks to generate the blob text.
---

# blob-writer

Fill each blob's `text` and `model` in a chapter JSON. A python script makes N parallel
OpenRouter calls (N = number of blobs to write), one per blob, each on a model drawn at
random from a fixed pool. Each call returns the prose for that blob; the script writes
`text` and the chosen `model` back into the file **in place**. You never write the prose
yourself.

## Prerequisite input

A chapter JSON of the koschei-chapter format, already run through `blob-scaffold`,
`blob-plotter`, and `blob-metadata`, so every blob has a filled `prompt`, `mode`, `type`,
and `tags`, with `model` and `text` still empty. The script also reads `chapter.context`.

## Setup (one time)

1. Get an OpenRouter key at https://openrouter.ai/keys.
2. Copy `assets/.env.example` to `assets/.env` and paste the key into `OPENROUTER_API_KEY`.
   `.env` is gitignored. An `OPENROUTER_API_KEY` set in the environment takes precedence.

## The model pool

Defined as the `MODELS` array in `assets/write_blobs.py`. Each blob's call picks one at
random, with replacement. Edit that array to reseed. Current pool:

- `nvidia/nemotron-3-ultra-550b-a55b`
- `anthropic/claude-sonnet-4.6`
- `openai/o3`
- `thinkingmachines/inkling`

## Run it

From the project root (CorpLore), with Bash:

```bash
python .claude/skills/blob-writer/assets/write_blobs.py <path-to-chapter.json>
```

- Add `--only-empty` to write only blobs whose `text` is still empty (retry failed blobs).

## What the script does

- Builds a prompt per blob: `chapter.context` and the blob's `mode`/`type`/`tags` become a
  system message; the blob's `prompt` becomes the user message. Every call is instructed to
  stay **under 200 words** and to output prose only.
- Fires all calls in parallel (one thread per blob).
- Retries a failing call up to 3 times (rerolling the model each attempt) with backoff.
- Writes `text` + `model` into each blob on success; leaves both empty on persistent
  failure. Preserves the JSON structure, key order, 2-space indent, and trailing newline.
- Prints a summary: per blob its number, word count, status, and model; then a total and
  the list of any FAILED blob numbers.

## Hard rules

- **Do not write or edit any blob prose by hand.** All `text` comes from the API via the
  script. Your job is to run the script and report the summary.
- **Do not modify** `prompt`, `mode`, `type`, `tags`, `number`, or any chapter-level field.
- **Do not commit** `assets/.env` or the API key, and never print the key.

## Procedure

1. Confirm the input file's blobs have filled `prompt`/`mode`/`type`/`tags` (run the earlier
   blob skills first if not) and that `assets/.env` exists (or the env var is set).
2. Run the script on the chapter file.
3. Relay the summary to the user. If any blobs FAILED, offer to re-run with `--only-empty`.
4. Do not edit the file by hand.

## Final check before finishing

- [ ] Every intended blob has a non-empty `text` and a `model` from the pool (or is reported
      as FAILED).
- [ ] Only `text` and `model` changed; no other fields, no new keys, no hand-written prose.
- [ ] The JSON still parses and keeps its original structure and formatting.
- [ ] The API key was never printed or committed.
