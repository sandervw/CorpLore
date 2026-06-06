Hey claude, read the following three files. Analyze them closely to understand what this story is about. PAy particularly close attention to the 'form' or 'structure' I'm going for. When you finished, gie an under 250 word explanation of how this story is being developed, and what it's about.
- @Stories\Obelisk\Overview.md
- @Stories\Obelisk\Story-Outline.md
- @Stories\Obelisk\The-Gatling-Laser-Axe.md

Great job. Your task for this chat is to help me break down the rest of te scenes into blobs, and draft the blobs for each scene. We're going to do this scene by scene. Let's start with *Scene 2*. Could suggest a blob breakdown for this scene? Try for *7-9 blobs* total. Keep your response under 400 words, and write your suggested breakdown to the outline (your words, but keep my formatting).

I've made a few edits to your suggested outline. Now, let's try to draft it. I think this works best if you function as an orchestrator. Pass the necessary info to an opus-level sub-agent. Instruct it to draft the blobs for the scene we just worked on. Make sure it notes the following:
- The blobs are 250 characters max
- The blobs are written like social media posts written by a dark fantasy character (pass it a random character name: Elric of Menibone, Guts, Mazirian the Magician, or Kane from Legacy of Kane)
Any questions?

I've edited the agent's original draft of the blobs. I want you to analyze what the agent wrote, and how I changed it. Come up with a brief (under 100 word) list of general 'types' or 'styles' of edit I made. Don't give specific examples: focus on patterns to stress, and focus on anti-patterns to avoid.
Once you have your list, can you put it under the new 'Ongoing editing notes' section I added to the outline. After that, we'll proceed.

I've fleshed out the next scene now, so let's move onto *Scene 3*. Suggest a blob breakdown for this scene. Try for *5-6 blobs* total. Keep your response under 400 words, and write your suggested breakdown to the outline (your words, but keep my formatting).

I've edited. Same thing as before: Pass the necessary info to an opus-level sub-agent. Instruct it to draft the blobs for the scene we just worked on. Make sure it notes the following:
- The blobs are 250 characters max
- The blobs are written like social media posts written by a dark fantasy character (pass it a random character name: Elric of Menibone, Guts, Mazirian the Magician, or Kane from Legacy of Kane)
- *Make sure to highlight the editing notes we worked on with this run.*
Any questions?

Okay, this is better. Before we proceed to the 'editing notes' and next scene, lets update our workflow and get it fixed in place. I'm thinking something like the following:
1. I flesh out the scene file, and have you (**Orchestrator**) suggest a blob breakdown (usually with a set number of blobs).
2. You write your 400 word response (your words, my formatting) to the outline.
3. I edit the breakdown. I tell you to pass the necessary info to an opus-level sub-agent (**Writer**). Instruct it to draft the blobs for the scene. Make sure 250-character max, social-media-post-like text. Plus, any ongoing style/editing notes we have. *New*: for this, I want you to customize your prompt, and the editing notes, to fit the current scene. Just like you took out the "match Guts voice" note - remove, add, and change notes as needed based on our discussion.
4. The agent writes the prose (*new* have it actually write the prose to the story file from now on - I prefer to review text in the actual file).
5. *New*: you pass the freshly-written prose, along with the original goal, to *another* opus level sub-agent (**Reviewer**). The reviewer decides if the prose is generic/unfitting to the original idea, or if it genuinely matches the outline and style we set up. DO NOT prompt the agent with anything that would encourage it to rate positively - the goal is for the Reviewer to be completely arbitrary.
6. You (Orchestrator) and I review what the agent decided. I tell you if we need to rewrite (new Writer) with prompt/style adjustments.
7. After potential rewrites, I edit for the final time.
8. You update the editing guide based on my manual edits.
9. Repeat.

Does this make sense? Do you have any questions/suggestions?

claude --resume dac67900-a4ac-4ac6-a221-35030f8b740e