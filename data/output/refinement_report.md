# Prompt Refinement Report

## Workflow Position

This project is a 0.5-to-1 AI-video refinement workflow. It assumes that a story premise, draft prompts, reference images, selected clips, and iteration notes already exist. The code does not claim to generate a finished video from an empty prompt.

## Generated Refinement Artifacts

- `source_prompt_table.csv`: the source workbook prompts preserved as evidence.
- `refined_prompt_table.csv`: manual-upload prompts rebuilt from the source prompts with continuity, asset, and tool constraints.
- `wedavinci_upload_prompts.md`: human-readable refined prompt package for manual upload.
- `production_manifest.json`: reproducible inventory of inputs, outputs, and declared assets.

## Shot-Level Readiness

### s1-1: Office establishing shot

- Tool: wedavinci
- Method: text to image to video in Wedavinci
- Image reference: source_package/video_prompt_package/work_records/the_last_data_assets/scene-1-The_Weight_of_Meaningless_Work/shot-1/variant-1.png
- Existing clip: source_package/video_prompt_package/work_records/the_last_data_assets/scene-1-The_Weight_of_Meaningless_Work/shot-1/variant-3-selected.mp4
- Notes: Output directory: source_package/video_prompt_package/work_records/the_last_data_assets/scene-1-The_Weight_of_Meaningless_Work/shot-1 | Workbook output_ref normalized: source_package/video_prompt_package/work_records/the_last_data_assets/scene-1-The_Weight_of_Meaningless_Work/shot-1 | Refinement status: Ready for manual review and upload.

### s1-2: Office pressure and upload routine

- Tool: wedavinci
- Method: text to image to video in Wedavinci
- Image reference: source_package/video_prompt_package/work_records/the_last_data_assets/scene-1-The_Weight_of_Meaningless_Work/shot-2/variant-1.png
- Existing clip: source_package/video_prompt_package/work_records/the_last_data_assets/scene-1-The_Weight_of_Meaningless_Work/shot-2/variant-2-selected.mp4
- Notes: Output directory: source_package/video_prompt_package/work_records/the_last_data_assets/scene-1-The_Weight_of_Meaningless_Work/shot-2 | Workbook output_ref normalized: source_package/video_prompt_package/work_records/the_last_data_assets/scene-1-The_Weight_of_Meaningless_Work/shot-2 | Refinement status: Long video prompt; manual uploader may need to split or shorten it for the target platform.

### s1-3: Emergency alert interruption

- Tool: wedavinci
- Method: text to image to video in Wedavinci
- Image reference: source_package/video_prompt_package/work_records/the_last_data_assets/scene-1-The_Weight_of_Meaningless_Work/shot-3/variant-1.png
- Existing clip: source_package/video_prompt_package/work_records/the_last_data_assets/scene-1-The_Weight_of_Meaningless_Work/shot-3/variant-3-selected.mp4
- Notes: Output directory: source_package/video_prompt_package/work_records/the_last_data_assets/scene-1-The_Weight_of_Meaningless_Work/shot-3 | Workbook output_ref normalized: source_package/video_prompt_package/work_records/the_last_data_assets/scene-1-The_Weight_of_Meaningless_Work/shot-3 | Refinement status: Ready for manual review and upload.

### s2-1: Fist close-up

- Tool: wedavinci
- Method: image to video
- Image reference: source_package/video_prompt_package/work_records/S2S1_hands.png
- Existing clip: source_package/video_prompt_package/work_records/the_last_data_assets/scene-4-Scene_2_hit/shot-1/variant-1-selected.mp4
- Notes: Workbook image_ref normalized: source_package/video_prompt_package/work_records/S2S1_hands.png | Workbook output_ref normalized: source_package/video_prompt_package/work_records/the_last_data_assets/scene-4-Scene_2_hit/shot-1/variant-1-selected.mp4 | Refinement status: Ready for manual review and upload.

### s2-2: Explosion transition

- Tool: PixVerse.ai
- Method: 4 seconds. The apocalypse begins: an explosion erupts, sending shockwaves and dust through the scene. Flames rush toward the camera, glass shatters, and the debris completely covers the entire frame.
- Image reference: not declared
- Existing clip: not declared
- Notes: Refinement status: No declared image reference; manual reviewer should verify visual continuity. No declared generated clip; this shot may still require manual generation.

### s2-3: Confrontation with boss

- Tool: wedavinci
- Method: image to video
- Image reference: source_package/video_prompt_package/work_records/S2S2_hit.png
- Existing clip: source_package/video_prompt_package/work_records/the_last_data_assets/scene-5-Scene_5/shot-1/variant-1-selected.mp4
- Notes: Workbook image_ref normalized: source_package/video_prompt_package/work_records/S2S2_hit.png | Workbook output_ref normalized: source_package/video_prompt_package/work_records/the_last_data_assets/scene-5-Scene_5/shot-1/variant-1-selected.mp4 | Refinement status: Ready for manual review and upload.

### s3-1: Waking in the ruins

- Tool: seedance
- Method: image to video
- Image reference: not declared
- Existing clip: source_package/video_prompt_package/work_records/selected_video_clips/s3-1_wake.mp4
- Notes: Image reference directory: source_package/video_prompt_package/work_records/seedance_s3_reference_images | Workbook image_ref normalized: source_package/video_prompt_package/work_records/seedance_s3_reference_images | Workbook output_ref normalized: source_package/video_prompt_package/work_records/selected_video_clips/s3-1_wake.mp4 | Refinement status: No declared image reference; manual reviewer should verify visual continuity.

