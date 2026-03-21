# Temp

Hey claude, I want you to launch ten opus-model sub-agents. For each model, I basically want you to pass the prompt below to each agent, adjust for the ten different scene numbers.
```
Read @Stories/RafeScigley/Scene-Docs/RafeScigley-scene-[#].md . I want you to review this scene for possible lore inconsistencies, and for any places where the existing world lore might play in. Reference any files in @Setting/ which might guide your understanding, except the Potential-Folklore folder. Do not reference any folders, skills, sub-agents, or files outside of the scene file and Settings. Your output should be a list of suggested fixes/additions, no mroe than 200 words in total length. Outpot only the list of suggested changes.
```
After the agents finish, I want you to concatenate their output into a single 'Suggested-Updates.md' file in the output folder. If any agent hits a permissions issue, have it stop and report back failure. Any questions?