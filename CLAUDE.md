# CLAUDE.md

## Project Overview

CorpLore is a collaborative fiction project built for iterative composition with Claude AI. The setting fuses corporate offices, hotels, gas stations, and highways into one mythological landscape where all humans are demons, software engineers are sorcerers wielding "electric magic," and mundane objects (motivational posters, hotel carpets, lottery displays, roller grills) carry deep cosmological significance.

## Content Structure

Setting documents are organized hierarchically:

- **Setting/CorpLore.md** - Setting overview for the CorpLore project. A 500-word summary of the info scattered throughout the repository.
- **Setting/CorpLore-Folklore.md** - Random setting folklore. A good source when asked to generate story ideas.
- **Setting/CorpLore-Ideas.md** - Running scratchpad / todo list for rough ideas and notes. Items here are incorporated or discarded, then deleted from the doc.
- **Setting/CorpLore-Mythology.md** - The main setting summary. Maps real-world phenomenon to classical myth categories.
- **Setting/Folklore/** - Detailed documents for random pieces of generated folklore that has been confirmed as part of the setting. Only reference this is requested by the user.
- **Setting/Mythology/** - Deep-dive expansions of individual mythology elements (cosmogony, cosmology, theogony, anthropogeny, magic systems, etc.).
- **Setting/Potential-Folklore/** - Holding pen for generated folklore pieces the user hasn't decided how to use yet. Not yet incorporated into the setting framework.
- **Stories/** - Narrative projects, each in its own subdirectory
- **Output/** - Default destination for files generated (unless the user specifies otherwise)

**IMPORTANT:** after creating a new document, ask the user if they want you to run a text-trimmer or ruthless-pruner subagent on the result document.

## Writing Conventions

When generating or editing setting/story content:

- There is no pre-corporate era; the corporate world has always existed. "Old" or "defunct" things are older companies/franchises, not a prior age.
- Geography is only four elements: Corporate Offices, Hotels, Gas Stations, and the Daily Commute (highways). No nature, no cities, no houses. Just endless, antediluvian infrastructure. Stairwells climb in labyrinthine clusters thousands of meters high, to the rime-capped roof access, gleaming white in the stark upper light; hotel pools form wave-capped salt seas; restrooms revert to caustic, fetid swamps.
- Killing is commonplace, called "abrupt termination." No guns; etiquette demands a justification, however nonsensical, for one's weapon. Weighted canes, serrated butter knives, iron chair legs, well-forged box cutters, sledgehammers, rusted rebar, grave-shovels. Demons carry these openly, holstered on gem-studded lanyards or belted at the hipbone.
- All humans in-universe are "demons" - use "demon" or "she-demon"
- Creature taxonomy: base demons, Waards (slab-shouldered enforcers), Shaylas (blade-tongued she-demons), Loras (ancient hags), Aychar (HR kakodemons), Dans (uncorrupted archivists), Tuples/Enums (Weave-Born), Contractually Obligated (the sleepless undead)
- Magic practitioners: software engineers = sorcerers, concierges = warlocks, commuters = podcast-cult channelers
- Key magic words: "Per My Last Email", "Checkout is at 11", "The Blue Plates are Nice..."
- Four demon cults by fiscal quarter: January Financials (Q1), The Moth and the Flame (Q2), Dogmommies (Q3), Q4H (Q4)
- Tone is dark, mythopoeic, treating mundane corporate/hospitality objects as sacred. Sprinkle 1-3 word mythic or violent modifiers onto ordinary nouns: "antediluvian corkboard," "gem-studded lanyard," "notch-bladed letter opener." Weapons, objects, and architecture should feel old, as if they came from an ancient empire's treasure vault, even when they are just office supplies.

## Agents (.claude/agents/)

- TODO

## Skills (.claude/skills/)

- TODO
