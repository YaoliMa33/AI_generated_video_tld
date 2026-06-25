import fs from "node:fs/promises";
import path from "node:path";
import {
  Presentation,
  PresentationFile,
} from "file:///C:/Users/yaoli/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs";

const root = "C:/Users/yaoli/Documents/NLP/nlp2026_yazimaguo";
const outPptx = path.join(root, "presentation/the-last-data_final_presentation.pptx");
const previewDir = path.join(root, "work/final_presentation_preview");
const W = 1280;
const H = 720;

const C = {
  bg: "#F7F3EA",
  ink: "#1E1E1E",
  muted: "#5F6368",
  line: "#D8D0C2",
  red: "#D83A2E",
  blue: "#2563EB",
  navy: "#111827",
  pale: "#FFFFFF",
  code: "#0B1020",
  green: "#0F8B5F",
  amber: "#B7791F",
};

const img = {
  office1: path.join(root, "data/input/source_package/video_prompt_package/work_records/the_last_data_assets/scene-1-The_Weight_of_Meaningless_Work/shot-1/variant-1.png"),
  office2: path.join(root, "data/input/source_package/video_prompt_package/work_records/the_last_data_assets/scene-1-The_Weight_of_Meaningless_Work/shot-2/variant-1.png"),
  alert: path.join(root, "data/input/source_package/video_prompt_package/work_records/the_last_data_assets/scene-1-The_Weight_of_Meaningless_Work/shot-3/variant-1.png"),
  fist: path.join(root, "data/input/source_package/video_prompt_package/work_records/S2S1_hands.png"),
  hit: path.join(root, "data/input/source_package/video_prompt_package/work_records/S2S2_hit.png"),
  ruins: path.join(root, "data/input/source_package/video_prompt_package/work_records/seedance_s3_reference_images/S3S1_all.png"),
  rebuild: path.join(root, "data/input/source_package/video_prompt_package/work_records/seedance_s4_reference_images/9_munich_last.png"),
};

async function writeBlob(filePath, blob) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.writeFile(filePath, new Uint8Array(await blob.arrayBuffer()));
}

async function readImage(filePath) {
  const bytes = await fs.readFile(filePath);
  return bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength);
}

function shape(slide, cfg) {
  return slide.shapes.add(cfg);
}

function text(slide, value, x, y, w, h, style = {}) {
  const s = shape(slide, {
    geometry: "textbox",
    position: { left: x, top: y, width: w, height: h },
    fill: "none",
    line: { style: "solid", fill: "none", width: 0 },
  });
  s.text = value;
  s.text.style = {
    typeface: style.typeface || "Aptos",
    fontSize: style.fontSize ?? 20,
    bold: style.bold ?? false,
    color: style.color || C.ink,
    alignment: style.alignment,
  };
  return s;
}

function rect(slide, x, y, w, h, fill, line = "none", radius = 0) {
  return shape(slide, {
    geometry: radius ? "roundRect" : "rect",
    position: { left: x, top: y, width: w, height: h },
    fill,
    line: { style: "solid", fill: line, width: line === "none" ? 0 : 1 },
    borderRadius: radius || undefined,
  });
}

function chrome(slide, section = "THE LAST DATA") {
  slide.background.fill = C.bg;
  rect(slide, 44, 34, W - 88, 48, C.pale, C.line, 10);
  rect(slide, 64, 50, 10, 10, C.red, "none", 5);
  rect(slide, 84, 50, 10, 10, C.amber, "none", 5);
  rect(slide, 104, 50, 10, 10, C.green, "none", 5);
  text(slide, section, 142, 46, 420, 20, { fontSize: 12, bold: true, color: C.muted });
  text(slide, "Prompt Generation + Feedback Iteration + Manual Production", 758, 46, 390, 20, {
    fontSize: 12,
    color: C.muted,
    alignment: "right",
  });
}

function title(slide, label, heading, sub = "") {
  text(slide, label.toUpperCase(), 76, 112, 360, 24, { fontSize: 13, bold: true, color: C.red });
  text(slide, heading, 76, 150, 800, 104, { fontSize: 40, bold: true, color: C.ink });
  if (sub) text(slide, sub, 78, 264, 720, 54, { fontSize: 18, color: C.muted });
}

