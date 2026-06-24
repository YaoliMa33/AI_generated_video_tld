from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

from ollama_client import OllamaClient


SYSTEM_PROMPT = """You are assisting an academic AI-video project.

Your task is the 0-to-0.5 stage: transform a story script into a first
AI-video prompt plan. This stage creates a shot plan, text-to-image prompts,
image-to-video prompts, and continuity constraints. It must not claim that
images or clips already exist.

Integrity rules:
- Do not invent generated files, reference images, or finished clips.
- Keep the output focused on prompt planning for manual AI-video generation.
- Separate text-to-image prompts from image-to-video prompts.
- Preserve the story premise and avoid adding unsupported characters or props.
- Make the plan useful for a later 0.5-to-1 refinement stage using real assets.
"""


SHOT_BLUEPRINTS = [
    {
        "id": "s1-1",
        "title": "Office data routine",
        "time_range": "0-6s",
        "story_function": "Establish the future data office and the protagonist's repetitive upload work.",
        "tool": "manual text-to-image, then image-to-video",
        "method": "text-to-image-to-video",
    },
    {
        "id": "s1-2",
        "title": "Boss pressure",
        "time_range": "6-12s",
        "story_function": "Show the boss pressuring the protagonist to keep uploading data.",
        "tool": "manual text-to-image, then image-to-video",
        "method": "text-to-image-to-video",
    },
    {
        "id": "s1-3",
        "title": "Extinction alert",
        "time_range": "12-18s",
        "story_function": "Introduce the emergency alert while the office routine continues.",
        "tool": "manual text-to-image, then image-to-video",
        "method": "text-to-image-to-video",
    },
    {
        "id": "s2-1",
        "title": "Hand tension",
        "time_range": "18-21s",
        "story_function": "Use a close-up of the protagonist's hand to show suppressed anger.",
        "tool": "manual image-to-video",
        "method": "image-to-video",
    },
    {
        "id": "s2-2",
        "title": "Impact transition",
        "time_range": "21-25s",
        "story_function": "Transition from office conflict to catastrophe.",
        "tool": "manual image-to-video or transition generation",
        "method": "image-to-video",
    },
    {
        "id": "s2-3",
        "title": "Confrontation",
        "time_range": "25-33s",
        "story_function": "The protagonist confronts the boss and questions the value of the work.",
        "tool": "manual image-to-video",
        "method": "image-to-video",
    },
    {
        "id": "s3-1",
        "title": "Waking in ruins",
        "time_range": "33-45s",
        "story_function": "The protagonist wakes after the catastrophe and sees the destroyed city.",
        "tool": "manual image-to-video",
        "method": "image-to-video",
    },
    {
        "id": "s3-2",
        "title": "Civilization archive activation",
        "time_range": "45-53s",
        "story_function": "The protagonist discovers and activates the CIVILIZATION ARCHIVE hard drive.",
        "tool": "manual image-to-video",
        "method": "image-to-video",
    },
    {
        "id": "s4",
        "title": "Holographic reconstruction",
        "time_range": "53-70s",
        "story_function": "Blue holographic architectural data rebuilds the city from the ruins.",
        "tool": "manual image-to-video",
        "method": "image-to-video",
    },
]


def read_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Story script does not exist: {path}")
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError(f"Story script is empty: {path}")
    return text


def build_llm_prompt(story_script: str) -> str:
    return (
        "Create a concise Markdown prompt-generation plan for this AI-video story. "
        "Use exactly these sections: Story Logline, Visual Continuity Bible, Shot Plan, Prompting Risks. "
        "Do not mention existing files, reference images, or generated clips. "
        "The plan is for a later manual AI-video workflow.\n\n"
        f"Story script:\n{story_script}"
    )


def image_prompt_for(shot: dict[str, str], story_script: str) -> str:
    base_style = (
        "vertical 9:16 cinematic frame, photorealistic sci-fi disaster film style, "
        "controlled composition, clear subject hierarchy, no subtitles, no watermark"
    )
    continuity = (
        "Continuity: same exhausted protagonist, same bureaucratic boss when present, "
        "same black CIVILIZATION ARCHIVE hard drive when present, cold blue data-office palette before the impact, "
        "ash-gray ruin palette after the impact, blue holographic reconstruction light in the final sequence."
    )
    return (
        f"{shot['title']}. {shot['story_function']} "
        f"Create a still image that can become the first frame of this shot. "
        f"{continuity} Style: {base_style}. "
        f"Story context: {story_script}"
    )


