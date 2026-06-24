from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

from ollama_client import OllamaClient


SYSTEM_PROMPT = """You are assisting an academic AI-video project.

Your task is to help refine an existing half-finished AI-video production package.
The project already contains a story premise, draft prompts, reference images,
selected generated clips, and iteration notes. Treat these as source evidence.

Integrity rules:
- Do not invent missing scenes, assets, dialogue, or model outputs.
- Preserve the declared shot order.
- If a prompt is ambiguous, mark it as a risk instead of silently resolving it.
- Keep image-generation prompts separate from image-to-video prompts.
- Produce content that is reproducible from the provided config.
- Present the workflow as "0.5 to 1 refinement", not as "0 to 1 generation".
"""


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Config file does not exist: {path}")
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("Config root must be a JSON object.")
    return data


def resolve_project_path(config_path: Path, value: str | None) -> Path | None:
    if value is None or value == "":
        return None
    path = Path(value)
    if path.is_absolute():
        return path
    return (config_path.parent / path).resolve()


def validate_config(config: dict[str, Any], config_path: Path) -> list[dict[str, Any]]:
    shots = config.get("shots")
    if not isinstance(shots, list) or not shots:
        raise ValueError("Config must contain a non-empty shots list.")

    validated: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for index, shot in enumerate(shots, start=1):
        if not isinstance(shot, dict):
            raise ValueError(f"Shot {index} must be a JSON object.")

        shot_id = shot.get("id")
        if not isinstance(shot_id, str) or not shot_id.strip():
            raise ValueError(f"Shot {index} is missing a non-empty id.")
        if shot_id in seen_ids:
            raise ValueError(f"Duplicate shot id: {shot_id}")
        seen_ids.add(shot_id)

        image_path = resolve_project_path(config_path, shot.get("image_path"))
        video_path = resolve_project_path(config_path, shot.get("video_path"))
        for label, path in [("image_path", image_path), ("video_path", video_path)]:
            if path is not None and not path.exists():
                raise FileNotFoundError(f"{label} for shot {shot_id} does not exist: {path}")

        image_prompt = shot.get("image_prompt")
        video_prompt = shot.get("video_prompt")
        if not isinstance(image_prompt, str) or not image_prompt.strip():
            raise ValueError(f"Shot {shot_id} is missing image_prompt.")
        if not isinstance(video_prompt, str) or not video_prompt.strip():
            raise ValueError(f"Shot {shot_id} is missing video_prompt.")

        validated.append(
            {
                **shot,
                "image_path_resolved": str(image_path) if image_path else None,
                "video_path_resolved": str(video_path) if video_path else None,
            }
        )
    return validated


def excerpt(value: str, max_chars: int = 1200) -> str:
    if len(value) <= max_chars:
        return value
    return value[:max_chars].rstrip() + "\n[TRUNCATED_FOR_LLM_CONTEXT; full prompt is preserved in prompt_table.csv and production_manifest.json]"


def build_generation_prompt(config: dict[str, Any], shots: list[dict[str, Any]]) -> str:
    project = config.get("project", {})
    constraints = config.get("global_constraints", [])
    compact_shots = [
        {
            "id": shot.get("id", ""),
            "title": shot.get("title", ""),
            "tool": shot.get("tool", ""),
            "method": shot.get("method", ""),
        }
        for shot in shots
    ]
    return (
        "Create a concise Markdown refinement summary for this half-finished AI video project. "
        "Do not answer only OK. Use exactly these sections: Story Premise, Shot-by-Shot Storyboard, "
        "Manual Video Production Notes, Continuity Risks, Refinement Strategy. "
        "Do not invent character names, tools, file paths, dialogue, or assets. "
        "Refer to the characters only as Protagonist and Boss. "
        "The manual production tools are exactly the tools listed in the shot list.\n\n"
        f"Project: {project.get('title', '')}\n"
        f"Source script: {config.get('source_script', '')}\n"
        f"Workflow constraints: {json.dumps(constraints, ensure_ascii=False)}\n"
        f"Shots: {json.dumps(compact_shots, ensure_ascii=False)}"
    )


def write_prompt_table(output_dir: Path, shots: list[dict[str, Any]], filename: str = "prompt_table.csv") -> None:
    fields = [
        "id",
        "title",
        "time_range",
        "image_prompt",
        "video_prompt",
        "notes",
        "image_path",
        "video_path",
    ]
    with (output_dir / filename).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for shot in shots:
            writer.writerow({field: shot.get(field, "") for field in fields})