### s3-2: Activating the civilization archive hard drive

- Tool: PixVerse.ai
- Method: 
- Image reference: not declared
- Existing clip: not declared
- Notes: Workbook image_ref normalized: A young white male wearing a gray-brown jacket. | Workbook output_ref normalized: A silver metallic external hard drive with the words “CIVILIZATION ARCHIVE” printed on it. | Refinement status: No declared image reference; manual reviewer should verify visual continuity. No declared generated clip; this shot may still require manual generation. Long video prompt; manual uploader may need to split or shorten it for the target platform.

### s4: One-shot reconstruction

- Tool: seedance
- Method: image to video
- Image reference: not declared
- Existing clip: source_package/video_prompt_package/work_records/selected_video_clips/s4_seedance_onecut.mp4
- Notes: Image reference directory: source_package/video_prompt_package/work_records/seedance_s4_reference_images | Workbook image_ref normalized: source_package/video_prompt_package/work_records/seedance_s4_reference_images | Workbook output_ref normalized: source_package/video_prompt_package/work_records/selected_video_clips/s4_seedance_onecut.mp4 | Refinement status: No declared image reference; manual reviewer should verify visual continuity.

## Ollama Refinement Summary

## Refinement Summary: The Last Data - Half-Finished AI Video Production

This project is currently in a state of refinement, focusing on enhancing the visual storytelling and technical execution.  The core narrative revolves around Protagonist and Boss grappling with the implications of an extinction-level event – the collapse of civilization data. This requires careful attention to shot composition, prompt consistency, and workflow integration. The AI video production pipeline is currently being refined through iterative prompting and manual tool usage.

**Story Premise:** The protagonist, a Data Worker, discovers a hard drive containing the remnants of a lost Civilization Archive.  This archive holds the blueprints for rebuilding society after a catastrophic event. Protagonist and Boss are tasked with this reconstruction as the world collapses around them.

**Shot-by-Shot Storyboard:**

*   **s1-1:** "Office establishing shot" - *Tool: Wedavinci*. – Focus on a large, slightly dilapidated office space, emphasizing dust motes and muted lighting to establish the setting of the future.  The composition should convey a sense of decay and isolation.
*   **s1-2:** “Office pressure and upload routine” - *Tool: Wedavinci*. – A fast-paced sequence depicting the protagonist manually uploading data from the hard drive, emphasizing movement and urgency. Utilize quick cuts to highlight the process.
*   **s1-3:** "Emergency alert interruption" - *Tool: Wedavinci*. –  A dramatic, chaotic scene showing a simulated emergency alert triggered by the archive's contents. The visual should convey shock and potential danger.
*   **s2-1:** “Fist close-up” - *Tool: Wedavinci*. – A close-up of the protagonist’s face, conveying determination or weariness as they examine the hard drive.  Focus on subtle details to establish character presence.
*   **s2-2:** "Explosion transition" - *Tool: PixVerse.ai*. – This shot will use a 4-second sequence to depict an explosion erupting from the scene, sending shockwaves and dust through the area. The camera should be angled downwards to emphasize the scale of the destruction.
*   **s2-3:** "Confrontation with boss" - *Tool: Wedavinci*. – Protagonist facing Boss in a dimly lit room. Focus on the protagonist's posture, conveying a sense of conflict and perhaps apprehension.  The lighting should be stark and create shadows to emphasize the tension.
*   **s3-1:** "Waking in the ruins" - *Tool: Seedance*. – A wide shot showcasing the protagonist emerging from rubble, looking at the archive hard drive. The composition should highlight the vastness of the ruined landscape.
*    **s3-2:** “Activating the civilization archive hard drive” - *Tool: PixVerse.ai*. –  A slow, deliberate sequence showing the process of activating the hard drive, highlighting the data being restored. Use a color palette that shifts from muted to brighter tones as it's activated.
*   **s4:** "One-shot reconstruction" - *Tool: Seedance*. – A single shot showcasing the complete archive hard drive and its contents. The composition should be visually striking, emphasizing the scale of the data.

**Manual Video Production Notes (WeDaVinci & PixVerse.ai):**

*   Utilize WeDaVinci for initial text-to-image generation based on the story outline.
*   Employ PixVerse.ai to create the final video segments, focusing on establishing a consistent visual style and pacing.  Specifically, prioritize smooth transitions between shots.
*   Maintain shot order throughout the entire production – this is crucial for narrative cohesion.
*   Carefully attribute all tools used (WeDaVinci, PixVerse.ai) consistently.

**Continuity Risks:**

*   Potential inconsistencies in lighting and color grading across different scenes will require careful attention during post-production.
*   The transition between the initial text-to-image generation and the final video segments needs to be seamless – ensure smooth transitions are implemented.  A slight delay or visual stutter could disrupt the flow of the narrative.

**Refinement Strategy:**

Phase 1 (0.5 - 1 refinement): Focus on refining the composition of s2-2, particularly the explosion transition and the confrontation scene.  Iterate on the lighting to enhance the dramatic impact. Refine shot transitions between scenes – ensure a consistent flow.
Phase 2 (0.5 - 1 refinement):  Strengthen the visual storytelling through more detailed character expressions and subtle environmental cues.  Fine-tune the color palette for greater emotional resonance. Address any potential inconsistencies in the generated clips.

**Note:** This summary prioritizes establishing a solid foundation for the AI video production. Further iteration will be driven by feedback from the initial shot list and the generated content.
