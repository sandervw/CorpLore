# Obelisk Drafting Workflow

How "The Gatling Laser Axe" gets written, scene by scene. Three roles: **Orchestrator** (main Claude), **Writer** (opus sub-agent), **Reviewer** (opus sub-agent).

## The Loop

1. **Author** fleshes out the scene description in the story/outline file.
2. **Orchestrator** suggests a blob breakdown (usually a target blob count), in a response under 400 words, and writes it to `Story-Outline.md` under that scene (Orchestrator's words, Author's formatting).
3. **Author** edits the breakdown, then tells Orchestrator to launch the Writer.
4. **Orchestrator** launches the **Writer** (opus). Writer drafts the blobs and writes the prose DIRECTLY into `The-Gatling-Laser-Axe.md` under the scene header. Writer also returns each blob's character count in its final message for verification.
5. **Orchestrator** launches the **Reviewer** (opus, read-only) in parallel. Author reads the prose in the file while the Reviewer judges.
6. **Orchestrator + Author** review the Reviewer's verdict. Orchestrator translates any failures into concrete Writer-prompt adjustments. Author decides whether to rewrite.
7. **Author** does the final manual edit pass.
8. **Orchestrator** updates the permanent guide based on the Author's manual edits, and commits the accepted scene to git.
9. Repeat.

## Writer (opus sub-agent)

Prompt is CUSTOMIZED per scene. Always include:
- The single most important rule: the entire feed is **Beau's**, tweeting after the fact (see `Story-Style.md` > Narrator).
- The Voice Bible (per-quote character voices). Do not flatten voices into one tone.
- The Canon list (do NOT re-explain established creatures/objects).
- The Editing Notes (voice first; anti-generic).
- The scene goal + the Author's edited breakdown.
- 250-character max per blob. No em-dashes.
- Any prior good blobs in the scene, passed as LOCKED exemplars / the quality bar.

Do NOT assign one random character voice to the whole scene. The constant narrator is Beau; only quoted speakers get their own named voice. Customize notes per scene: remove, add, or change them to fit (e.g. earlier we dropped the "match Guts" note because it flattened everything).

Writer writes ONLY to the current scene's section. Never touch prior scenes or Author-locked blobs.

## Reviewer (opus sub-agent, read-only)

Goal: impartial judgment of whether the prose matches the original idea and style, or is generic/unfitting. Anti-leniency safeguards (mandatory):
- **Blind it.** Never tell it the prose is AI-written, that a prior draft was rejected, or anything that invites approval. No "we worked hard on this." It evaluates a submission against a standard.
- Give it the real yardstick: scene goal, Author's edited breakdown, Voice Bible, Canon list, Editing Notes.
- **Verdict form: PASS/FAIL per blob, each backed by a quoted line as evidence.** It must also name the single WEAKEST blob. A reviewer forced to find the worst thing cannot blanket-approve.
- Fresh/cold every run, no memory of past runs. Read-only (judges, does not edit).
- Orchestrator keeps its own opinion OUT of the Reviewer prompt.

## Notes: two layers

- **Permanent guide** (in `Story-Style.md`): Narrator, Character Voice Bible, Canon Established, Ongoing Editing Notes. Durable, applies to all scenes. Only lessons proven by the Author's manual edits graduate into it (step 8). Scene descriptions and blob breakdowns stay in `Story-Outline.md`.
- **Per-scene directives**: generated fresh by Orchestrator each run, NOT persisted. Keeps the permanent guide from bloating.

Orchestrator owns keeping the **Canon list** current: each scene that introduces a new creature/object/mechanic gets it appended so the next Writer won't re-explain it.

## Git

After the Author's final edit (step 7-8), Orchestrator commits the accepted scene. Any later Writer run that clobbers something is one `git restore` away from recovery.
