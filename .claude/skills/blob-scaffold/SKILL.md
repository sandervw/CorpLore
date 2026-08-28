---
name: blob-scaffold
description: Turn a chapter (title, outline text, word target, optional type) into a JSON chapter object with an empty blobs array sized to the word target. Use when the user mentions "blob-scaffold" or asks to scaffold a chapter/blobs into JSON.
---

Produce a single JSON chapter object from the user's input. The input is a chapter with an outline of text beneath it, a word target, and an optional type.

## Output shape

```json
{
  "chapter": {
    "number": <int>,
    "title": "<string>",
    "wordcount": <word target, int>,
    "type": "<string, or empty string if none given>",
    "outline": "<full outline text, verbatim>",
    "context": [ ... ],
    "blobs": [ ... ]
  }
}
```

Each blob:

```json
{ "number": <1..N>, "prompt": "", "mode": "", "type": "", "tags": [], "text": "" }
```

`context` is an array of exactly 5 strings:

```json
[
  "[fact 1]",
  "[fact 2]",
  "[fact 3]",
  "[fact 4]",
  "[fact 5]"
]
```

## Rules

- **Blob count** = `ceil(word_target / 200)`. E.g. 3000 -> 15, 2200 -> 11, 1116 -> 6.
- Blobs are numbered 1..N; every blob field is empty (`prompt` `""`, `mode` `""`, `type` `""`, `tags` `[]`, `text` `""`). Only `number` varies.
- `outline` holds the full text under the chapter, verbatim. Preserve `*italics*`, `(*subtext*)`, quotes, and hyphens exactly; encode line breaks as `\n`.
- `type` is the chapter type string if given (e.g. `"Violence - fights, kills, torture"`), else `""`.
- `context` = the 5 most important facts about the story/scene that any LLM MUST know before working on any part of it. These are story-level, not chapter-level, so the same 5 facts apply to every chapter of the same story. Draw them from the outline and any story materials in context. Examples: `"The main character is Gneiss Rong."`, `"The story is told in first-person."`
- Each context fact is a complete English sentence of 10 words or less. Exactly 5, no more, no fewer.
- Never invent or fill blob contents; this only scaffolds the empty structure.
- No em-dashes anywhere.

## Steps

1. Parse title, number, word target, optional type, and outline text from the input.
2. Compute N = ceil(word_target / 200).
3. Derive the 5 context facts (each a complete sentence, 10 words or less) from the outline and story materials.
4. Write the JSON to the file/location the user names, or ask if unspecified. Pretty-print with 2-space indent.
