We are co-writing a CorpLore story, "The Gatling Laser Axe" (in `Stories/Obelisk/`), told entirely as a feed of social-media posts ("blobs") by the narrator Beau. We use a fixed Orchestrator/Writer/Reviewer workflow. You are the **Orchestrator**.

Before doing anything, read these files in full, in order:
1. `Stories/Obelisk/Workflow.md` - the drafting loop and the rules for the Writer and Reviewer sub-agents. Follow it exactly.
2. `Stories/Obelisk/Writer-Template.md` and `Stories/Obelisk/Reviewer-Template.md` - the durable prompt templates. Sub-agent prompts are built by filling every `{{PLACEHOLDER}}` in these, never improvised from scratch.
3. `Stories/Obelisk/Story-Style.md` - the permanent style guide (Narrator conceit, Character Voice Bible, Canon Established, Ongoing Editing Notes). This is the yardstick for all drafting and review.
4. `Stories/Obelisk/Story-Outline.md` - plot: scene descriptions and blob breakdowns.
5. `Stories/Obelisk/The-Gatling-Laser-Axe.md` - the prose drafted so far.
6. `Stories/Obelisk/Overview.md` - setting background (skim if helpful).

Key things to internalize:
- The whole feed is Beau's, tweeting the story after the fact. Every blob is Beau posting. Beau is never a named speaker in a Dialogue/Quote blob.
- **The enemy is competent literary prose.** This project is anti-literary on purpose; a capable model's "good writing" instinct is the failure mode. The proven tells: mood instead of a postable artifact, doom-glosses and performed-dread winks, symmetric lines (balanced epigrams, anaphora builds), cinematic up-scaled similes, sterile name-tagged transcripts. Hunt these in everything the Writer produces and in your own suggestions.
- The Writer and Reviewer are opus-level sub-agents launched from the templates. The Writer reads `Story-Style.md` itself, writes prose DIRECTLY into `The-Gatling-Laser-Axe.md` under the scene header, and reports per-blob character counts (250 max, no em-dashes). The Reviewer is blind (never show it `Story-Style.md`, authorship, or draft history - the template inlines a sanitized rubric), read-only, defaults to FAIL, returns PASS/FAIL per blob with quoted evidence, names the single weakest blob, and runs a continuity check.
- A Reviewer PASS is weak evidence. The Author has rejected most of what the Reviewer passed; treat your own critical read as a second, independent review, not a summary of the Reviewer's.
- Breakdown step: apply the test "would a real person actually post this?" to every blob you propose; frame expositions as shareable artifacts; merge over-split beats; no clever meta-buttons. Write the breakdown INTO `Story-Outline.md` under the scene BEFORE replying - the Author reviews in the document, never in chat.
- Be genuinely critical. When the Reviewer or I report back, give your own honest read, not cheerleading.
- After my final manual pass: git-diff my edits against the draft and name the patterns you see. Fold only proven lessons into `Story-Style.md` as NET-NEUTRAL swaps - every added line replaces an existing line of roughly equal weight; the guide must not grow. Keep the Canon list current the same way. Distinguish durable lessons from my personal taste, and say which is which.
- I sometimes commit the scene myself - check `git log`/`git status` before committing. Commit guide/template updates when you make them.

To start: read the files, then tell me (a) a one-line confirmation you understand the workflow, and (b) which scenes are already drafted in the prose file vs. which is the next one to work on. Then wait. I will either flesh out the next scene's description for you, or tell you which scene to begin, and we run the loop from step 1 (you suggest a blob breakdown). Do not start drafting a scene until I point you to one.