async function addImage(slide, filePath, x, y, w, h, alt) {
  slide.images.add({
    blob: await readImage(filePath),
    contentType: filePath.toLowerCase().endsWith(".jpg") || filePath.toLowerCase().endsWith(".jpeg") ? "image/jpeg" : "image/png",
    alt,
    fit: "cover",
    position: { left: x, top: y, width: w, height: h },
    geometry: "roundRect",
    borderRadius: "rounded-xl",
  });
}

function bullet(slide, items, x, y, w, gap = 42, color = C.ink) {
  items.forEach((item, i) => {
    const yy = y + i * gap;
    rect(slide, x, yy + 7, 8, 8, C.red, "none", 4);
    text(slide, item, x + 22, yy, w - 22, 32, { fontSize: 17, color });
  });
}

function code(slide, value, x, y, w, h) {
  rect(slide, x, y, w, h, C.code, "none", 8);
  text(slide, value, x + 22, y + 18, w - 44, h - 36, {
    typeface: "Consolas",
    fontSize: 14,
    color: "#E5E7EB",
  });
}

function stat(slide, k, v, x, y, w, accent = C.blue) {
  rect(slide, x, y, w, 78, C.pale, C.line, 8);
  text(slide, k, x + 18, y + 14, w - 36, 20, { fontSize: 12, bold: true, color: accent });
  text(slide, v, x + 18, y + 40, w - 36, 24, { fontSize: 20, bold: true, color: C.ink });
}

function flow(slide, steps, x, y, w) {
  const stepW = (w - (steps.length - 1) * 24) / steps.length;
  steps.forEach((s, i) => {
    const xx = x + i * (stepW + 24);
    rect(slide, xx, y, stepW, 96, C.pale, C.line, 8);
    text(slide, String(i + 1).padStart(2, "0"), xx + 16, y + 16, 50, 20, { fontSize: 13, bold: true, color: C.red });
    text(slide, s, xx + 16, y + 44, stepW - 32, 36, { fontSize: 15, bold: true });
    if (i < steps.length - 1) {
      shape(slide, {
        geometry: "line",
        position: { left: xx + stepW + 6, top: y + 48, width: 12, height: 0 },
        line: { style: "solid", fill: C.red, width: 2, beginArrowType: "none", endArrowType: "triangle" },
        fill: "none",
      });
    }
  });
}

