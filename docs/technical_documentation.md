# Technical Documentation

## Purpose

This repository documents the reproducible code side of the AI-video project **The Last Data**. The final video production is manual, but the prompt process is made auditable through Python scripts, structured config files, generated tables, iteration logs, and a local Ollama API call.

## Two-Part Workflow

### Part 1: Code/NLP Workflow

The code performs the NLP/prompt workflow:

1. Read the workbook `data/input/prompt_image_video.xlsx`.
2. Extract shot IDs, tools, methods, prompts, reference images, output paths, and iteration notes.
3. Build `data/input/project_config.json`.
4. Validate declared media paths.
5. Call local Ollama through `http://localhost:11434/api/generate`.
6. Write reproducible output artifacts into `data/output/`.

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

This script validates the config, calls Ollama, and writes output artifacts.

Output files:

- `data/output/prompt_table.csv`
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
- The local LLM output is treated as a supporting summary, not as a replacement for the original prompt table.
- Full prompts are preserved in `prompt_table.csv`, `production_manifest.json`, and `wedavinci_upload_prompts.md`.

## Reproducibility Notes

The local model available during development was `gemma3:1b`. Because this is a small model, the code sends a compact project summary to Ollama and preserves the full prompts separately in deterministic output files. A stronger local Ollama model can be substituted by editing `ollama.text_model` in `data/input/project_config.json`.
