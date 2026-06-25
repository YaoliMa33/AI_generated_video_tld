# The Last Data

This repository contains the code and documentation for a two-part AI video assignment workflow. The Code/NLP part is framed as a **two-stage 0-to-1 prompt workflow with feedback-driven iteration**:

1. **0-to-0.5 script-to-prompt generation**: start from a story script and generate an initial shot plan, text-to-image prompts, and image-to-video prompts.
2. **0.5-to-1 asset-grounded refinement**: use the existing prompt workbook, reference images, selected generated clips, and iteration notes to validate and refine the production package.
3. **Feedback-driven prompt iteration**: after manually reviewing a generated image or video, write problem records and optimization suggestions; the code detects those feedback files and writes the next-round optimized prompt table.

Part 1 is the **Code/NLP Workflow**. Python programs read the source script, prompt workbook, scene notes, reference images, generated clip paths, and iteration notes. They call a local Ollama LLM API and save generated prompts, source prompts, refined prompts, a storyboard/refinement summary, production manifest, and iteration log.

Part 2 is the **Manual AI Video Production Workflow**. The final prompts are entered manually into AI video tools such as WeDaVinci, PixVerse.ai, and Seedance. The generated clips are saved, edited, and exported as the final video and presentation.

The repository does not automate WeDaVinci, PixVerse.ai, or Seedance access. No platform credentials, cookies, or private API tokens are stored in this project.

## Technical Highlights

1. **Two-Stage Prompt Workflow**
   - Stage 1 starts from the story script and generates initial image prompts and image-to-video prompts.
   - Stage 2 uses existing images, generated clips, workbook records, and human review notes to refine the prompt package.
   - This reflects the real production process: the code supports prompt generation and improvement, while media generation remains a manual creative step.

2. **Local LLM API With Ollama**
   - The workflow uses a local Ollama API to generate and refine prompt-related text.
   - The current configuration uses `gemma3:1b` through `http://localhost:11434/api/generate`.
   - No private cloud API key is required, so another user can rerun the code with their own local Ollama setup.

3. **Prompt Table as Production Tracker**
   - The output tables organize each shot by shot ID, image prompt, video motion prompt, visual style, source assets, problem notes, and revised prompt.
   - The tables act as a production tracker for manual upload into AI video tools.
   - Source prompts and refined prompts are saved separately so the workflow remains auditable.

4. **Human-in-the-Loop Iteration**
   - After reviewing generated images or videos, the user writes problem records and optimization directions in `data/input/problem_records/`.
   - The iteration script automatically detects those files and generates the next-round optimized prompt table.
   - Iteration outputs are saved in `data/output/iterations/<round_id>/` without overwriting previous assets or prompt tables.

5. **Manual AI Video Production Boundary**
   - WeDaVinci, PixVerse.ai, Seedance, or similar tools are used manually.
   - Python does not upload prompts, control video-platform accounts, or store platform credentials.
   - The code is responsible for prompt generation, prompt refinement, documentation, and reproducibility.

## Authors

Name(s): Yaoli Ma, Ziyu Guo  
Course: NLP 2026  
University: Technical University of Munich  
Semester / Year: Summer 2026

## Project Overview

The video, **The Last Data**, is a short cinematic AI-generated film about a future architectural data worker who believes scanning and uploading civilization data is meaningless. During an extinction-level impact alert, the conflict between the protagonist and the boss escalates. After the catastrophe, the protagonist wakes in ruins, discovers the `CIVILIZATION ARCHIVE` hard drive, and the stored data becomes the basis for rebuilding the city as blue holographic architecture.

The code does not generate the final video directly. Its role is to make the prompt workflow reproducible and defensible: it extracts the workbook-based prompt process into a structured JSON config, validates declared media paths, calls Ollama, preserves the original prompts as source evidence, and writes a refined prompt package for manual upload.

This is not presented as a fully automated video generator. Stage 1 generates prompts only. It does not create, replace, or overwrite images or clips. Stage 2 keeps the existing reference images and selected clips as the grounding assets for manual video generation.

## Repository Structure

