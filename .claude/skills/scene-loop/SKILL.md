---
name: scene-loop
description: Scene-by-scene drafting loop for a story folder. Claude proposes beat breakdowns with grounding details, the Author writes all prose, Claude checks continuity and gives critical feedback. Use at the start of a drafting session or when the user mentions "scene loop".
---

Two roles: the **Author** writes ALL prose; Claude breaks scenes into beats, keeps canon straight, and critiques.

## Story files

Work in a story folder under `Stories/` (confirm which if unclear). At session start read, in order:

- `../Overview.md` - project concept, if present
- `Story-Idea.md` - broad story context
- `Scene-Outline.md` - plot, scene descriptions, beat breakdowns
- `<Story>-Draft.md` - prose so far
- `Canon.md` - terse decisions that bind later scenes (create when first needed)
- any style/character docs in the specific story folder

Never read files from other story folders - only the active story folder plus its `../Overview.md`.

## The loop

1. Author fleshes out a scene description in `Scene-Outline.md`.
2. Claude writes a beat breakdown into `Scene-Outline.md` under that scene BEFORE replying. Reply under 300 words; the Author reviews the document, not the chat.
3. Author edits the breakdown. Claude cleans up spelling/format on request.
4. Grounding pass, one beat at a time (below).
5. Author writes the scene into `<Story>-Draft.md`.
6. Claude reads the finished scene: continuity check against the draft and `Canon.md`, then a critical read against outline and setting - critical, not cheerleading. Append 3-4 canon one-liners for the scene to `Canon.md`.
7. Author commits. Claude never commits unless told.

## Beats

- Under 200 words per beat - sized so the Author can write it up in a spare ~15 minutes.
- Mark NEW setting elements as explicit invention slots rather than specifying them.
- Spend throwaway proper nouns freely; numeric precision where it is funny or telling.
- `## Scene N` headers, bold beat-type headers (`**Personal:**`), blank lines between beats. No em-dashes anywhere - spaced hyphens or commas.

## Grounding pass

Only after the full breakdown is in `Scene-Outline.md`, for each beat:

1. Run `python .claude/skills/scene-loop/scripts/sample_grounding.py 4` - a fresh run per beat.
2. Pick 2 of the 4 sampled types; append one concrete detail per pick (each 15 words or fewer) to that beat's entry.
3. Repeat until every beat has its two details.

Never read anything in this skill's `assets/` - the script's stdout is the only allowed window into grounding details.