def video_prompt_for(shot: dict[str, str]) -> str:
    motion_rules = {
        "s1-1": "Slow push-in through the future data office; screens flicker subtly while the protagonist repeats the upload routine.",
        "s1-2": "Maintain the same office layout; the boss leans in and points toward the upload progress while the protagonist stays tense and silent.",
        "s1-3": "Red alert light enters the blue office lighting; the characters react to the broadcast before anyone moves.",
        "s2-1": "Close-up motion only; fingers curl into a fist, knuckles whiten, slight tremor, no camera cut.",
        "s2-2": "A sudden shockwave and debris transition covers the frame, connecting the office conflict to the catastrophe.",
        "s2-3": "Handheld confrontation energy; the protagonist grabs the boss, office objects scatter, red warning light intensifies.",
        "s3-1": "First-person awakening rhythm; blurred darkness opens into ruins, then slowly rises toward a destroyed city view.",
        "s3-2": "Macro focus on the hard drive; dust is wiped away, blue startup light activates, scanning light crosses the surface.",
        "s4": "One-shot reconstruction movement; blue holographic wireframes rise from ruins, architectural data rebuilds city forms.",
    }
    return (
        f"{shot['title']}. {motion_rules[shot['id']]} "
        "Preserve character and environment continuity. Use smooth, physically plausible camera motion. "
        "Do not add unsupported characters, logos, subtitles, or unrelated props."
    )


def build_generated_shots(story_script: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for shot in SHOT_BLUEPRINTS:
        rows.append(
            {
                "id": shot["id"],
                "title": shot["title"],
                "time_range": shot["time_range"],
                "tool": shot["tool"],
                "method": shot["method"],
                "story_function": shot["story_function"],
                "image_prompt": image_prompt_for(shot, story_script),
                "video_prompt": video_prompt_for(shot),
                "asset_status": "generated prompt only; no image or video asset is created or overwritten in stage 0-to-0.5",
            }
        )
    return rows


def write_generated_prompt_table(output_dir: Path, rows: list[dict[str, str]]) -> None:
    fields = [
        "id",
        "title",
        "time_range",
        "tool",
        "method",
        "story_function",
        "image_prompt",
        "video_prompt",
        "asset_status",
    ]
    with (output_dir / "generated_prompt_table.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_plan_markdown(output_dir: Path, story_script: str, rows: list[dict[str, str]], llm_text: str) -> None:
    lines = [
        "# 0-to-0.5 Script-to-Prompt Generation Plan",
        "",
        "This stage starts from the story script and generates a first prompt plan. It does not generate, replace, or overwrite any image or video asset.",
        "",
        "## Story Script",
        "",
        story_script,
        "",
        "## Generated Shot Prompts",
        "",
    ]
    for row in rows:
        lines.extend(
            [
                f"### {row['id']}: {row['title']}",
                "",
                f"- Time range: {row['time_range']}",
                f"- Tool/method: {row['tool']} / {row['method']}",
                f"- Story function: {row['story_function']}",
                f"- Asset status: {row['asset_status']}",
                "",
                "Image prompt:",
                "",
                row["image_prompt"],
                "",
                "Video prompt:",
                "",
                row["video_prompt"],
                "",
            ]
        )
    lines.extend(["## Ollama Generation Notes", "", llm_text, ""])
    (output_dir / "script_to_prompt_plan.md").write_text("\n".join(lines), encoding="utf-8")


def write_manifest(output_dir: Path, story_path: Path, rows: list[dict[str, str]], llm_text: str) -> None:
    manifest: dict[str, Any] = {
        "workflow_stage": "0-to-0.5 script-to-prompt generation",
        "story_script": str(story_path).replace("\\", "/"),
        "shot_count": len(rows),
        "asset_policy": "This stage writes prompt artifacts only. It does not create, modify, or replace image/video assets.",
        "generated_files": [
            "generated_prompt_table.csv",
            "script_to_prompt_plan.md",
            "stage1_generation_manifest.json",
        ],
        "ollama_generation_notes": llm_text,
        "shots": rows,
    }
    (output_dir / "stage1_generation_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a 0-to-0.5 AI-video prompt plan from a story script.")
    parser.add_argument("--script", required=True, type=Path, help="Path to the story script or creative brief.")
    parser.add_argument("--output", required=True, type=Path, help="Directory for generated output artifacts.")
    parser.add_argument("--base-url", default="http://localhost:11434", help="Local Ollama base URL.")
    parser.add_argument("--model", default="gemma3:1b", help="Local Ollama model name.")
    parser.add_argument("--dry-run", action="store_true", help="Generate deterministic prompt table without calling Ollama.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    story_path = args.script.resolve()
    output_dir = args.output.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    story_script = read_text(story_path)
    rows = build_generated_shots(story_script)

    if args.dry_run:
        llm_text = "DRY RUN: script-to-prompt table generated without calling Ollama."
    else:
        client = OllamaClient(args.base_url)
        llm_text = client.generate(
            model=args.model,
            system_prompt=SYSTEM_PROMPT,
            user_prompt=build_llm_prompt(story_script),
            temperature=0.2,
        )

    write_generated_prompt_table(output_dir, rows)
    write_plan_markdown(output_dir, story_script, rows, llm_text)
    write_manifest(output_dir, story_path, rows, llm_text)
    print(f"Wrote 0-to-0.5 prompt plan to {output_dir}")


if __name__ == "__main__":
    main()