```text
.
|-- README.md
|-- requirements.txt
|-- src/
|   |-- generate_from_script.py
|   |-- build_config_from_workbook.py
|   |-- iterate_prompts.py
|   |-- main.py
|   `-- ollama_client.py
|-- data/
|   |-- input/
|   |   |-- story_script.md
|   |   |-- prompt_image_video.xlsx
|   |   |-- workbook_nonempty_cells.json
|   |   |-- project_config.json
|   |   |-- project_config.example.json
|   |   |-- media/
|   |   |   `-- final_video.mp4
|   |   |-- problem_records/
|   |   `-- source_package/
|   `-- output/
|       |-- prompt_table.csv
|       |-- generated_prompt_table.csv
|       |-- script_to_prompt_plan.md
|       |-- stage1_generation_manifest.json
|       |-- source_prompt_table.csv
|       |-- refined_prompt_table.csv
|       |-- refinement_report.md
|       |-- iteration_log.md
|       |-- iteration_log.json
|       |-- production_manifest.json
|       |-- storyboard.json
|       |-- wedavinci_upload_prompts.md
|       `-- iterations/
|-- docs/
|   `-- technical_documentation.md
`-- presentation/
    |-- llm_io_demo.ipynb
    `-- the-last-data_final_presentation.pptx
```

| Path | Description |
| --- | --- |
| `src/generate_from_script.py` | Stage 1: generates a first shot/prompt plan from `story_script.md` |
| `src/build_config_from_workbook.py` | Converts the prompt workbook into `data/input/project_config.json` |
| `src/main.py` | Validates the config, calls Ollama, writes source prompt artifacts, and generates refined manual-upload prompts |
| `src/iterate_prompts.py` | Detects human problem records and writes next-round optimized prompts |
| `src/ollama_client.py` | Local Ollama HTTP API client |
| `data/input/prompt_image_video.xlsx` | Original prompt/process workbook |
| `data/input/source_package/` | Original prompt package with reference images and generated clips |
| `data/input/media/final_video.mp4` | Final exported video provided for submission |
| `data/output/` | Generated prompt table, iteration log, manifest, storyboard, and manual upload package |
| `docs/` | Technical workflow documentation |
| `presentation/llm_io_demo.ipynb` | Jupyter demonstration notebook for visualizing feedback-driven prompt iteration |
| `presentation/the-last-data_final_presentation.pptx` | Final project presentation |

## Requirements

- Python 3.10 or newer
- Python packages listed in `requirements.txt`: `openpyxl`, `pandas`, `notebook`
- A running local Ollama HTTP service
- Local Ollama model configured in `data/input/project_config.json`
  - Current local configuration: `gemma3:1b`
  - API mode: `/api/generate`
- Manual access to WeDaVinci, PixVerse.ai, Seedance, or equivalent video generation tools

Ollama runs locally and normally does not require an external API key.

## Setup Instructions

