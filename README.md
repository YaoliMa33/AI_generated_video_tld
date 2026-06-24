# The Last Data

This repository contains the code and documentation for a two-part AI video assignment workflow. The Code/NLP part is now framed as a **two-stage 0-to-1 prompt workflow**:

1. **0-to-0.5 script-to-prompt generation**: start from a story script and generate an initial shot plan, text-to-image prompts, and image-to-video prompts.
2. **0.5-to-1 asset-grounded refinement**: use the existing prompt workbook, reference images, selected generated clips, and iteration notes to validate and refine the production package.

Part 1 is the **Code/NLP Workflow**. Python programs read the source script, prompt workbook, scene notes, reference images, generated clip paths, and iteration notes. They call a local Ollama LLM API and save generated prompts, source prompts, refined prompts, a storyboard/refinement summary, production manifest, and iteration log.

Part 2 is the **Manual AI Video Production Workflow**. The final prompts are entered manually into AI video tools such as WeDaVinci, PixVerse.ai, and Seedance. The generated clips are saved, edited, and exported as the final video and presentation.

The repository does not automate WeDaVinci, PixVerse.ai, or Seedance access. No platform credentials, cookies, or private API tokens are stored in this project.

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
|       `-- wedavinci_upload_prompts.md
|-- docs/
|   `-- technical_documentation.md
`-- presentation/
```

| Path | Description |
| --- | --- |
| `src/generate_from_script.py` | Stage 1: generates a first shot/prompt plan from `story_script.md` |
| `src/build_config_from_workbook.py` | Converts the prompt workbook into `data/input/project_config.json` |
| `src/main.py` | Validates the config, calls Ollama, writes source prompt artifacts, and generates refined manual-upload prompts |
| `src/ollama_client.py` | Local Ollama HTTP API client |
| `data/input/prompt_image_video.xlsx` | Original prompt/process workbook |
| `data/input/source_package/` | Original prompt package with reference images and generated clips |
| `data/input/media/final_video.mp4` | Final exported video provided for submission |
| `data/output/` | Generated prompt table, iteration log, manifest, storyboard, and manual upload package |
| `docs/` | Technical workflow documentation |

## Requirements

- Python 3.10 or newer
- Python package listed in `requirements.txt`: `openpyxl`
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

## How to Run the Project

First generate the 0-to-0.5 prompt plan from the story script:

```bash
python src/generate_from_script.py --script data/input/story_script.md --output data/output
```

This writes `generated_prompt_table.csv`, `script_to_prompt_plan.md`, and `stage1_generation_manifest.json`. It does not create or modify image/video assets.

Then rebuild the structured project config from the prompt workbook:

```bash
python src/build_config_from_workbook.py --workbook data/input/prompt_image_video.xlsx --input-dir data/input --output data/input/project_config.json
```

Validate the config without calling Ollama:

```bash
python src/main.py --config data/input/project_config.json --output data/output --dry-run
```

Generate the production files through Ollama:

```bash
python src/main.py --config data/input/project_config.json --output data/output
```

The scripts write the generated prompt table, source prompt table, refined prompt table, iteration log, storyboard/refinement summary, production manifest, and manual upload prompt package to `data/output/`.

## Input Files

| File | Location | Description |
| --- | --- | --- |
| `story_script.md` | `data/input/story_script.md` | Story input for Stage 1 script-to-prompt generation |
| `prompt_image_video.xlsx` | `data/input/prompt_image_video.xlsx` | Original workbook containing prompt process, final prompts, tool choices, reference paths, and output paths |
| `project_config.json` | `data/input/project_config.json` | Structured config generated from the workbook |
| `workbook_nonempty_cells.json` | `data/input/workbook_nonempty_cells.json` | Audit extraction of non-empty workbook cells |
| Reference images and clips | `data/input/source_package/` | Original production assets and selected generated clips |
| Final video | `data/input/media/final_video.mp4` | Final exported video |

All declared media paths are validated. If a path is declared but the file does not exist, the program stops with an explicit error.

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
10. Save generated clips, edit them manually, and export the final video.

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
