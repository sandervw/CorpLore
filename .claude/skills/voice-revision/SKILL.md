---
name: voice-revision
description: Revise, rewrite, or redo prose in specific character 'voices'. Use when user asks to revise text in Freeman, Cugel, Gittes, Dagoth Ur, or Solaire voice. Also use for any request to rewrite with a particular voice or as a particular character.
---

# Literary Revision

Revise user-provided prose into a specific character voice while preserving core narrative beats.

## Workflow

1. Identify requested voice from user input
2. Load the appropriate voice reference from `references/`
3. Extract core beats from source prose (outline, not rewrite)
4. Apply guidelines systematically
5. Verify output respects any character limit specified

## Available Voices

| Voice         | Voice                                    | Use Case                                      | Reference            |
| ------------- | ---------------------------------------- | --------------------------------------------- | -------------------- |
| **Freeman**   | Neurotic 1st person, stream of consciousness | Comedic self-interested survival narration | [freeman-voice.md]   |
| **Cugel**   | Grandiose rogue, ornate self-assured inner monologue | Entitled swindler narration with Vancian diction | [cugel-voice.md]   |
| **Gittes**  | Cynical PI, hard-boiled inner monologue              | Suspicious detective narration with noir diction  | [gittes-voice.md]  |
| **Dagoth Ur** | Messianic god-king, serene prophetic inner monologue | Betrayed deity narration with liturgical diction | [dagoth-ur-voice.md] |
| **Solaire** | Devout questing knight, radiant faith inner monologue | Earnest pilgrim narration with wondering diction | [solaire-voice.md] |

## Voice Selection

- User says "Freeman," "Freeman's Mind," "neurotic," "inner monologue," "stream of consciousness" → Load freeman-voice.md
- User says "Cugel," "Cugel's Saga," "Vancian," "grandiose rogue," "swindler narration" → Load cugel-voice.md
- User says "Gittes," "Chinatown," "hard-boiled," "noir," "gumshoe," "cynical PI" → Load gittes-voice.md
- User says "Dagoth Ur," "messianic," "god-king," "betrayed god," "liturgical," "prophetic" → Load dagoth-ur-voice.md
- User says "Solaire," "Praise the Sun," "sunlight warrior," "radiant faith," "questing knight," "jolly cooperation" → Load solaire-voice.md
- Ambiguous request → Ask user to specify voice

## Output Guidelines

- Preserve all core narrative beats from source
- Respect character limits if specified (default: no limit)
- Do not add plot elements absent from source
- Voice transformation only—not content invention
