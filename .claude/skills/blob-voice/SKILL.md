---
name: blob-voice
description: Revise chapter JSON blob text fields into a specific character voice using parallel OpenRouter API calls in 3-blob batches, overwriting in place. Use when the user requests "blob-voice" or asks to apply a voice revision across chapter blobs.
---

# blob-voice

Revise the `text` fields of all blobs in a chapter JSON to embody a chosen
character voice. Runs parallel OpenRouter calls against `anthropic/claude-opus-5`
in batches of up to 3 blobs, then writes the updated `text` back into the file
**in place** (no backup files, no separate copies).

## Prerequisite input

A chapter JSON conforming to the koschei-chapter schema where all blobs have
populated `text`. Supported voices from `.claude/skills/voice-revision/`:
- `gneiss` (dynamic generator per batch)
- `necromancer` (dynamic generator per batch)
- `freeman`
- `paladin`
- `thorogood`
- `rogue`

## Setup (one time)

Ensure `OPENROUTER_API_KEY` is present in the environment or inside
`.claude/skills/blob-voice/assets/.env` (copied from sibling skill assets).

## The model

Fixed model: `anthropic/claude-opus-5`.

## Run it

From the repository root (CorpLore), execute:

```bash
python .claude/skills/blob-voice/assets/voice_blobs.py <path-to-chapter.json> <voice-type>
```

Example:
```bash
python .claude/skills/blob-voice/assets/voice_blobs.py Stories/Obelisk/current-work/koschei-chapter-6.json gneiss
```

## What the script does

1. Batches the blobs into slices of 3 (or fewer for the tail).
2. Spawns parallel worker threads to dispatch each batch simultaneously.
3. For dynamic voices (`gneiss`, `necromancer`), generates a freshly sampled
   voice guide for each API request to ensure rich stylistic variety. For static
   voices, reads the corresponding reference guide directly.
4. Prompts `claude-opus-5` strictly to revise only cadence, voice, and syntax
   while strictly preserving story beats, actions, and delivery forms.
5. Validates the JSON array structure and numbers from each batch before any
   changes are committed.
6. Overwrites the target chapter JSON **in-place** with no backups.
7. Prints a per-blob word count comparison and modification status.

## Hard rules

- **Do not edit blob prose by hand.** The script manages API calls and validation.
- **Do not touch other fields** (`number`, `prompt`, `mode`, `tags`, `type`, etc.).
- **Overwrite in-place**; never create `.bak` or alternate output files.
- **Never print or commit API keys.**
