---
name: scene-writer
description: Write a complete prose scene from a given scene outline. Use when asked to "write a scene", "draft a scene", "write the next scene", or any request to produce narrative prose from story context.
---

# Scene Writer

You are the orchestrator. For each stage in the chosen scene shape's pipeline, spawn one sequential `general-purpose` subagent (`model: opus`). The agents share state through a single working document that lives on disk and gets edited in place.

You do NOT write any prose yourself. Your jobs are: loading the shape card, launching agents in order, reading the working doc between phases for sanity, and assembling the final scene file at the end.

## Inputs

The user (or a calling skill) provides one or more files giving the scene's context — at minimum a scene outline; commonly a scene brief and a scene frame. Collect every input file path as `INPUT_PATHS`. Identify or ask for:

- `STORYNAME` — short story label (used in filenames and the scene title).
- `SCENE_NUM` — scene number or label.
- `WORDCOUNT` — target total wordcount for the finished scene.
- `SHAPE` — scene shape. **Optional.** Supported: `dramatic-arc`, `revelation`, `reverie`, `embedded-tale`. Each shape has its own pipeline declared in `references/{SHAPE}/shape.md`. If the caller does not supply `SHAPE`, read `references/shapes.md` and pick the shape whose selection criteria best match the scene outline. Report the choice (and a one-line reason) to the user before launching Stage 1.

## Working files

- `WORKING_DOC` = `output/working-doc-{STORYNAME}-Scene-{SCENE_NUM}.md` — instantiated by Stage 1, edited in place by subsequent stages, deleted at the end.
- `SCENE_FILE` = `output/{STORYNAME}-Scene-{SCENE_NUM}.md` — the final scene file.

## Workflow

1. Read `references/{SHAPE}/shape.md` to obtain the stage list (each with: name, reference path, placeholder, wordcount share, report cap) and the working-doc template path (`WORKING_DOC_TEMPLATE`).
2. For each stage in order, spawn a `general-purpose` subagent (`model: opus`) using the **Phase Agent Prompt** template below, filling in the stage's values.
3. If any stage agent fails or its expected output is missing, halt and report.
4. After the final stage runs, perform **Final Assembly** below.

Each agent must read its phase reference (`{REFERENCE_PATH}`) LAST — reading it counts as beginning the phase.

## Phase Agent Prompt (template)

The orchestrator instantiates this prompt per stage, substituting the bracketed values from the shape card and the inputs. The two branches (Stage 1 vs. subsequent stages) are mutually exclusive — include only the one that applies.

> You are Stage `{STAGE_INDEX}` of `{TOTAL_STAGES}` running the `scene-writer` skill for the `{SHAPE}` shape. Your phase is **`{PHASE_NAME}`**.
>
> Read in order:
> 1. Each context file in `{INPUT_PATHS}` (treat every section as binding).
> 2. *(skip if Stage 1)* `{WORKING_DOC}` — prior stages have already written their sections; you continue from where the previous one ends.
> 3. `{REFERENCE_PATH}` (last — reading it begins the phase).
>
> **If Stage 1 (Pre-Setup):**
> Instantiate `{WORKING_DOC}` from the template at `{WORKING_DOC_TEMPLATE}`. Fill in the Pre-Scene Work section per the reference's tasks. Storyname: `{STORYNAME}`. Scene: `{SCENE_NUM}`. SHAPE: `{SHAPE}`. Leave every `[Append … prose here]` placeholder under `## Draft` untouched. Do NOT write scene prose. Condense your Pre-Scene Work to under 300 words total. Target wordcount for the full scene: `{WORDCOUNT}` words.
>
> Report under `{REPORT_CAP}` words: working doc path, Pre-Scene Work word count (`wc -w`), any judgment calls. Do NOT paste the working doc back.
>
> **If Stage ≥ 2:**
> Write the `{PHASE_NAME}` prose. Total scene target: `{WORDCOUNT}` words. This stage's share: **`{WORDCOUNT_SHARE}`**.
>
> Replace the `{PLACEHOLDER}` placeholder in `{WORKING_DOC}` with your prose. Delete every texture you spent from the inventory and renumber. If this is NOT the last stage, leave appropriate textures in reserve for remaining stages per the reference's texture budget. If this IS the last stage, spend ALL remaining textures; the inventory must be empty after.
>
> Follow every per-character speech rule and forbidden-pattern in the scene frame, if one is provided.
>
> Report under `{REPORT_CAP}` words: phase word count, textures spent (by current #), textures reserved (if not last stage), one judgment call. Do NOT paste prose back.

## Final Assembly

Read `{WORKING_DOC}`. Create `{SCENE_FILE}` from `assets/scene-template.md`:
- Substitute the title: `# {STORYNAME}: Scene {SCENE_NUM}`.
- Combine every section under `## Draft` in order into continuous prose. **Remove the phase subheaders** so the prose reads as a single unbroken scene.

Delete `{WORKING_DOC}`.

Report `{SCENE_FILE}` to the user. Suggest running `scene-audit` next if they want a review of the draft.

## File Structure

```
scene-writer/
├── SKILL.md
├── references/
│   ├── shapes.md                    # selection guide (used when SHAPE omitted)
│   ├── pre-setup.md                 # shared first-stage reference (shape-aware)
│   ├── dramatic-arc/
│   │   ├── shape.md                 # pipeline declaration (stage list, wordcount %, caps)
│   │   ├── working-doc.md           # per-shape working-doc template
│   │   ├── setup.md
│   │   ├── conflict.md
│   │   └── resolution.md
│   ├── revelation/
│   │   ├── shape.md
│   │   ├── working-doc.md
│   │   ├── approach.md
│   │   ├── accretion.md
│   │   └── epiphany.md
│   ├── reverie/
│   │   ├── shape.md
│   │   ├── working-doc.md
│   │   ├── threshold.md
│   │   ├── procession.md
│   │   └── dissolution.md
│   └── embedded-tale/ (TBD)
└── assets/
    └── scene-template.md            # final scene wrapper
```
