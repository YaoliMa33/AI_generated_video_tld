# Problem Records and Optimization Suggestions

Place human review notes in this folder when a generated image or video clip is not satisfactory.

The iteration script scans every `.md` and `.txt` file in this folder and uses the content as feedback for the next prompt revision round.

Recommended format:

```text
Shot: s1-2
Observed problem:
- The camera starts too wide and does not match the previous shot.
- The boss speaks before the emergency broadcast ends.

Optimization direction:
- Keep the opening frame close to the previous clip's final frame.
- Delay the boss dialogue until after the broadcast is fully finished.
- Keep the red alarm beeps as background sound under the boss dialogue.
```

Rules:

- Use shot IDs such as `s1-1`, `s1-2`, `s2-3`, `s3-1`, or `s4` when the feedback belongs to a specific shot.
- If a note applies to the whole film, write `Shot: global`.
- Do not put API keys or platform credentials in this folder.
- The script does not generate images or videos. It only writes the next-round prompt table and iteration report.
