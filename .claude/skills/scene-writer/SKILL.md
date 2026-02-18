---
name: scene-writer
description: Write a complete prose scene from a story background and scene outline. Use when asked to "write a scene", "draft a scene", "write the next scene", or any request to produce narrative prose from a scene outline or story context.
---

# Scene Writer

Write a complete prose scene by developing it through structured narrative phases.

## Inputs

The user provides:

- **Story background**: The broader narrative context (world, characters, prior events).
- **Scene outline/idea**: What this specific scene should accomplish — its purpose, characters involved, tone.
- **Scene priorities (optional)**: What different aspects of style or parts of of prose should weigh most in the scene - action, dialogue, humor, etc.
- **Wordcount**: Target length for the finished scene.

## Workflow

_Each step's reference file must only be read AFTER the previous step's output has been completed. Do NOT batch-read reference files. Reading a step's reference file counts as beginning that step._

---

### Step 1: Pre-Setup

Read `references/pre-setup.md`.

Using the story background and scene outline, follow the reference file's instructions to generate the raw material for this scene.

### Step 2: Condense to Working Document

Condense the output of Step 1 to **under 300 words**. This is your scene's working inventory — a compact reference of elements available to draw from as you write.

Write this condensed material to a new file using the `assets/working-doc.md` template.

### Step 3: Setup

Read `references/setup.md`.

Follow the reference file's instructions to write the setup phase of the scene, drawing from your working document.

### Step 4: Append Setup & Spend Details

Append the prose you wrote in Step 3 to your `working-doc.md` file.

Then, in the working document's inventory section, **remove any textural details you used** in the setup.

### Step 5: Conflict

Read `references/conflict.md`.

Follow the reference file's instructions to write the conflict phase of the scene, drawing from the remaining details in your working document.

### Step 6: Append Conflict & Spend Details

Append the prose you wrote in Step 5 to your `working-doc.md` file.

Again, **remove any textural details you used** from the working document's inventory.

### Step 7: Resolution

Read `references/resolution.md`.

Follow the reference file's instructions to write the resolution phase of the scene, drawing from the remaining details in your working document.

### Step 8: Append Resolution & Begin Post-Scene Section

Append the prose you wrote in Step 7 to your `working-doc.md` file.

In the working document's **Post-Scene** section, fill in the **Questions Posed** subsection — the unresolved threads or tensions that carry forward into future scenes. The remaining Post-Scene subsections (Scene Summary, Characters, Reflection) will be filled in during later steps.

**Remove any remaining textural details** from the working document's inventory. The inventory should now be empty.

### Step 9: Review

Read `references/review.md`.

Follow the reference file's instructions to review and revise the full scene prose in your working document. This is a revision pass — tighten, adjust, and polish. Also fill in the **Reflection** subsection of the Post-Scene section.

### Step 10: Write to Scene Template

Copy the `assets/scene-template.md` template to a new file named `[Storyname]-Scene-[X].md` (where `[Storyname]` is derived from the story background and `[X]` is the scene number, provided by the user or inferred).

Write your reviewed scene prose into the **Full Scene** section. Combine the setup, conflict, and resolution into continuous text — **remove the phase subheaders** (Setup / Conflict / Resolution) so the prose reads as a single unbroken scene.

### Step 11: Post-Scene

Read `references/post-scene.md`.

Follow the reference file's instructions to generate post-scene material — filling in the **Scene Summary** and **Characters Introduced or Referenced** subsections.

### Step 12: Write Post-Scene Summary

Copy the `assets/post-scene-summary.md` template to a new file named `[Storyname]-Scene-[X]-Summary.md`.

Write the full post-scene material (Scene Summary, Questions Posed, Characters, and Reflection) into this file.

### Step 13: Clean Up & Present

Delete the working document created in Step 2.

Present both finished files to the user:
- `[Storyname]-Scene-[X].md` — the scene prose
- `[Storyname]-Scene-[X]-Summary.md` — the post-scene summary

## File Structure

```
scene-writer/
├── SKILL.md
├── references/
│   ├── pre-setup.md
│   ├── setup.md
│   ├── conflict.md
│   ├── resolution.md
│   ├── review.md
│   └── post-scene.md
└── assets/
    ├── working-doc.md
    ├── scene-template.md
    └── post-scene-summary.md
```