def build_refinement_constraints(config: dict[str, Any], shot: dict[str, Any]) -> list[str]:
    project = config.get("project", {})
    aspect_ratio = project.get("aspect_ratio", "9:16")
    constraints = [
        f"Keep the declared shot id and story position: {shot.get('id', '')}.",
        f"Keep the manual generation tool and method: {shot.get('tool', '')} / {shot.get('method', '')}.",
        f"Keep the target aspect ratio: {aspect_ratio}.",
        "Preserve the existing protagonist, boss, office, ruins, hard drive, and reconstruction continuity when they are present in the source prompt.",
        "Do not add new scenes, characters, props, dialogue, or video-platform actions that are not supported by the source workbook.",
    ]
    if shot.get("image_path"):
        constraints.append(f"Use the declared image reference as visual evidence: {shot['image_path']}.")
    if shot.get("video_path"):
        constraints.append(f"Use the declared generated clip as the existing production state: {shot['video_path']}.")
    return constraints


def refined_prompt(source_prompt: str, constraints: list[str]) -> str:
    source_prompt = source_prompt.strip()
    constraint_text = "\n".join(f"- {item}" for item in constraints)
    return (
        "Refined manual-upload prompt based on the existing source material.\n\n"
        "Source prompt:\n"
        f"{source_prompt}\n\n"
        "Refinement constraints:\n"
        f"{constraint_text}\n\n"
        "Production instruction:\n"
        "Improve consistency, motion clarity, camera continuity, and tool readability while preserving the source scene and declared assets."
    )


def risk_notes(shot: dict[str, Any]) -> str:
    risks: list[str] = []
    if not shot.get("image_path"):
        risks.append("No declared image reference; manual reviewer should verify visual continuity.")
    if not shot.get("video_path"):
        risks.append("No declared generated clip; this shot may still require manual generation.")
    if len(str(shot.get("video_prompt", ""))) > 1800:
        risks.append("Long video prompt; manual uploader may need to split or shorten it for the target platform.")
    if not risks:
        risks.append("Ready for manual review and upload.")
    return " ".join(risks)


def build_refined_shots(config: dict[str, Any], shots: list[dict[str, Any]]) -> list[dict[str, Any]]:
    refined: list[dict[str, Any]] = []
    for shot in shots:
        constraints = build_refinement_constraints(config, shot)
        refined.append(
            {
                **shot,
                "source_image_prompt": shot.get("image_prompt", ""),
                "source_video_prompt": shot.get("video_prompt", ""),
                "image_prompt": refined_prompt(str(shot.get("image_prompt", "")), constraints),
                "video_prompt": refined_prompt(str(shot.get("video_prompt", "")), constraints),
                "notes": f"{shot.get('notes', '')} | Refinement status: {risk_notes(shot)}".strip(" |"),
            }
        )
    return refined


