# blob-smoother - captured request bodies

### `system` message

**Task:**
You are given an ordered set of consecutive passages. Every passage except the last is a read-only reference. Edit ONLY the last passage so it flows from and stays consistent with the one(s) before it.

**Story context:**
The protagonist is Gneiss, a lone demon. Gneiss is on a quest that takes him into planes of hell. His magic Coat hides his senses, making him unsensed. All humans are demons and she-demons. The tale is told first-person in an archaic voice.

**Rules/Method:**
- Focus on the transition from the prior passage to your 
- Reconcile only real conflicts: contradictory names/locations/descriptions, jarring jumps, vocabulary repetition.
- Don't introduce new details, characters, objects, or events.
- Do NOT erase unique details. Fix only serious conflicts.
- Preserve the last passage's form: its mode is 'description' and its type is 'foreshadowing'. Do not, for example, turn dialogue into narration.
- *Your revision must be under 250 words*. Exceeding this is failure.

**Output Format:**
Return ONLY the revised last passage. No preamble, no labels, no commentary, no 'pre-revision'. Nothing before or after the prose.

### `user` message

Here are the passages (Edit ONLY the final one.)

**Passage 1 (FIXED - reference only)**
```
The Coat drinks the light ere it finds mine eyes, and I walk unsensed beneath the vault of that first hell. Ankle-deep we wade through sable-waters, liquid opal glowing with bruised amethyst and sickly jade, each ripple catching hues that have no name in any tongue of earth or pit. The mulchers follow, their great heads lowered, breath steaming in air thick as honey.

Walls rise at impossible angles — geometry that bites the reason — folded shadow upon folded shadow, tangled shadows and silence woven tight as shroud-cloth. No torch burns here. None need. The water births its own pallor, a phosphorescence seeping from stone that never knew sun.

Yet — *there*. Half-drowned in silt, a rusted iron spike driven deep between two slabs. The hammer-marks still fresh upon its head. A chain once clung to it, long since rotted or wrenched free. Some wretch was bound here. Some wretch *waited* here. The spike bears the crooked signature of mortal hands: impatient, fearful, precise.

We pass it by. The water swallows our footfalls whole.
```

**Passage 2 (EDIT THIS - the last passage)**
```
The shadow realm did this to those who dwelt too long within its borders. I had marked it before, in other hells, in other marching columns of the damned—how the oppressive atmosphere settled into a demon's bones like moisture into old stone. The she-demons who led the procession had eyes that had deepened past ordinary darkness, past mere fatigue, until each socket held something resembling a small and private abyss. Their gestures, once perhaps slight and quotidian, had grown vast. A raised hand became an invocation. A turned head became a declaration of grief. They moved as though unseen musicians scored their every step, as though the dim and sourceless light had bleached away all middle tones and left only the stark extremes of brightness and void. Their mouths shaped words I could not hear, yet the words looked enormous—proclamations, condemnations, elegies. The wear of accumulated time showed in their coats, their boots, the cracks running like old maps across their knuckles. They had been here long enough that the place had entered them. I pulled my Coat close and kept still, grateful to be unsensed, grateful the shadow had not yet found the marrow of my particular bones.
```

Return only the revised final passage, prose only.

