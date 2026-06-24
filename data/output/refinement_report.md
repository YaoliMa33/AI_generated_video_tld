# Prompt Refinement Report

## Workflow Position

This project uses a two-stage 0-to-1 AI-video prompt workflow. Stage 1 generates an initial shot and prompt plan from the story script. Stage 2 refines the prompt package using existing draft prompts, reference images, selected clips, and iteration notes.

Stage 1 does not create or replace image/video files. The existing images remain the grounding assets for Stage 2 refinement and for manual video generation.

## Generated Refinement Artifacts

- `generated_prompt_table.csv`: first-pass 0-to-0.5 prompts generated from the story script.
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

Okay, here’s a refinement summary for the AI video project, adhering strictly to your instructions:

**Story Premise:** The Last Data is set in a future architectural data worker who believes scanning and uploading civilization data is meaningless. During an extinction-level impact alert, they experience a catastrophic event that forces them into ruins.  They discover a hard drive containing the archived data of a lost civilization – the Civilization Archive – and realize it’s the key to rebuilding society as blue holographic architecture.

**Shot-by-Shot Storyboard:**

*   **Stage 1 (0-to-0.5): Script & Initial Shot Plan.** The script will detail initial scene setups, focusing on establishing a sense of isolation and bleakness within the ruins.  We'll generate a preliminary shot plan outlining key camera angles, lighting, and composition for the first few scenes – prioritizing visual storytelling over narrative details.
*   **Stage 2 (0.5-1): Refinement - Prompt Review & Iteration.** We’ll meticulously review the existing draft prompts generated in Stage 1.  Specifically, we'll focus on refining the image prompts to better capture the desired atmosphere of decay and technological remnants.  We will also refine the video prompt based on initial feedback from the shot plan.
*   **Stage 3 (0.5-1): Manual AI Video Production Workflow.** The script will be directly translated into detailed, specific prompts for WeDaVinci, PixVerse.ai, Seedance, or equivalent tool.  The focus is on establishing a consistent visual style and pacing – aiming for a slow, deliberate aesthetic reflecting the protagonist's disillusionment.
*   **Stage 4 (0.5-1): Initial Video Production.** The initial video production will be initiated with the generated prompts. We’ll prioritize establishing the core visuals of each scene, focusing on establishing a consistent color palette and lighting scheme to create a melancholic mood.

**Continuity Risks:**  The transition between scenes needs careful consideration. Ensure sufficient visual "space" is allocated for each shot to avoid jarring transitions. The 'explosion' sequence in Stage 2 requires significant attention to detail – the imagery should feel impactful and believable within the context of the ruins. Maintaining consistency with the initial shot plan will be crucial.

**Refinement Strategy:**  The primary refinement strategy involves iterative prompting based on feedback from the existing visuals. We’ll use a combination of prompt adjustments (e.g., adding details, altering composition) to achieve a cohesive and emotionally resonant final product. The focus is on enhancing the visual storytelling – emphasizing atmosphere, color palette, and overall mood rather than narrative exposition.  We'll also incorporate subtle 'visual cues' within the prompts to guide the AI towards a specific aesthetic (e.g., suggesting dust motes, crumbling textures).