```bash
git clone https://gitlab.lrz.de/nlp2026/yazimaguo/nlp2026_yazimaguo.git
cd nlp2026_yazimaguo
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

On macOS / Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start Ollama and make sure the configured model is available:

```bash
ollama pull gemma3:1b
ollama serve
```

## How to Run in Terminal

Terminal execution is the standard reproducible workflow. It writes all generated files to `data/output/`.

### 1. Generate the Stage 1 script-to-prompt plan

Purpose: convert `data/input/story_script.md` into an initial shot plan, image prompts, and image-to-video prompts.

Command:

```bash
python src/generate_from_script.py --script data/input/story_script.md --output data/output
```

Expected result:

- `data/output/generated_prompt_table.csv`
- `data/output/script_to_prompt_plan.md`
- `data/output/stage1_generation_manifest.json`

Check: open `data/output/generated_prompt_table.csv` and verify that shot-level prompts were written.

This step does not create or modify image/video assets.

### 2. Rebuild the structured project config from the workbook

Purpose: convert the original workbook into `data/input/project_config.json`, which is used by the refinement script.

Command:

```bash
python src/build_config_from_workbook.py --workbook data/input/prompt_image_video.xlsx --input-dir data/input --output data/input/project_config.json
```

Expected result:

- `data/input/project_config.json`

Check: open `data/input/project_config.json` and verify that shots, prompts, tools, and declared media paths are present.

### 3. Validate the config without calling Ollama

Purpose: check declared paths and config structure before making an LLM call.

Command:

```bash
python src/main.py --config data/input/project_config.json --output data/output --dry-run
```

Expected result:

- the command should finish without path or config errors
- no new Ollama output is required in this dry run

Check: if this step fails, fix the missing or incorrect declared input path before running the LLM workflow.

`--dry-run` does not call Ollama.

### 4. Generate the Stage 2 refined prompt package through Ollama

Purpose: preserve source prompts, call the local Ollama API, and write refined prompts for manual upload into AI video tools.

Command:

```bash
python src/main.py --config data/input/project_config.json --output data/output
```

Expected result:

- `data/output/source_prompt_table.csv`
- `data/output/refined_prompt_table.csv`
- `data/output/refinement_report.md`
- `data/output/wedavinci_upload_prompts.md`
- `data/output/production_manifest.json`
- `data/output/storyboard.json`

Check: open `data/output/refined_prompt_table.csv` and `data/output/refinement_report.md`.

This command calls Ollama.

### 5. Generate a next-round prompt table from human feedback

Purpose: convert written problem records and optimization directions into next-round prompts.

After manually reviewing a generated image or video, write feedback in `data/input/problem_records/` and run:

```bash
python src/iterate_prompts.py --feedback-dir data/input/problem_records --prompt-table data/output/refined_prompt_table.csv --output-dir data/output/iterations --round-id round_01
```

Expected result:

- `data/output/iterations/round_01/next_prompt_table.csv`
- `data/output/iterations/round_01/iteration_report.md`
- `data/output/iterations/round_01/iteration_manifest.json`

Check: open `data/output/iterations/round_01/next_prompt_table.csv` and compare it with `data/output/refined_prompt_table.csv`.

This command calls Ollama. The iteration script does not generate images or videos. It only creates the next-round prompt package based on human problem records and optimization directions.

## How to Run in Jupyter

Jupyter execution is the visual demonstration workflow. It calls the same `.py` scripts, displays inputs and outputs below notebook cells, and still writes the generated files to `data/output/`.

Start Jupyter:

```bash
jupyter notebook presentation/llm_io_demo.ipynb
```

Then run the notebook cells from top to bottom.

The notebook demonstrates this loop:

```text
problem_records -> iterate_prompts.py -> local Ollama API -> next-round prompt table
```

What the notebook shows:

- the project path and selected feedback text,
- the feedback file written to `data/input/problem_records/<round_id>/feedback.md`,
- the exact Python command used for iteration,
- stdout and stderr from `src/iterate_prompts.py`,
- the output paths under `data/output/iterations/<round_id>/`,
- a table preview of `next_prompt_table.csv`,
- the first part of `iteration_report.md`.

Each notebook run generates a timestamped `round_id`, so previous iteration outputs are not overwritten.

The notebook is not a replacement for the project scripts. It is a presentation and inspection layer over the same reproducible `.py` workflow.

## Input Files

| File | Location | Description |
| --- | --- | --- |
| `story_script.md` | `data/input/story_script.md` | Story input for Stage 1 script-to-prompt generation |
| `prompt_image_video.xlsx` | `data/input/prompt_image_video.xlsx` | Original workbook containing prompt process, final prompts, tool choices, reference paths, and output paths |
| `project_config.json` | `data/input/project_config.json` | Structured config generated from the workbook |
| `workbook_nonempty_cells.json` | `data/input/workbook_nonempty_cells.json` | Audit extraction of non-empty workbook cells |
| Problem records | `data/input/problem_records/` | Human-written issues and optimization directions after reviewing generated media |
| Reference images and clips | `data/input/source_package/` | Original production assets and selected generated clips |
| Final video | `data/input/media/final_video.mp4` | Final exported video |

Declared media paths are validated in Stage 2 because the refinement step claims to be grounded in existing images and clips. The validation does not prove that a video was generated from a specific prompt; it only prevents the workflow from citing missing assets as evidence. If a declared reference path is wrong, the program stops instead of producing an unsupported refinement package.

## Output Files

| File | Location | Description |
| --- | --- | --- |
| `generated_prompt_table.csv` | `data/output/generated_prompt_table.csv` | Stage 1 prompt table generated from the story script before asset grounding |
| `script_to_prompt_plan.md` | `data/output/script_to_prompt_plan.md` | Markdown plan for the 0-to-0.5 script-to-prompt stage |
| `stage1_generation_manifest.json` | `data/output/stage1_generation_manifest.json` | Machine-readable record of the Stage 1 generation outputs |
| `prompt_table.csv` | `data/output/prompt_table.csv` | Shot-by-shot prompt table for review and submission evidence |
| `source_prompt_table.csv` | `data/output/source_prompt_table.csv` | Source prompts preserved from the workbook as audit evidence |
| `refined_prompt_table.csv` | `data/output/refined_prompt_table.csv` | Refined manual-upload prompts generated from the source prompts and declared assets |
| `refinement_report.md` | `data/output/refinement_report.md` | Explanation of the 0.5-to-1 refinement workflow and shot-level readiness |
| `iteration_log.md` | `data/output/iteration_log.md` | Human-readable prompt iteration record |
| `iteration_log.json` | `data/output/iteration_log.json` | Machine-readable iteration history and latest Ollama output |
| `production_manifest.json` | `data/output/production_manifest.json` | Project metadata, shot count, declared assets, and generated file list |
| `storyboard.json` | `data/output/storyboard.json` | Raw Ollama storyboard summary output |
| `wedavinci_upload_prompts.md` | `data/output/wedavinci_upload_prompts.md` | Human-readable prompt package for manual video-tool upload |
| `next_prompt_table.csv` | `data/output/iterations/<round_id>/next_prompt_table.csv` | Next-round prompts generated from human problem records and optimization suggestions |
| `iteration_report.md` | `data/output/iterations/<round_id>/iteration_report.md` | Shot-level summary of detected feedback and revision strategy |

## Reproducing the Results

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies with `pip install -r requirements.txt`.
4. Start Ollama and make sure `gemma3:1b` is available, or edit `data/input/project_config.json` to use another local model.
5. Run `src/generate_from_script.py` to generate the Stage 1 prompt plan from `story_script.md`.
6. Rebuild the config from the workbook with `src/build_config_from_workbook.py`.
7. Run `src/main.py` to generate the Stage 2 refinement outputs in `data/output/`.
8. Review `generated_prompt_table.csv`, `source_prompt_table.csv`, `refined_prompt_table.csv`, and `refinement_report.md`.
9. Manually upload or paste the selected refined prompts into WeDaVinci, PixVerse.ai, Seedance, or another chosen AI video tool.
10. If the generated media is unsatisfactory, write feedback in `data/input/problem_records/` and run `src/iterate_prompts.py`.
11. Use `data/output/iterations/<round_id>/next_prompt_table.csv` for the next manual generation attempt.
12. Save generated clips, edit them manually, and export the final video.

## Additional Documentation

- Technical documentation: `docs/technical_documentation.md`

## Presentation

Presentation file: `presentation/the-last-data_final_presentation.pptx`

Final video: `data/input/media/final_video.mp4`

## Important Notes

- Video generation is manual and may use WeDaVinci, PixVerse.ai, Seedance, or another selected tool.
- The local Ollama model is used for Stage 1 script-to-prompt planning and Stage 2 refinement-oriented prompt-structure support. The source prompts are preserved in `source_prompt_table.csv`; refined manual-upload prompts are written to `refined_prompt_table.csv` and `wedavinci_upload_prompts.md`.
- Stage 1 does not change existing image references. The final video can still be based on the current images and selected clips.
- The code does not upload private credentials.
- The program fails explicitly for missing declared files instead of silently ignoring them.
- Some original workbook text and extracted paths may preserve the encoding of the submitted source files. The original workbook is included for auditability.

## Troubleshooting

| Problem | Possible Solution |
| --- | --- |
| Ollama connection fails | Check that `ollama serve` is running and that `ollama.base_url` is correct in `project_config.json` |
| Model not found | Pull the configured model with `ollama pull gemma3:1b` or update `ollama.text_model` |
| File not found error | Check that every declared `image_path` and `video_path` exists relative to `data/input/` |
| Empty or vague Ollama output | Use a stronger local Ollama model and rerun `src/main.py` |