async function buildDeck() {
  const p = Presentation.create({ slideSize: { width: W, height: H } });

  let s = p.slides.add();
  chrome(s, "NLP PROJECT WEEK");
  text(s, "The Last Data", 76, 152, 650, 82, { fontSize: 56, bold: true, color: C.red });
  text(s, "Script-to-prompt generation plus asset-grounded refinement", 80, 250, 610, 34, { fontSize: 22, color: C.ink });
  bullet(s, ["Stage 1 generates a first prompt plan from the story script", "Stage 2 refines prompts using existing images, clips, and iteration notes", "Stage 3 detects problem records and writes next-round prompts"], 82, 336, 560, 48);
  await addImage(s, img.office1, 760, 126, 350, 510, "Office scene still");
  text(s, "Yaoli Ma / Ziyu Guo", 82, 622, 320, 24, { fontSize: 16, color: C.muted });

  s = p.slides.add();
  chrome(s);
  title(s, "Premise", "A useless upload becomes the only backup of civilization.", "The story turns prompt generation into a clear narrative: preservation only becomes visible after catastrophe.");
  await addImage(s, img.alert, 810, 118, 340, 430, "Emergency alert still");
  bullet(s, ["Future office: architecture data is scanned and uploaded", "Extinction alert: the boss still demands the upload", "After impact: the archive hard drive becomes the key to reconstruction"], 92, 340, 600, 52);

  s = p.slides.add();
  chrome(s);
  title(s, "Assignment Split", "Three code stages, one final film.", "The code workflow generates prompts, refines them with existing assets, and iterates after human review.");
  flow(s, ["Story script", "Prompt plan", "Asset refinement", "Feedback iteration", "Edited final video"], 86, 340, 1108);
  stat(s, "Code/NLP", "0-to-1 prompt workflow", 92, 238, 300, C.blue);
  stat(s, "Manual production", "WeDaVinci / PixVerse / Seedance", 430, 238, 392, C.red);
  stat(s, "Evidence", "CSV, JSON, Markdown, PPTX", 860, 238, 300, C.green);

  s = p.slides.add();
  chrome(s);
  title(s, "Technical Highlights", "How code supports the video workflow.", "The project uses Python and a local LLM API to make prompt generation, refinement, and iteration reproducible.");
  const highlights = [
    ["1", "Two-stage prompt workflow", "Story script to initial prompts, then asset-grounded refinement using existing images, clips, and review notes."],
    ["2", "Local Ollama API", "A local LLM call generates and refines prompt text without private cloud API keys."],
    ["3", "Prompt table tracker", "Each shot keeps image prompts, motion prompts, visual style, problem notes, and revised prompts."],
    ["4", "Human-in-the-loop iteration", "Problem records are detected automatically and converted into next-round optimized prompts."],
    ["5", "Manual production boundary", "WeDaVinci, PixVerse, and Seedance are used manually; code handles prompts, documentation, and reproducibility."],
  ];
  highlights.forEach(([num, head, body], i) => {
    const yy = 324 + i * 58;
    rect(s, 92, yy, 54, 46, i === 1 ? C.blue : i === 3 ? C.green : C.red, "none", 8);
    text(s, num, 92, yy + 11, 54, 24, { fontSize: 20, bold: true, color: C.pale, alignment: "center" });
    text(s, head, 174, yy - 2, 360, 24, { fontSize: 20, bold: true, color: C.ink });
    text(s, body, 174, yy + 28, 880, 32, { fontSize: 16, color: C.muted });
  });

  s = p.slides.add();
  chrome(s);
  title(s, "Repository", "The GitLab repo is the reproducibility layer.", "All important inputs and generated outputs are stored with explicit paths.");
  code(s, `src/\n  generate_from_script.py\n  build_config_from_workbook.py\n  main.py\n  iterate_prompts.py\n  ollama_client.py\n\ndata/input/\n  story_script.md\n  prompt_image_video.xlsx\n  problem_records/\n  source_package/\n\ndata/output/\n  generated_prompt_table.csv\n  refined_prompt_table.csv\n  iterations/round_01/next_prompt_table.csv`, 86, 300, 520, 300);
  bullet(s, ["Story script drives Stage 1 prompt generation", "Workbook and assets ground Stage 2 refinement", "Problem records drive Stage 3 next-round prompts"], 700, 318, 430, 58);

  s = p.slides.add();
  chrome(s);
  title(s, "Code Pipeline", "Script to prompts, assets to refinement, feedback to next round.", "The code writes prompt artifacts only; image and video generation remains manual.");
  flow(s, ["Read script", "Generate prompt plan", "Validate media", "Refine prompts", "Iterate from feedback"], 96, 258, 1088);
  code(s, `python src/generate_from_script.py --script data/input/story_script.md --output data/output\n\npython src/build_config_from_workbook.py --workbook data/input/prompt_image_video.xlsx --input-dir data/input --output data/input/project_config.json\n\npython src/main.py --config data/input/project_config.json --output data/output\n\npython src/iterate_prompts.py --feedback-dir data/input/problem_records --prompt-table data/output/refined_prompt_table.csv --output-dir data/output/iterations --round-id round_01`, 92, 382, 1070, 240);

  s = p.slides.add();
  chrome(s);
  title(s, "Ollama API", "The LLM call supports both stages.", "No external API key is required for the code workflow.");
  code(s, `POST http://localhost:11434/api/generate\n\n{\n  "model": "gemma3:1b",\n  "prompt": "<project premise + shot list>",\n  "stream": false,\n  "options": { "temperature": 0.2 }\n}`, 86, 284, 560, 250);
  bullet(s, ["Stage 1: script-to-prompt planning", "Stage 2: storyboard, continuity risks, and refinement strategy", "Stage 3: feedback analysis and next-round prompt revision"], 720, 304, 430, 58);

  s = p.slides.add();
  chrome(s);
  title(s, "Prompt Artifacts", "The outputs separate generation, evidence, and refinement.", "The generated files are reviewable and can be regenerated from the script and workbook.");
  stat(s, "Shots", "9", 92, 250, 180, C.red);
  stat(s, "Prompt tables", "Generated + refined + iterated", 302, 250, 260, C.blue);
  stat(s, "Iteration log", "Markdown + JSON", 542, 250, 260, C.green);
  stat(s, "Manifest", "All paths + assets", 832, 250, 260, C.amber);
  code(s, `data/output/generated_prompt_table.csv\n- first prompt plan from story_script.md\n\ndata/output/refined_prompt_table.csv\n- refined manual-upload prompt\n- continuity and asset constraints\n\ndata/input/problem_records/*.md\n- human review issues\n- optimization directions\n\ndata/output/iterations/round_01/next_prompt_table.csv\n- next-round prompts`, 110, 350, 940, 250);

  s = p.slides.add();
  chrome(s);
  title(s, "Manual Production", "Final prompts are uploaded by hand.", "The code produces the prompt package; video tools produce the media.");
  await addImage(s, img.fist, 86, 302, 260, 300, "Fist close-up reference");
  await addImage(s, img.hit, 386, 302, 260, 300, "Confrontation reference");
  bullet(s, ["WeDaVinci: text-to-image-to-video and image-to-video shots", "PixVerse.ai: selected transition / hard-drive shots", "Seedance: longer one-shot ruin and reconstruction clips", "Final video is exported separately as mp4"], 710, 318, 430, 52);

  s = p.slides.add();
  chrome(s);
  title(s, "Storyboard", "Static frames replace embedded videos.", "The submission deck shows representative images while the repo stores the generated video files.");
  await addImage(s, img.office2, 86, 282, 240, 286, "Office routine still");
  await addImage(s, img.ruins, 366, 282, 240, 286, "Ruins wake-up reference");
  await addImage(s, img.rebuild, 646, 282, 240, 286, "Reconstruction reference");
  bullet(s, ["Office pressure", "Catastrophe", "Archive discovery", "City reconstruction"], 930, 304, 260, 48);

  s = p.slides.add();
  chrome(s);
  title(s, "Iterations", "Human feedback becomes the next prompt round.", "The workflow keeps problem records and optimized prompts as reproducible artifacts.");
  bullet(s, ["User writes observed problem and optimization direction in data/input/problem_records", "Code detects feedback documents and shot IDs automatically", "Next-round prompts are written without overwriting images or clips", "Iteration report records what changed and what still needs manual review"], 96, 292, 960, 58);

  s = p.slides.add();
  chrome(s);
  title(s, "Reproducibility", "The repo can be rerun from the command line.", "A reviewer can rebuild Stage 1 and Stage 2 without video-platform credentials.");
  code(s, `pip install -r requirements.txt\nollama pull gemma3:1b\nollama serve\n\npython src/generate_from_script.py --script data/input/story_script.md --output data/output\npython src/build_config_from_workbook.py --workbook data/input/prompt_image_video.xlsx --input-dir data/input --output data/input/project_config.json\npython src/main.py --config data/input/project_config.json --output data/output\npython src/iterate_prompts.py --feedback-dir data/input/problem_records --prompt-table data/output/refined_prompt_table.csv --output-dir data/output/iterations --round-id round_01`, 92, 242, 720, 330);
  bullet(s, ["WeDaVinci, PixVerse, and Seedance remain manual", "Existing images remain the basis for the current video", "No cookies or private platform credentials are committed"], 850, 312, 330, 58);

  s = p.slides.add();
  chrome(s, "CONCLUSION");
  title(s, "What the project demonstrates", "AI video needs generation, refinement, and iteration.", "The code side creates prompts, grounds them in assets, and responds to human feedback; the manual side turns prompts into video.");
  bullet(s, ["NLP contribution: script-to-prompt generation plus feedback-driven prompt iteration", "Engineering contribution: reproducible workflow and explicit media validation", "Creative contribution: a coherent film about the last preserved data of civilization"], 106, 318, 900, 60);
  text(s, "Final output: The Last Data", 106, 582, 520, 32, { fontSize: 28, bold: true, color: C.red });

  return p;
}

async function main() {
  await fs.mkdir(previewDir, { recursive: true });
  await fs.mkdir(path.dirname(outPptx), { recursive: true });
  const deck = await buildDeck();

  for (const [index, slide] of deck.slides.items.entries()) {
    const stem = `slide-${String(index + 1).padStart(2, "0")}`;
    await writeBlob(path.join(previewDir, `${stem}.png`), await deck.export({ slide, format: "png", scale: 1 }));
    await fs.writeFile(path.join(previewDir, `${stem}.layout.json`), await (await slide.export({ format: "layout" })).text());
  }
  await writeBlob(path.join(previewDir, "deck-montage.webp"), await deck.export({ format: "webp", montage: true, scale: 1 }));

  const pptx = await PresentationFile.exportPptx(deck);
  await pptx.save(outPptx);
  console.log(outPptx);
  console.log(`slides=${deck.slides.items.length}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
