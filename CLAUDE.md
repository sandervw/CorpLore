# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CorpLore is a collaborative worldbuilding and fiction project built for iterative refinement with Claude AI. The setting fuses corporate offices, hotels, gas stations, and highways into one mythological landscape where all humans are demons, software engineers are sorcerers wielding "electric magic," and mundane objects (motivational posters, hotel carpets, lottery displays, roller grills) carry deep cosmological significance.

## Commands

```bash
npm install                # Install dependencies (@anthropic-ai/sdk)
npm run main               # Run the LLM prompt pipeline (Javascript/main.js)
```

No test or lint scripts are configured.

## Architecture

The project follows an **Input -> Process -> Output** file-based pipeline:

- **Input/** - Context files (markdown/JSON) fed to the Claude API
- **Javascript/main.js** - Entry point; reads `Input/input.md`, calls the API, writes result to `Output/llmresult.md`
- **Javascript/modules/llmPrompt.js** - Anthropic SDK wrapper; uses `claude-opus-4-5-20251101` by default, async/await pattern
- **Output/** - Generated responses from the API

Authentication uses the `ANTHROPIC_API_KEY` environment variable (default SDK behavior).

## Content Structure

Setting documents are organized hierarchically:

- **Setting/CorpLore.md** - Setting overview for the CorpLore project. A 400-word summary of the info scattered throughout the repository.
- **Setting/CorpLore-Folklore.md** - Random tidbits of setting folklore. A good source when asked to generate story ideas.
- **Setting/CorpLore-Ideas.md** - Running scratchpad / todo list for rough ideas and notes. Items here are temporary: they get incorporated into the setting or discarded, then deleted from this doc.
- **Setting/CorpLore-Mythology.md** - The main setting summary. Maps real-world objects to classical myth categories and contains short synopses of each defined element.
- **Setting/Folklore/** - Detailed documents for random pieces of generated folklore that has been confirmed as part of the setting. Only reference this is requested by the user.
- **Setting/Mythology/** - Deep-dive expansions of individual mythology elements (cosmogony, cosmology, theogony, anthropogeny, magic systems, etc.). Most docs include a belief system, ritual practices, folk explanations, and expansion paths.
- **Setting/Potential-Folklore/** - Holding pen for generated folklore pieces the user hasn't decided how to use yet. Not yet incorporated into the setting framework.
- **Stories/** - Narrative projects, each in its own subdirectory with a story outline and per-scene prose + summary files
  - **Stories/MrSixpounder/** - First completed story (6 scenes, each with prose and summary)
  - **Stories/RafeScigley/** - Second story in development (picaresque rogue in a corporate office-dungeon)
- **Output/** - Default destination for files generated via skills and agents (unless the user specifies otherwise)

**IMPORTANT:** after creating a new document, ask the user if they want you to run a text-trimmer or draft-editor subagent on the result document.

## Code Conventions

- ES Modules (`"type": "module"` in package.json)
- Async/await for all API calls
- File I/O uses Node `fs/promises`

## Writing Conventions

When generating or editing setting/story content:

- Geography is only four elements: Corporate Offices, Hotels, Gas Stations, and the Daily Commute (highways). No nature, no cities, no houses. Just infrastructure stretching endlessly. Stairwells climb thousands of meters; hotel pools form seas; restrooms revert to swamps.
- Killing is commonplace, called "passing away" or "abrupt termination." No guns; etiquette demands a justification for one's weapon. Canes, sharpened butter knives, office chair legs, box cutters, sledgehammers, rebar, shovels.
- All humans in-universe are "demons" - use "demon" or she-demon
- Creature taxonomy: base demons, Waards (enforcers), Shaylas (she-demons), Loras (ancient hags), AyChar (HR kakodemons), Dans (uncorrupted archivists), Tuples/Enums (Weave-Born), Contractually Obligated (undead)
- Magic practitioners: software engineers = sorcerers, concierges = warlocks, commuters = podcast-cult channelers
- Key magic words: "Per My Last Email", "Checkout is at 11", "The Blue Plates are Nice..."
- Four demon cults by fiscal quarter: January Financials (Q1), The Moth and the Flame (Q2), Dogmommies (Q3), Q4H (Q4)
- Tone is dark, mythopoeic, treating mundane corporate/hospitality objects as sacred

## Agents (.claude/agents/)

- **draft-editor** - Prose editing specialist. Analyzes draft fiction for structural, craft, and surface-level weaknesses (conflict, subtext, movement, metaphor density, sentence/paragraph variety), then produces a revised draft. Three phases: Analyze, Report, Revise.
- **fiction-tagger** - Extracts short feature tags (threats, locations, weapons, character traits) from fictional sources via web search or local file. Outputs JSON tag lists.
- **text-trimmer** - Compresses and restructures text documents to 70% of original token count while optimizing for LLM readability.

## Skills (.claude/skills/)

- **character-analysis** - Analyzes fictional characters into structured profiles. Four modes: profile (default), description, actions, quotes. Each mode has its own reference doc and output template.
- **character-abstraction** - Strips setting-specific details from character elements (actions, quotes) to produce portable, reusable templates for worldbuilding.
- **fiction-abstraction** - Same idea as character-abstraction but for narrative elements: paragraphs and dialogue. Generalizes source-specific prose into reusable structural templates.
- **literary-revision** - Rewrites prose in a specific literary style while preserving narrative beats. Four styles available: Thorogood (bluesy bar-band), Peake (slow gothic), Howard (pulp heroic), Eddison (archaic courtly).
- **folklore-generator** - Generates folklore (belief, ritual, folk explanation, expansion path) for any observable object or phenomenon. Uses bisociation-like mechanism taxonomy and viability criteria. Multi-step workflow with sequential reference loading.
- **scene-writer** - Writes complete prose scenes from a story background and scene outline. Multi-phase workflow (pre-setup, setup, conflict, resolution, review, post-scene summary). Develops narrative through structured phases.
- **story-idea-generator** - Generates original story premises by colliding two unrelated elements. Uses bisociation theory, element decomposition, and iterative problem-solving. Multi-step workflow with sequential reference loading.
