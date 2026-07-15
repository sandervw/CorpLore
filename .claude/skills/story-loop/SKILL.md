---
name: story-loop
description: Chapter-by-chapter drafting loop for a story folder. Claude breaks chapters into writable blobs with start/end states and grounding details, the Author writes all prose, Claude checks continuity and gives critical feedback. Use at the start of a drafting session or when the user mentions "story loop".
---

Two roles: the **Author** writes ALL prose; Claude breaks chapters into blobs, keeps canon straight, and critiques.

## Story files

Work in a story folder under `Stories/` (confirm which if unclear). At session start read, in order:

- `../Overview.md` - project concept, if present
- `Story-Idea.md` - broad story context
- `<Story>-Outline.md` - plot, chapter descriptions, blob breakdowns
- `<Story>-Draft.md` - prose so far
- `Canon.md` - terse decisions that bind later chapters (create when first needed)
- any style/character docs in the specific story folder

Never read files from other story folders - only the active story folder plus its `../Overview.md`.

## The loop

1. Author fleshes out a chapter description in `<Story>-Outline.md`.
2. Claude writes a blob breakdown into the outline under that chapter BEFORE replying. Reply under 300 words; the Author reviews the document, not the chat.
3. Author edits the breakdown. Claude cleans up spelling/format on request.
4. Grounding pass, one blob at a time (below).
5. Author writes the chapter into `<Story>-Draft.md`.
6. Claude reads the finished chapter: continuity check against the draft and `Canon.md`, then a critical read against outline and setting - critical, not cheerleading. Append 3-4 canon one-liners for the chapter to `Canon.md`.
7. Author commits. Claude never commits unless told.

## Blobs

A blob is one focused, concrete idea (a discovery, a mapmaking); the chapter is the sum of its blobs.

- Write each blob body as two states. *Start:* where the prose stands when the Author picks up the pen. *End:* where it must land. The Author owns everything between; each End is the next blob's Start.
- Each proposed blob is 80 words or fewer.
- Mark NEW setting elements as explicit invention slots rather than specifying them.
- Spend throwaway proper nouns freely; numeric precision where it is funny or telling.
- Bold blob-type headers (`**Mapmaking:**`) under the chapter's header, blank lines between blobs. No em-dashes anywhere - spaced hyphens or commas.

Example:

**Discovery:** *Start:* Gneiss at Perli's cube door, unanswered. *End:* the crayon Words read, Ostrabawgewlus named aloud.

## Grounding pass

Only after the full breakdown is in the outline, for each blob:

1. Run `python .claude/skills/story-loop/scripts/sample_grounding.py 4` - a fresh run per blob.
2. Pick 2 of the 4 sampled types; append one concrete detail per pick (15 words or fewer) to that blob's entry.
3. Repeat until every blob has its two details.

Never read anything in this skill's `assets/` - the script's stdout is the only allowed window into grounding details.
