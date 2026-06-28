# Revision Steps

## (DONE) Manual

Start by manually revising each individual scene file
- Compare the scene to your outline
- Compare the scene to Morrowing inspiration

Make necessary edits
- Your usual manual changes
- Focus on cutting/trimming

## Automatic (Make Claude do it)

(DONE) Revise dialogue

(DONE) Run ruthless-pruner

(DONE) Run prose-detailer

```
VERBS/ADVERBS/ADJECTIVES
Hey claude, do a 'vocabulary' edit of the story scene below. Your job is to find the most common verbs, adverbs, and adjectives, and replace them with obscure, archaic, or excrutiatingly-specific synonyms. Only replace those three parts of speech; do not do any noun-replacements. Also no hyphenated, compound, or made-up replacements, and no word insertions/deletions (only *replacements*). Your goal is to replace only the 10% most-common verbs/adverbs/adjectives as they appear in fiction; if a word is the first one that appears in your large-language-model word completion, it is probably a common one. Your output should be just the edited text, no comments, summaries, etc.\n\nThe Scene:\n\n

NOUNS
Hey claude, do a 'vocabulary' edit of the story scene below. Your job is to replace roughly 10% of the *nouns* in the scene with obscure, archaic, or excrutiatingly-specific synonyms. Only replace the nouns - do not replace verbs, adjectives, etc. Also, do not replace any proper-nouns or pronouns. Your replacements must not be hyphenated, compound, or made-up words, and no word insertions/deletions (only *replacements*). Focus on the most-common nouns as they appear in fantasy; if a word is the first one that appears in your large-language-model word completion, it is probably a common one. Your output should be just the edited text, no comments, summaries, etc.\n\nThe Scene:\n\n
```

Run final spelling/grammar

Run final sanity check