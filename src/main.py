from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

from ollama_client import OllamaClient


SYSTEM_PROMPT = """You are assisting an academic AI-video project.

Your task is to convert provided project metadata, shot prompts, image references,
and video-shot notes into structured production material for manual WeDaVinci upload.

Integrity rules:
- Do not invent missing scenes, assets, dialogue, or model outputs.
- Preserve the declared shot order.
- If a prompt is ambiguous, mark it as a risk instead of silently resolving it.
- Keep image-generation prompts separate from image-to-video prompts.
- Produce content that is reproducible from the provided config.
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
        "Create a concise Markdown storyboard summary for this AI video project. "
        "Do not answer only OK. Use exactly these sections: Story Premise, Shot-by-Shot Storyboard, "
        "Manual Video Production Notes, Continuity Risks. "
        "Do not invent character names, tools, file paths, dialogue, or assets. "
        "Refer to the characters only as Protagonist and Boss. "
        "The manual production tools are exactly the tools listed in the shot list.\n\n"
        f"Project: {project.get('title', '')}\n"
        f"Source script: {config.get('source_script', '')}\n"
        f"Workflow constraints: {json.dumps(constraints, ensure_ascii=False)}\n"
        f"Shots: {json.dumps(compact_shots, ensure_ascii=False)}"
    )


def write_prompt_table(output_dir: Path, shots: list[dict[str, Any]]) -> None:
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
    with (output_dir / "prompt_table.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for shot in shots:
            writer.writerow({field: shot.get(field, "") for field in fields})


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
    write_prompt_table(output_dir, shots)
    write_iteration_log(output_dir, config, ollama_text)
    public_shots = [
        {key: value for key, value in shot.items() if not key.endswith("_resolved")}
        for shot in shots
    ]

    manifest = {
        "project": config.get("project", {}),
        "workflow_parts": [
            "Part 1: Code/NLP workflow with local Ollama prompt generation",
            "Part 2: Manual AI video production workflow in WeDaVinci or another selected tool",
        ],
        "source_script": config.get("source_script", ""),
        "shot_count": len(shots),
        "shots": public_shots,
        "generated_files": [
            "storyboard.json",
            "production_manifest.json",
            "wedavinci_upload_prompts.md",
            "prompt_table.csv",
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
        "note": "The local LLM receives compact shot excerpts. Full prompts are preserved in prompt_table.csv and production_manifest.json.",
        "raw_model_output": ollama_text,
    }
    (output_dir / "storyboard.json").write_text(
        json.dumps(storyboard_payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    markdown = [
        "# WeDaVinci Manual Upload Prompts",
        "",
        "This file was generated from the local project configuration, original prompt workbook, and Ollama output.",
        "Video generation is manual and is not automated by this repository.",
        "",
        "## Source Prompt Table",
        "",
    ]
    for shot in shots:
        markdown.extend(
            [
                f"### {shot.get('id', '')}: {shot.get('title', '')}",
                "",
                f"- Tool: {shot.get('tool', '')}",
                f"- Method: {shot.get('method', '')}",
                f"- Image reference: {shot.get('image_path', '') or 'not declared'}",
                f"- Video output: {shot.get('video_path', '') or 'not declared'}",
                "",
                "Image prompt:",
                "",
                str(shot.get("image_prompt", "")).strip() or "not declared",
                "",
                "Video prompt:",
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
