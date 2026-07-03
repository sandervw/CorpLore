# Obelisk Drafting Workflow

How The current story gets written, scene by scene. Two roles: the **Author** (writes ALL prose) and **Claude** (suggests breakdowns, keeps canon and continuity straight).

## Session start

Read, in order:
- `Obelisk/Overview.md` (broad character/setting concept)
- `Obelisk/Koschei/Story-Idea.md` (broad story context)
- `Obelisk/Koschei/Scene-Outline.md` (plot, scene descriptions)
- `Obelisk/Koschei/Koschei-Draft.md` (story so far)

## The Loop

1. **Author** fleshes out the scene description in `Scene-Outline.md`.
2. **Claude** proposes a *beat* breakdown and writes it INTO `Scene-Outline.md` under that scene BEFORE replying;
   1. The chat reply stays under 300 words (Claude's words, Author's formatting)
   2. The Author reviews the breakdown in the document, never in chat
3. **Author** edits the breakdown. Claude may be asked to clean up spelling/format afterward.
4. **Author** writes the scene's prose into `Koschei.md`.
5. **Claude** reads the finished scene:
   1. Run a continuity check (who is where, who dies, counts, names, compass directions against earlier scenes)
   2. Give an honest critical read only if asked - critical means critical, not cheerleading.
6. **Author** commits. Claude NEVER commits unless explicitly told to.

## *Beat* Breakdown principles

- Under 200 words per beat - beats should be things the author could write up in a spare ~15 minutes
- Merge over-split beats; no clever meta-buttons.
- Mark invention (NEW setting elements) as explicit slots rather than specifying the inventions.
- Spend new throwaway proper nouns freely; numeric precision where it is funny or telling.

## Grounding pass (after every breakdown)

Only AFTER the full beat breakdown is written into `Story-Outline.md`, run a grounding pass, one beat at a time:
1. Run `python Stories/Obelisk/sample_grounding.py 4` to sample four grounding-detail types.
2. For the current beat, pick 2 of the 4 types and suggest one concrete detail per chosen type (2 details total, each 15 words or fewer), appended to that beat's breakdown entry in `Story-Outline.md`.
3. Rerun the script fresh for the next beat and repeat until every beat has its two details.

Never read `Grounding-Details.json` or `Grounding-Details.md` (or any other grounding file in the Obelisk folder) - the script's output is the only allowed window into them.

## Format constraints

- Each beat aims for 250 characters or fewer.
- No em-dashes anywhere; spaced hyphens or commas.
- `## Scene N` headers, bold beat-type headers (`**Personal:**`), blank lines between beats.
