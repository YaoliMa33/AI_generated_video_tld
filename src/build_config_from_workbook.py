from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import openpyxl


SHOT_TITLES = {
    "s1-1": "Office establishing shot",
    "s1-2": "Office pressure and upload routine",
    "s1-3": "Emergency alert interruption",
    "s2-1": "Fist close-up",
    "s2-2": "Explosion transition",
    "s2-3": "Confrontation with boss",
    "s3-1": "Waking in the ruins",
    "s3-2": "Activating the civilization archive hard drive",
    "s4": "One-shot reconstruction",
}


def cell_text(sheet: Any, address: str) -> str:
    value = sheet[address].value
    if value is None:
        return ""
    return str(value).strip()


def clean_ref(value: str) -> str:
    return value.strip().strip('"').strip()


def normalize_workbook_reference(reference: str) -> Path:
    normalized = reference.replace("\\", "/")
    replacements = {
        "工作留痕": "work_records",
        "The_Blueprint": "the_last_data_assets",
        "image_referrence_for_seedance_s3-1": "seedance_s3_reference_images",
        "image_referrence_for_seedance_s4": "seedance_s4_reference_images",
        "shorts_need": "selected_video_clips",
        "s4 seedance_onecut.mp4": "s4_seedance_onecut.mp4",
    }
    for old, new in replacements.items():
        normalized = normalized.replace(old, new)
    return Path(normalized)


def resolve_reference(input_dir: Path, reference: str) -> Path | None:
    reference = clean_ref(reference)
    if not reference.startswith("工作留痕"):
        return None
    return input_dir / "source_package" / "video_prompt_package" / normalize_workbook_reference(reference)


def relative_to_input(input_dir: Path, path: Path) -> str:
    return str(path.relative_to(input_dir)).replace("\\", "/")


def normalized_reference_text(reference: str) -> str:
    reference = clean_ref(reference)
    if reference.startswith("工作留痕"):
        path = Path("source_package") / "video_prompt_package" / normalize_workbook_reference(reference)
        return str(path).replace("\\", "/")
    return reference


def selected_media_from_output_dir(input_dir: Path, output_dir: Path) -> tuple[str, str, str]:
    selected_videos = sorted(output_dir.glob("*selected.mp4"))
    images = sorted(output_dir.glob("*.png"))
    image_path = relative_to_input(input_dir, images[0]) if images else ""
    video_path = relative_to_input(input_dir, selected_videos[0]) if selected_videos else ""
    note = f"Output directory: {relative_to_input(input_dir, output_dir)}"
    return image_path, video_path, note


def build_shots(input_dir: Path, workbook_path: Path) -> list[dict[str, Any]]:
    workbook = openpyxl.load_workbook(workbook_path, data_only=True)
    sheet = workbook["final_input_output_videos"]
    shots: list[dict[str, Any]] = []

    for column in ["B", "C", "D", "F", "G", "H", "J", "K", "M"]:
        shot_id = cell_text(sheet, f"{column}3")
        prompt = cell_text(sheet, f"{column}5")
        method = cell_text(sheet, f"{column}6")
        tool = cell_text(sheet, f"{column}4")
        image_ref = clean_ref(cell_text(sheet, f"{column}7"))
        output_ref = clean_ref(cell_text(sheet, f"{column}8"))

        if column == "K":
            extra_cells = ["K10", "K11", "K13", "K14", "K16", "K17", "K19", "K20", "K22", "K24", "K26", "K28", "K30", "K32"]
            extra = "\n\n".join(cell_text(sheet, cell) for cell in extra_cells if cell_text(sheet, cell))
            prompt = f"{prompt}\n\n{extra}".strip()

        if not shot_id and not prompt:
            continue

        image_path = ""
        video_path = ""
        notes: list[str] = []

        image_reference_path = resolve_reference(input_dir, image_ref)
        if image_reference_path:
            if image_reference_path.is_file():
                image_path = relative_to_input(input_dir, image_reference_path)
            elif image_reference_path.is_dir():
                notes.append(f"Image reference directory: {relative_to_input(input_dir, image_reference_path)}")

        output_reference_path = resolve_reference(input_dir, output_ref)
        if output_reference_path:
            if output_reference_path.is_file() and output_reference_path.suffix.lower() == ".mp4":
                video_path = relative_to_input(input_dir, output_reference_path)
            elif output_reference_path.is_dir():
                selected_image, selected_video, note = selected_media_from_output_dir(input_dir, output_reference_path)
                image_path = image_path or selected_image
                video_path = video_path or selected_video
                notes.append(note)

        if image_ref:
            notes.append(f"Workbook image_ref normalized: {normalized_reference_text(image_ref)}")
        if output_ref:
            notes.append(f"Workbook output_ref normalized: {normalized_reference_text(output_ref)}")

        is_text_to_image = "text to image" in method.lower()
        shots.append(
            {
                "id": shot_id.replace(" ", "_"),
                "title": SHOT_TITLES.get(shot_id, shot_id),
                "time_range": "",
                "tool": tool,
                "method": method,
                "image_path": image_path,
                "video_path": video_path,
                "image_prompt": prompt if is_text_to_image else prompt,
                "video_prompt": prompt,
                "notes": " | ".join(notes),
            }
        )

    return shots


