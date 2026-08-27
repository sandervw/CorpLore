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
    "blobs": [ ... ]
  }
}
```

Each blob:

```json
{ "number": <1..N>, "prompt": "", "type": "", "tags": [], "text": "" }
```

## Rules

- **Blob count** = `ceil(word_target / 200)`. E.g. 3000 -> 15, 2200 -> 11, 1116 -> 6.
- Blobs are numbered 1..N; every blob field is empty (`prompt` `""`, `type` `""`, `tags` `[]`, `text` `""`). Only `number` varies.
- `outline` holds the full text under the chapter, verbatim. Preserve `*italics*`, `(*subtext*)`, quotes, and hyphens exactly; encode line breaks as `\n`.
- `type` is the chapter type string if given (e.g. `"Violence - fights, kills, torture"`), else `""`.
- Never invent or fill blob contents; this only scaffolds the empty structure.
- No em-dashes anywhere.

## Steps

1. Parse title, number, word target, optional type, and outline text from the input.
2. Compute N = ceil(word_target / 200).
3. Write the JSON to the file/location the user names, or ask if unspecified. Pretty-print with 2-space indent.
