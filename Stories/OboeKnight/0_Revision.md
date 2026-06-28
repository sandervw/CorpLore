# Revision Steps

## Manual

Start by manually revising each individual scene file
- Compare the scene to your outline
- Compare the scene to Morrowing inspiration

Make necessary edits
- Your usual manual changes
- Focus on cutting/trimming

## Automatic (Make Claude do it)

Revise dialogue

Run prose-pruner

Check for lore consistency

Edit for specificity:
```
Hey claude, I need you to function as a subagent orchestrator for a revision task. I want you to pass the following prompt to three opus-level sub-agents:

PROMPT_START:
Hey claude, read @{FILE} . Do not read any other files. I want you to revise and overwrite this scene file. Your goal is to make the scene more concrete and specific by apply the set of actionable changes below:
1. Convert plural objects/elements into singular ones with a descriptive tag.
2. Replace general descriptive attributes ("wood") with specific ones ("chestnut").
3. Swap abstract nouns ("violence") for the act ("a boot on his wrist").
4. Replace adverbs with the gesture they summarize ("said angrily" becomes a slammed cup).
5. Attach a number where you wrote "many" or "some."
6. Cut "seemed/felt like"; state it.
7. Trade "walked" for how they walked.
8. Replace "things/stuff" with the actual object.

Keep your edits as minimal as possible: you are not rewriting the story, changing the plot, changing the characters, or making other large-scale revisions. You are making minimal adjustments which add specificity to the scene. Your final wordcount must not exceed 105% of the original wordcount. Remember: cutting/replacing is better than adding.
PROMPT_END:

Each agent should be given one of three scene files (scenes 7-9) from @stories\Dreamreel\Scenes\ . Scenes 1-6 are already done.

Any questions?
```

```
VERBS/ADVERBS/ADJECTIVES
Hey claude, do a 'vocabulary' edit of the story scene below. Your job is to find the most common verbs, adverbs, and adjectives, and replace them with obscure, archaic, or excrutiatingly-specific synonyms. Only replace those three parts of speech; do not do any noun-replacements. Also no hyphenated, compound, or made-up replacements, and no word insertions/deletions (only *replacements*). Your goal is to replace only the 10% most-common verbs/adverbs/adjectives as they appear in fiction; if a word is the first one that appears in your large-language-model word completion, it is probably a common one. Your output should be just the edited text, no comments, summaries, etc.\n\nThe Scene:\n\n

NOUNS
Hey claude, do a 'vocabulary' edit of the story scene below. Your job is to replace roughly 10% of the *nouns* in the scene with obscure, archaic, or excrutiatingly-specific synonyms. Only replace the nouns - do not replace verbs, adjectives, etc. Also, do not replace any proper-nouns or pronouns. Your replacements must not be hyphenated, compound, or made-up words, and no word insertions/deletions (only *replacements*). Focus on the most-common nouns as they appear in fantasy; if a word is the first one that appears in your large-language-model word completion, it is probably a common one. Your output should be just the edited text, no comments, summaries, etc.\n\nThe Scene:\n\n
```

Run final spelling/grammar

Run final sanity check