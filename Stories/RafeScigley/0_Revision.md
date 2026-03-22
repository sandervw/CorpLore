# Revision Steps

## (DONE) Manual

Start by manually revising each individual scene file

Start with review
- Compare the scene to your outline
- Compare to the scene to CorpLore
- Compare the scene to Cugel Inspiration

Make necessary edits
- Your usual manual changes
- Focus on cutting/trimming

Review for common LLM patterns (things to have it avoid next time)

## Automatic Claude Edits

POSSIBLE IDEA: Compare each manually-edited scene file to claude's output
- Break down differences for each file
- Ask claude to create editing guide for each file
- Ask claude to merge editing guides

### 1. General prose review (Went well)

Tropes, scenes-logic issues, etc
```
PROMPT
Hey claude, do a general prose review of the text below. Your job is to find logical inconsistencies, use of common fiction tropes, repeated beats - anything that seems 'rough' or 'unpolished' in the prose. Your output should be a a brief list of any identified issues, along with suggested fixes. Your output must be less than 200 words.\n\nThe Prose:\n\n
```

### 2. Lore consistency review (Gave same recs over and over...)

Look for missed opportunities to weave in lore

```
RAN VIA 10 OPUS-LEVEL SUB-AGENTS
Read @Stories/RafeScigley/Scene-Docs/RafeScigley-scene-[#].md . I want you to review this scene for possible lore inconsistencies, and for any places where the existing world lore might play in. Reference any files in @Setting/ which might guide your understanding, except the Potential-Folklore folder. Do not reference any folders, skills, sub-agents, or files outside of the scene file and Settings. Your output should be a list of suggested fixes/additions, no mroe than 200 words in total length. Outpot only the list of suggested changes.
```

### 3. Word choice (Very Effective - especially nouns)

(uncommon verbs/adverbs/adjectives, specific instances of nouns, certain % replacement for each)

Possible future idea - have it do 'Archaic word replacement' too

```
VERBS/ADVERBS/ADJECTIVES
Hey claude, do a 'vocabulary' edit of the story scene below. Your job is to find the most common verbs, adverbs, and adjectives, and replace them with uncommon synonyms. Only replace those three parts of speech; do not do any noun-replacements. Also no hyphenated, compound, or made-up replacements, and no word insertions/deletions (only *replacements*). Your goal is to replace only the 15% most-common verbs/adverbs/adjectives as they appear in fiction; if a word is the first one that appears in your large-language-model word completion, it is probably a common one. Your output should be just the edited text, no comments, summaries, etc.\n\nThe Scene:\n\n

NOUNS
Hey claude, do a 'vocabulary' edit of the story scene below. Your job is to replace roughly 15% of the *nouns* in the scene with obscure, archaic, or excrutiatingly-specific synonyms. Only replace the nouns - do not replace verbs, adjectives, etc. Also, do not replace any proper-nouns or pronouns. Your replacements must not be hyphenated, compound, or made-up words, and no word insertions/deletions (only *replacements*). Focus on the most-common nouns as they appear in fantasy; if a word is the first one that appears in your large-language-model word completion, it is probably a common one. Your output should be just the edited text, no comments, summaries, etc.\n\nThe Scene:\n\n
```

### 4. Dialogue (Mixed effectiveness - need to really stress no "adding", and no editing non-dialogue)

For Rafe - updated to match Rogue style guide

```
RAFE
Hey claude, read the following style guide:\n\n{style_guide}\n\nYour job is to edit dialogue and character-thoughts in the fiction scene pasted below using these guidelines. You are only editing the dialogue/thoughts of the character *Rafe*, no other characters. If you need to increase the length of Rafe's dialogue, do so by 'folding' surround exposition/description into the dialogue; reframe surrounding text as dialogue, do not simply repeat beats/thoughts. o prevent bloating, the total length in characters of your final output text must be less than or equal to the length of the original - count before and after. Your output should be just the edited text, no comments, summaries, etc.\n\nThe Scene:\n\n
```

## Future Process Changes

Possibly don't pass in specific style guide during writing
- too much context
- save it for a specific post-processing step