def build_iterations(workbook_path: Path) -> list[dict[str, str]]:
    workbook = openpyxl.load_workbook(workbook_path, data_only=True)
    sheet = workbook["prompt_process"]
    entries = [
        ("v1", "D23", "D24"),
        ("v2", "D25", "D27"),
        ("v3", "G29", "G30"),
    ]
    iterations: list[dict[str, str]] = []
    for version, change_cell, reason_cell in entries:
        change = cell_text(sheet, change_cell)
        reason = cell_text(sheet, reason_cell)
        if change or reason:
            iterations.append(
                {
                    "version": version,
                    "date": "2026-06-18 to 2026-06-22",
                    "change": change,
                    "reason": reason,
                    "result": "Prompt revised in prompt_image_video.xlsx and reflected in final_input_output_videos.",
                }
            )
    return iterations


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build project_config.json from the prompt workbook.")
    parser.add_argument("--workbook", type=Path, default=Path("data/input/prompt_image_video.xlsx"))
    parser.add_argument("--input-dir", type=Path, default=Path("data/input"))
    parser.add_argument("--output", type=Path, default=Path("data/input/project_config.json"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_dir = args.input_dir.resolve()
    workbook_path = args.workbook.resolve()

    source_script = (
        "The Last Data: a future architectural data worker thinks scanning and uploading civilization data is meaningless. "
        "During an extinction-level impact alert, conflict with the boss escalates. After the catastrophe, the protagonist "
        "wakes in ruins, discovers the Civilization Archive hard drive, and the stored data becomes the basis for rebuilding "
        "the city as blue holographic architecture."
    )

    config = {
        "project": {
            "title": "The Last Data",
            "authors": ["Yaoli Ma", "Ziyu Guo"],
            "course": "NLP 2026",
            "university": "Technical University of Munich",
            "semester": "Summer 2026",
            "target_platform": "Manual AI video generation: WeDaVinci, PixVerse.ai, Seedance",
            "aspect_ratio": "9:16",
            "final_video_path": "media/final_video.mp4",
        },
        "source_script": source_script,
        "ollama": {
            "base_url": "http://localhost:11434",
            "api_mode": "generate",
            "text_model": "gemma3:1b",
            "vision_model": "",
        },
        "global_constraints": [
            "Part 1 is Code/NLP Workflow: read existing story, draft prompts, reference images, generated clips, and iteration notes; then call local Ollama API for refinement-oriented structuring.",
            "This is a 0.5-to-1 workflow for improving a half-finished AI-video production package, not a 0-to-1 story-to-video generator.",
            "Part 2 is Manual AI Video Production Workflow: manually enter final prompts into WeDaVinci, PixVerse.ai, Seedance, or equivalent tool.",
            "Do not claim that WeDaVinci is called by code.",
            "Preserve shot order, tool attribution, reference images, output paths, and iteration issues from the workbook.",
            "Do not invent missing video files or generated assets.",
        ],
        "iteration_history": build_iterations(workbook_path),
        "shots": build_shots(input_dir, workbook_path),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {args.output} with {len(config['shots'])} shots.")


if __name__ == "__main__":
    main()
