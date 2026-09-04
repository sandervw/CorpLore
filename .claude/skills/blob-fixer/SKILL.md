---
name: blob-fixer
description: Align every blob's written prose back to the chapter outline via a single OpenRouter API call that returns the same {number, text} array with minimal surgical corrections, then writes it back into the chapter JSON in place. Use when the user invokes "blob-fixer" or passes a written chapter JSON and asks to fix continuity against the outline.
---
# blob-fixer

Minimally correct a chapter's blob prose so it agrees with its outline. A python
script makes ONE OpenRouter call — outline, context, and an array of
`{number, text}` objects go in; the same array with targeted fixes comes out.
The script writes the results back into the file **in place**. You never edit
the prose yourself.

## Prerequisite input

A chapter JSON of the koschei-chapter format whose blobs all have non-empty
`text` (i.e. already run through `blob-writer`). The script reads
`chapter.outline`, `chapter.context`, and every blob's `number` and `text`.

## Setup (one time)

1. Get an OpenRouter key at https://openrouter.ai/keys.
2. Copy `assets/.env.example` to `assets/.env` and paste the key into
   `OPENROUTER_API_KEY`. `.env` is gitignored. An `OPENROUTER_API_KEY` set in
   the environment takes precedence.

## The model

A single fixed model, set as `MODEL` in `assets/fix_blobs.py`:

- `qwen/qwen3.8-2.4t-a95b`

## Run it

From the project root (CorpLore), with Bash:

```bash
python .claude/skills/blob-fixer/assets/fix_blobs.py <path-to-chapter.json>
```

## What the script does

- Sends one request: system message = the minimal-correction editing brief;
  user message = `chapter.outline`, `chapter.context`, and the
  `{number, text}` array as JSON.
- The brief forbids the model from changing delivery form, rewriting sections,
  erasing unique words or elements, or adding anything new; it must return
  ONLY the corrected JSON array, same length, same numbers.
- Retries up to 3 times on HTTP errors or unparseable/mismatched replies.
  On persistent failure the file is left **untouched**.
- Validates the reply before writing: must parse as a JSON array, same length,
  same blob numbers, every `text` a non-empty string.
- Writes the corrected `text` back into each blob; preserves JSON structure,
  key order, 2-space indent, and trailing newline. No `.bak` — rely on git.
- Prints a summary: per blob old/new word counts and same/edited status.

## Hard rules

- **Do not edit any blob prose by hand.** All corrections come from the API
  via the script. Your job is to run the script and report the summary.
- **Do not modify** `outline`, `context`, `prompt`, `mode`, `type`, `tags`,
  `number`, or any other field — only `text` changes.
- **Do not commit** `assets/.env` or the API key, and never print the key.

## Procedure

1. Confirm every blob has non-empty `text` (run `blob-writer` first if not)
   and that `assets/.env` exists (or the env var is set).
2. Run the script on the chapter file.
3. Relay the summary to the user (which blobs were edited, word-count deltas).
4. Do not edit the file by hand.

## Final check before finishing

- [ ] The script reported success; on failure the file is unchanged and the
      error is relayed to the user.
- [ ] Only `text` fields changed; no other fields, no new keys.
- [ ] The JSON still parses and keeps its original structure and formatting.
- [ ] The API key was never printed or committed.
