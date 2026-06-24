# Technical Documentation

## Purpose

This repository documents the reproducible code side of the AI-video project **The Last Data**. The final video production is manual, but the prompt process is made auditable through Python scripts, structured config files, generated tables, iteration logs, and a local Ollama API call.

The method is a **0.5-to-1 refinement workflow**. It does not claim to create a complete video from an empty story prompt. Instead, it starts from existing production material: a story premise, draft prompts, reference images, selected generated clips, scene notes, and iteration records. The code organizes these materials, validates them, and produces a refined prompt package for manual AI-video tools.

## Two-Part Workflow

### Part 1: Code/NLP Workflow

The code performs the NLP/prompt refinement workflow:

1. Read the workbook `data/input/prompt_image_video.xlsx`.
2. Extract shot IDs, tools, methods, prompts, reference images, output paths, and iteration notes.
3. Build `data/input/project_config.json`.
4. Validate declared media paths.
5. Call local Ollama through `http://localhost:11434/api/generate`.
6. Preserve the workbook prompts as source evidence.
7. Generate refined manual-upload prompts with explicit continuity, asset, and tool constraints.
8. Write reproducible output artifacts into `data/output/`.

### Part 2: Manual AI Video Production Workflow

The generated prompt package is used manually in video tools:

- WeDaVinci for text-to-image-to-video and image-to-video shots,
- PixVerse.ai for selected transition or hard-drive shots,
- Seedance for longer image-to-video / one-shot reconstruction clips.

The code does not automate these platforms. The final media work remains manual: upload/paste prompts, generate clips, save clips, edit, export final video, and prepare the presentation.

## Scripts

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
- `data/output/source_prompt_table.csv`
- `data/output/refined_prompt_table.csv`
- `data/output/refinement_report.md`
- `data/output/iteration_log.md`
- `data/output/iteration_log.json`
- `data/output/production_manifest.json`
- `data/output/storyboard.json`
- `data/output/wedavinci_upload_prompts.md`

### `src/ollama_client.py`

This file contains the local Ollama HTTP client. The current config uses:

- base URL: `http://localhost:11434`
- endpoint mode: `/api/generate`
- model: `gemma3:1b`

## Methodological Constraints

- The program does not claim to call WeDaVinci, PixVerse.ai, or Seedance APIs.
- The program does not silently create missing images, videos, prompts, or scenes.
- Missing declared files are treated as errors.
- The prompt workbook remains included as the source of truth.
- The local LLM output is treated as a supporting summary and refinement aid, not as a replacement for source evidence.
- Source prompts are preserved in `source_prompt_table.csv`, `prompt_table.csv`, and `production_manifest.json`.
- Refined prompts are written separately in `refined_prompt_table.csv` and `wedavinci_upload_prompts.md`.
- The method is described as improving an existing AI-video package from 0.5 to 1, not as generating a video from zero.

## Reproducibility Notes

The local model available during development was `gemma3:1b`. Because this is a small model, the code sends a compact project summary to Ollama and preserves the full prompts separately in deterministic output files. A stronger local Ollama model can be substituted by editing `ollama.text_model` in `data/input/project_config.json`.