def write_refined_prompt_table(output_dir: Path, refined_shots: list[dict[str, Any]]) -> None:
    fields = [
        "id",
        "title",
        "tool",
        "method",
        "source_image_prompt",
        "refined_image_prompt",
        "source_video_prompt",
        "refined_video_prompt",
        "image_path",
        "video_path",
        "notes",
    ]
    with (output_dir / "refined_prompt_table.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for shot in refined_shots:
            writer.writerow(
                {
                    "id": shot.get("id", ""),
                    "title": shot.get("title", ""),
                    "tool": shot.get("tool", ""),
                    "method": shot.get("method", ""),
                    "source_image_prompt": shot.get("source_image_prompt", ""),
                    "refined_image_prompt": shot.get("image_prompt", ""),
                    "source_video_prompt": shot.get("source_video_prompt", ""),
                    "refined_video_prompt": shot.get("video_prompt", ""),
                    "image_path": shot.get("image_path", ""),
                    "video_path": shot.get("video_path", ""),
                    "notes": shot.get("notes", ""),
                }
            )


def write_refinement_report(output_dir: Path, refined_shots: list[dict[str, Any]], ollama_text: str) -> None:
    lines = [
        "# Prompt Refinement Report",
        "",
        "## Workflow Position",
        "",
        "This project uses a two-stage 0-to-1 AI-video prompt workflow. Stage 1 generates an initial shot and prompt plan from the story script. Stage 2 refines the prompt package using existing draft prompts, reference images, selected clips, and iteration notes.",
        "",
        "Stage 1 does not create or replace image/video files. The existing images remain the grounding assets for Stage 2 refinement and for manual video generation.",
        "",
        "## Generated Refinement Artifacts",
        "",
        "- `generated_prompt_table.csv`: first-pass 0-to-0.5 prompts generated from the story script.",
        "- `source_prompt_table.csv`: the source workbook prompts preserved as evidence.",
        "- `refined_prompt_table.csv`: manual-upload prompts rebuilt from the source prompts with continuity, asset, and tool constraints.",
        "- `wedavinci_upload_prompts.md`: human-readable refined prompt package for manual upload.",
        "- `production_manifest.json`: reproducible inventory of inputs, outputs, and declared assets.",
        "",
        "## Shot-Level Readiness",
        "",
    ]
    for shot in refined_shots:
        lines.extend(
            [
                f"### {shot.get('id', '')}: {shot.get('title', '')}",
                "",
                f"- Tool: {shot.get('tool', '')}",
                f"- Method: {shot.get('method', '')}",
                f"- Image reference: {shot.get('image_path', '') or 'not declared'}",
                f"- Existing clip: {shot.get('video_path', '') or 'not declared'}",
                f"- Notes: {shot.get('notes', '')}",
                "",
            ]
        )
    lines.extend(["## Ollama Refinement Summary", "", ollama_text, ""])
    (output_dir / "refinement_report.md").write_text("\n".join(lines), encoding="utf-8")


def write_iteration_log(output_dir: Path, config: dict[str, Any], ollama_text: str) -> None:
    iterations = config.get("iteration_history", [])
    if not isinstance(iterations, list):
        raise ValueError("iteration_history must be a list if provided.")

    payload = {
        "declared_iterations": iterations,
        "current_ollama_generation": {
            "description": "Latest LLM-assisted prompt-structuring output.",
            "raw_model_output": ollama_text,
        },
    }
    (output_dir / "iteration_log.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    lines = ["# Iteration Log", ""]
    if iterations:
        for item in iterations:
            if not isinstance(item, dict):
                raise ValueError("Each iteration_history entry must be an object.")
            lines.extend(
                [
                    f"## {item.get('version', 'unknown version')}",
                    "",
                    f"- Date: {item.get('date', '')}",
                    f"- Change: {item.get('change', '')}",
                    f"- Reason: {item.get('reason', '')}",
                    f"- Result: {item.get('result', '')}",
                    "",
                ]
            )
    else:
        lines.extend(["No manual iteration history was declared in the input config.", ""])

    lines.extend(["## Latest Ollama Output", "", ollama_text, ""])
    (output_dir / "iteration_log.md").write_text("\n".join(lines), encoding="utf-8")


def write_outputs(output_dir: Path, config: dict[str, Any], shots: list[dict[str, Any]], ollama_text: str) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    refined_shots = build_refined_shots(config, shots)
    write_prompt_table(output_dir, shots)
    write_prompt_table(output_dir, shots, "source_prompt_table.csv")
    write_refined_prompt_table(output_dir, refined_shots)
    write_refinement_report(output_dir, refined_shots, ollama_text)
    write_iteration_log(output_dir, config, ollama_text)
    public_shots = [
        {key: value for key, value in shot.items() if not key.endswith("_resolved")}
        for shot in shots
    ]
    public_refined_shots = [
        {key: value for key, value in shot.items() if not key.endswith("_resolved")}
        for shot in refined_shots
    ]
    stage1_files = [
        "generated_prompt_table.csv",
        "script_to_prompt_plan.md",
        "stage1_generation_manifest.json",
    ]
    existing_stage1_files = [name for name in stage1_files if (output_dir / name).exists()]

    manifest = {
        "project": config.get("project", {}),
        "workflow_mode": "0-to-1 AI-video prompt workflow: 0-to-0.5 script-to-prompt generation plus 0.5-to-1 asset-grounded refinement",
        "workflow_parts": [
            "Stage 1: 0-to-0.5 script-to-prompt generation from story_script.md; this stage writes prompt artifacts only and does not modify media assets",
            "Stage 2: 0.5-to-1 refinement that reads existing draft prompts, reference images, generated clips, and iteration notes",
            "Code/NLP output: generated prompt table, source prompt table, refined prompt table, refinement report, storyboard summary, and production manifest",
            "Part 2: Manual AI video production workflow in WeDaVinci or another selected tool",
        ],
        "source_script": config.get("source_script", ""),
        "shot_count": len(shots),
        "shots": public_shots,
        "refined_shots": public_refined_shots,
        "generated_files": [
            *existing_stage1_files,
            "storyboard.json",
            "production_manifest.json",
            "wedavinci_upload_prompts.md",
            "prompt_table.csv",
            "source_prompt_table.csv",
            "refined_prompt_table.csv",
            "refinement_report.md",
            "iteration_log.json",
            "iteration_log.md",
        ],
    }

    (output_dir / "production_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    storyboard_payload = {
        "source": "ollama",
        "note": "The local LLM receives compact shot excerpts for refinement-oriented summarization. Full source prompts are preserved in source_prompt_table.csv and production_manifest.json; refined prompts are written to refined_prompt_table.csv.",
        "raw_model_output": ollama_text,
    }
    (output_dir / "storyboard.json").write_text(
        json.dumps(storyboard_payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    markdown = [
        "# Refined Manual Upload Prompts",
        "",
        "This file was generated from the local project configuration, original prompt workbook, declared reference assets, existing clips, and Ollama output.",
        "It is the Stage 2 output in a two-stage workflow: Stage 1 generates a first script-to-prompt plan, and Stage 2 refines prompts using existing image/video evidence.",
        "Existing images and selected clips are not replaced by the code; they remain the grounding assets for manual video generation.",
        "Video generation is manual and is not automated by this repository.",
        "",
        "## Refined Prompt Package",
        "",
    ]
    for shot in refined_shots:
        markdown.extend(
            [
                f"### {shot.get('id', '')}: {shot.get('title', '')}",
                "",
                f"- Tool: {shot.get('tool', '')}",
                f"- Method: {shot.get('method', '')}",
                f"- Image reference: {shot.get('image_path', '') or 'not declared'}",
                f"- Video output: {shot.get('video_path', '') or 'not declared'}",
                "",
                "Refined image prompt:",
                "",
                str(shot.get("image_prompt", "")).strip() or "not declared",
                "",
                "Refined video prompt:",
                "",
                str(shot.get("video_prompt", "")).strip() or "not declared",
                "",
            ]
        )
    markdown.extend(
        [
            "## Ollama Storyboard Summary",
            "",
            ollama_text,
            "",
        ]
    )
    (output_dir / "wedavinci_upload_prompts.md").write_text("\n".join(markdown), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate AI-video production prompts with local Ollama.")
    parser.add_argument("--config", required=True, type=Path, help="Path to project_config.json.")
    parser.add_argument("--output", required=True, type=Path, help="Directory for generated outputs.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate config and write manifest without calling Ollama.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config_path = args.config.resolve()
    config = read_json(config_path)
    shots = validate_config(config, config_path)

    if args.dry_run:
        ollama_text = "DRY RUN: config validated successfully; Ollama was not called."
    else:
        ollama_config = config.get("ollama", {})
        base_url = ollama_config.get("base_url")
        text_model = ollama_config.get("text_model")
        if not isinstance(base_url, str) or not base_url:
            raise ValueError("Config must define ollama.base_url.")
        if not isinstance(text_model, str) or not text_model:
            raise ValueError("Config must define ollama.text_model.")
        api_mode = ollama_config.get("api_mode", "chat")
        if api_mode not in {"chat", "generate"}:
            raise ValueError("ollama.api_mode must be either 'chat' or 'generate'.")

        client = OllamaClient(base_url)
        if api_mode == "chat":
            ollama_text = client.chat(
                model=text_model,
                system_prompt=SYSTEM_PROMPT,
                user_prompt=build_generation_prompt(config, shots),
            )
        else:
            ollama_text = client.generate(
                model=text_model,
                system_prompt=SYSTEM_PROMPT,
                user_prompt=build_generation_prompt(config, shots),
            )

    write_outputs(args.output.resolve(), config, shots, ollama_text)
    print(f"Wrote outputs to {args.output.resolve()}")


if __name__ == "__main__":
    main()
