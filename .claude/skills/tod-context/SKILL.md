---
name: tod-context
description: Use this skill whenever you are missings setting context or lore for the Time of Dying setting.
---

# Time-of-Dying Setting Lore

## Vocabulary lookups (sampling-first)

**Never read `setting/vocabulary.json` directly.** Use the sampling script for these arrays. Run commands from within the `setting/` subdirectory.

Treat sampling output as stylistic inspiration only; do not copy/paste content into new stories verbatim.

| Need | Command |
| :--- | :--- |
| Spells | `python sampling.py spells` |
| Ceremonies, Rituals, Rites | `python sampling.py ceremonies_rituals_rites` |
| Curses, Afflictions | `python sampling.py curses_affliction` |
| Mundane Necromantic Duties | `python sampling.py mundane_necromantic_duties` |
| Astrological/Religious Events | `python sampling.py astrological_religious_events` |
| Titles, Roles | `python sampling.py titles_roles` |
| Necromancy Supplies | `python sampling.py necromancy_supplies` |
| Locations | `python sampling.py locations` |
| Undead | `python sampling.py undead` |
| Cosmologisms | `python sampling.py cosmologisms` |
| Epithets | `python sampling.py epithets` |

## Setting-specific spellings

- "Chrypt" replaces "Crypt"
- "Tohmb" replaces "Tomb"

Apply to all setting content.

## Deeper lore (read if broader story context would help)

- `setting/Time-of-Dying.md`: Setting overview for the Time-of-Dying project.
- `setting/Folklore.md`: Random setting folklore. Good source when generating story ideas.
- `setting/Mythology.md`: Main setting summary. Maps setting details to specific myth categories.
- `setting/folklore/`: Detailed documents for confirmed folklore. Only reference if the user requests.
- `setting/mythology/`: Deep-dive expansions of mythology elements (cosmogony, cosmology, theogony, anthropogeny, magic systems).
- `setting/archive/`: Old or unused setting/story documents. Never access unless directed by the user.
