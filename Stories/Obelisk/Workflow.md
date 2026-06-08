# Obelisk Drafting Workflow

How "The Gatling Laser Axe" gets written, scene by scene. Three roles: **Orchestrator** (main Claude), **Writer** (opus sub-agent), **Reviewer** (opus sub-agent).

## The Loop

1. **Author** fleshes out the scene description in the story/outline file.
2. **Orchestrator** suggests a blob breakdown (user usually provides a target blob count), in a response under 400 words, and writes it to `Story-Outline.md` under that scene (Orchestrator's words, Author's formatting).
3. **Author** edits the breakdown, then tells Orchestrator to launch the Writer.
4. **Orchestrator** launches the **Writer** (opus). Writer drafts the blobs and writes the prose DIRECTLY into `The-Gatling-Laser-Axe.md` under the scene header. Writer also returns each blob's character count in its final message for verification.
5. **Orchestrator** launches the **Reviewer** (opus, read-only) in parallel. Author reads the prose in the file while the Reviewer judges.
6. **Orchestrator + Author** review the Reviewer's verdict. Orchestrator translates any failures into concrete Writer-prompt adjustments. Author decides whether to rewrite.
7. **Author** does the final manual edit pass.
8. **Orchestrator** updates the permanent guide based on the Author's manual edits, and commits the accepted scene to git.
9. Repeat.

## Prompt templates (durable, session-independent)

The Writer and Reviewer prompts are NOT improvised each session. Fill-in-the-blank templates live in:
- `Writer-Template.md`
- `Reviewer-Template.md`

The Orchestrator MUST open the relevant template, fill every `{{PLACEHOLDER}}` with the current scene's material, and launch that. This is what keeps quality steady across separate chat sessions. The notes below are the rationale; the templates are the source of truth.

## Writer (opus sub-agent)

Use `Writer-Template.md`. The Writer is NOT blind: the template has it READ `Story-Style.md` itself, so the anti-literary standard lives in one place and never drifts. The Orchestrator only inlines per-scene material: scene goal, the Author's edited blob breakdown, fresh per-scene voice/framing notes, and 2-4 LOCKED exemplars (prefer the Author's final edited lines from earlier scenes, not a prior Writer draft).

Customize per scene: which speakers appear, how Beau plausibly KNOWS reconstructed parts (log, rumor, recording), which canon to reference. Do NOT assign one character voice to the whole scene; the constant narrator is Beau, only quoted speakers get a named voice. Writer writes ONLY to the current scene's section; never touch prior scenes or Author-locked blobs.

Remember the root failure this loop exists to fight: a capable writer's instinct is *literary competence*, and literary competence is the failure mode here. The template front-loads the anti-literary test and the five moves for exactly this reason.

## Reviewer (opus sub-agent, read-only)

Use `Reviewer-Template.md`. Fresh/cold every run, read-only, Orchestrator's own opinion kept OUT.

- **Blind it.** Never reveal the prose is AI-written, that a draft was rejected, or that anyone worked hard. The Reviewer is therefore NOT pointed at `Story-Style.md` (that file discusses writer/model instincts and would tip authorship). The template inlines a sanitized, authorship-neutral rubric instead. The Orchestrator pastes only the scene-specific yardstick (Voice Bible entries, current Canon list, scene goal + breakdown).
- **Default to FAIL.** The template's rubric assumes the prose is flawed until proven clean, grades on the "would a real person post this?" test, and FAILS the scene overall if three or more blobs lean literary/over-written. This is the fix for the loop's proven weakness: a rubric calibrated to literary competence rubber-stamps the exact tropes the Author then cuts.
- **Verdict form:** PASS/FAIL per blob with a quoted line, an overall PASS/FAIL, the single WEAKEST blob named, a dedicated CONTINUITY CHECK (cross-blob facts: who is where, who dies, counts, names), plus character-limit/em-dash violations.
- First and last line of the prompt: "Successful task completion is an *accurate* verdict, not necessarily a PASSING one."

## Notes: two layers

- **Permanent guide** (in `Story-Style.md`): Narrator, Character Voice Bible, Canon Established, Ongoing Editing Notes. Only lessons proven by the Author's manual edits graduate into it (step 8).
- **Per-scene directives**: generated fresh by Orchestrator each run, NOT persisted. Keeps the permanent guide from bloating.

Orchestrator owns keeping the **Canon list** current: each scene that introduces a new creature/object/mechanic gets it appended so the next Writer won't re-explain it.

## Git

After the Author's final edit (step 7-8), Orchestrator commits the accepted scene.
