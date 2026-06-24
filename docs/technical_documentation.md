# Technical Documentation

## Purpose

This repository documents the reproducible code side of the AI-video project **The Last Data**. The final video production is manual, but the prompt process is made auditable through Python scripts, structured config files, generated tables, iteration logs, and a local Ollama API call.

The method is a **two-stage 0-to-1 prompt workflow**. It does not claim to generate the final video automatically. Instead, it separates prompt generation from video production:

1. **0-to-0.5 script-to-prompt generation**: read `story_script.md` and generate a first shot plan, text-to-image prompts, and image-to-video prompts.
2. **0.5-to-1 asset-grounded refinement**: read the existing workbook, reference images, selected generated clips, scene notes, and iteration records; then validate and refine the prompt package for manual AI-video tools.
3. **Feedback-driven iteration**: read human problem records and optimization suggestions after media review, then generate next-round prompts.

Stage 1 writes prompt artifacts only. It does not create, replace, or overwrite images or videos. The existing reference images remain the grounding assets for Stage 2 and for manual video generation. The feedback iteration stage also writes prompt artifacts only.

## Two-Part Workflow

### Part 1: Code/NLP Workflow

The code performs the NLP/prompt workflow:

1. Read the story script `data/input/story_script.md`.
2. Generate an initial prompt plan with `src/generate_from_script.py`.
3. Read the workbook `data/input/prompt_image_video.xlsx`.
4. Extract shot IDs, tools, methods, prompts, reference images, output paths, and iteration notes.
5. Build `data/input/project_config.json`.
6. Validate declared media paths.
7. Call local Ollama through `http://localhost:11434/api/generate`.
8. Preserve the workbook prompts as source evidence.
9. Generate refined manual-upload prompts with explicit continuity, asset, and tool constraints.
10. Read human problem records from `data/input/problem_records/`.
11. Generate next-round prompts with `src/iterate_prompts.py` when feedback exists.
12. Write reproducible output artifacts into `data/output/`.

### Part 2: Manual AI Video Production Workflow

The generated prompt package is used manually in video tools:

- WeDaVinci for text-to-image-to-video and image-to-video shots,
- PixVerse.ai for selected transition or hard-drive shots,
- Seedance for longer image-to-video / one-shot reconstruction clips.

The code does not automate these platforms. The final media work remains manual: upload/paste prompts, generate clips, save clips, edit, export final video, and prepare the presentation.

After reviewing generated media, the user can write a problem record such as "shot s1-2 starts too wide" or "the boss speaks too early." The iteration script detects the feedback file and writes the next prompt table for another manual generation attempt.

## Scripts

### `src/generate_from_script.py`

This script implements Stage 1: 0-to-0.5 script-to-prompt generation.

Input:

- `data/input/story_script.md`

Output:

- `data/output/generated_prompt_table.csv`
- `data/output/script_to_prompt_plan.md`
- `data/output/stage1_generation_manifest.json`

This script produces prompt artifacts only. It does not write image or video files.

### `src/build_config_from_workbook.py`

This script converts the workbook into `project_config.json`.

Input:

- `data/input/prompt_image_video.xlsx`
- extracted source assets under `data/input/source_package/`

Output:

- `data/input/project_config.json`

The script preserves workbook values and does not invent missing clips. If a workbook row references a directory with a selected video, the script links the selected `.mp4`. If a row has no generated video path, the config leaves `video_path` empty.

### `src/main.py`

This script validates the config, calls Ollama, and writes output artifacts. It keeps the original workbook prompts separate from the refined prompts so that the workflow remains auditable.

Output files:

- `data/output/prompt_table.csv`
- `data/output/generated_prompt_table.csv`
- `data/output/script_to_prompt_plan.md`
- `data/output/stage1_generation_manifest.json`
- `data/output/source_prompt_table.csv`
- `data/output/refined_prompt_table.csv`
- `data/output/refinement_report.md`
- `data/output/iteration_log.md`
- `data/output/iteration_log.json`
- `data/output/production_manifest.json`
- `data/output/storyboard.json`
- `data/output/wedavinci_upload_prompts.md`

### `src/iterate_prompts.py`

This script implements feedback-driven prompt iteration.

Input:

- `data/input/problem_records/*.md`
- `data/input/problem_records/*.txt`
- `data/output/refined_prompt_table.csv`

Output:

- `data/output/iterations/<round_id>/next_prompt_table.csv`
- `data/output/iterations/<round_id>/iteration_report.md`
- `data/output/iterations/<round_id>/iteration_manifest.json`

The script automatically scans the feedback folder. If a feedback file mentions shot IDs such as `s1-2`, `s3-1`, or `s4`, the feedback is applied to those shots. If a feedback file has no shot ID or uses `global`, it is treated as global feedback. The script does not generate or replace images/videos.

### `src/ollama_client.py`

This file contains the local Ollama HTTP client. The current config uses:

- base URL: `http://localhost:11434`
- endpoint mode: `/api/generate`
- model: `gemma3:1b`

## Methodological Constraints

- The program does not claim to call WeDaVinci, PixVerse.ai, or Seedance APIs.
- The program does not silently create missing images, videos, prompts, or scenes.
- Declared media paths are validated because Stage 2 claims to use existing media as evidence. This validation does not prove that a clip was generated from a prompt; it only prevents the workflow from citing missing files.
- Missing declared reference files are treated as errors.
- The prompt workbook remains included as the source of truth.
- The local LLM output is treated as a supporting summary and refinement aid, not as a replacement for source evidence.
- Stage 1 prompt generation does not overwrite reference images or selected clips.
- Feedback-driven iteration does not overwrite reference images or selected clips.
- Source prompts are preserved in `source_prompt_table.csv`, `prompt_table.csv`, and `production_manifest.json`.
- Refined prompts are written separately in `refined_prompt_table.csv` and `wedavinci_upload_prompts.md`.
- Next-round prompts are written separately in `data/output/iterations/<round_id>/next_prompt_table.csv`.
- The method is described as 0-to-1 at the prompt-workflow level: 0-to-0.5 prompt generation plus 0.5-to-1 asset-grounded refinement and manual video production.

## Reproducibility Notes

The local model available during development was `gemma3:1b`. Because this is a small model, the code sends a compact project summary to Ollama and preserves the full prompts separately in deterministic output files. A stronger local Ollama model can be substituted by editing `ollama.text_model` in `data/input/project_config.json`.
