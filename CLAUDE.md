# CLAUDE.md

A fiction project for the the **CorpLore** setting.
- `Stories/` - In progress and completed stories/narratives
- `Output/` - Default destination for generated files (unless the user specifies otherwise)

After creating a new document, ask the user if they want you to run text-trimmer or ruthless-pruner.

When counting words in a file, always use `wc -w <file>`

All skills referenced by name live in this project at `<project>/.claude/skills/<name>/`, never in `~/.claude/skills/`. Pass absolute paths to subagents.

"*subtext*" in an outline indicates material that should not be given directly in a scene - it should be hinted as obliquely as possible.

## Content Structure

- `Setting/CorpLore-Folklore.md` - Random setting folklore
- `Setting/CorpLore-Ideas.md` - Running scratchpad / todo list for ideas
- `Setting/CorpLore-Mythology.md` - Main setting summary
- `Setting/Folklore/` - Only reference this is requested by the user
- `Setting/Mythology/` - Deep-dive expansions of individual setting elements
- `Setting/Potential-Folklore/` - Only reference this is requested by the user
- `Stories/` - In progress and completed stories/narratives
- `Output/` - Default destination for generated files (unless the user specifies otherwise)

## Writing Conventions

When creating or editing content:
- There is no pre-corporate era; the corporate world has always existed.
- All geography is made of four elements: Corporate Offices, Hotels, Gas Stations, and the Daily Commute (highways).
- Killing is commonplace; most demons have weapons.
- All humans in-universe are "demons" - use "demon" for men, "she-demon" for women
- There are various magic practitioners: software engineers, concierges, podcast-cult channelers
- Many magics are based on key words/phrases: "Per My Last Email", "Checkout is at 11", "The Blue Plates are Nice..."
- There are four demon cults: January Financials, The Moth and the Flame, Dogmommies, Q4H
- The tone is dark, mythopoeic. Sprinkle 1-3 word mythic or violent modifiers onto ordinary nouns.
- Weapons, objects, and architecture should feel old, as if they came from an ancient empire.

## Communication Style

When communicating in chat with the user, and in fiction/fiction-planning documents, **Always** write the following style:
- **Prefer** complex sentences to simple ones
- **Prefer** a large sentence length standard deviation
- **Prefer** long sentences built from paratactic lists and appositives, not clauses
- **Prefer** function words 'of' and 'a'
- **Prefer** pronoun declarations via 'of': "I of", "You of", "She of"
- **Prefer** Anglo-Saxon verbs (*get, cut, put*, not *obtain, sever, position*)
- **Prefer** concrete monosyllabic nouns
- **Avoid** perfect grammar (Positive example: "She of long hair")
- **Avoid** *-tion/-ment/-ity* nominalizations
- **Never** use function words 'if', 'would', 'could', 'the', 'as', 'there', or 'but'
- **Never** use similes, only metaphor by direct assertion
- **Never** use contractions (dialogue excepted)
- **Never** use semicolons or ellipses (the colon is the only hinge)