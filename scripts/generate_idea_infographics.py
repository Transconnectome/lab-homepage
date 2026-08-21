#!/usr/bin/env python3
"""
Connectome Lab - Idea Infographic Generator (DGX-only)

For every idea in src/content/ideas/*.json that has no `image` yet, renders a
single Korean infographic via the codex CLI imagegen path (gpt-image-2,
ChatGPT login auth, no API key) and saves it to public/assets/ideas/<slug>.png,
then records `image` and `imageGeneratedBy` back into the idea JSON.

Requirements (all DGX-local; the script skips gracefully anywhere else):
- `codex` CLI on PATH, logged in
- the infographics skill harness at
  ~/.claude/skills/infographics/generate_image.py (it harvests codex's output
  from ~/.codex/generated_images/ — do not reimplement that here)

Design notes:
- Runs SEQUENTIALLY: codex imagegen is slower in parallel (measured by the
  infographics skill), 46-295s per image.
- Image prompts are "design-mode" briefs: concept-flow visualization with
  MINIMAL embedded text (title + a few short Korean noun-phrase labels), since
  Korean rendering inside generated images is the main failure mode.
- This script is NOT in the GitHub Actions workflow on purpose: images are
  generated on DGX and reviewed by a human before they are pushed. The /ideas
  page renders text-only cards for ideas without images, so a missing image is
  never a broken state.

Usage:
    python3 scripts/generate_idea_infographics.py [--limit N] [--slug SLUG] [--force]
"""

import argparse
import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
IDEAS_DIR = os.path.join(ROOT, "src", "content", "ideas")
ASSETS_DIR = os.path.join(ROOT, "public", "assets", "ideas")
HARNESS = os.path.expanduser("~/.claude/skills/infographics/generate_image.py")
IMAGE_GENERATED_BY = "imagegen:openai/gpt-image-2 (codex)"
PER_IMAGE_TIMEOUT = 900  # codex imagegen measured at 46-295s per image


def build_brief(idea):
    """Design-mode brief for the infographics harness (## Prompt header is parsed by it)."""
    title_ko = idea.get("titleKo") or idea.get("title", "")
    hypothesis = idea.get("hypothesisKo") or idea.get("hypothesis", "")
    experiment = idea.get("firstExperimentKo") or idea.get("firstExperiment", "")
    threads = " · ".join(idea.get("labThreads", [])[:3])
    inspiration = " · ".join(idea.get("externalInspiration", [])[:2])
    return f"""# S1 Brief — {title_ko}

## Prompt for nanobanana2
연구 아이디어 한 장 인포그래픽. 주제: "{title_ko}".
핵심 메시지(가설): {hypothesis}
개념 흐름(왼쪽→오른쪽): 외부 영감({inspiration}) + 연구실 기반({threads}) → 새 가설 → 첫 실험({experiment}) 순서의 개념 결합 다이어그램.
청중: 일반 방문객과 대학원생. 언어: 한국어, 전문용어는 영어 유지.
시각 제약: 밝은 배경(#FAF9F6 계열), 플랫 디자인, 가로형(16:9), 색 4개 이하.
이미지 안 텍스트는 최소화: 제목 1줄 + 짧은 한국어 명사구 라벨 4개 이하만. 긴 문장은 넣지 않는다.
레이아웃과 아이콘 선택은 재량에 맡긴다. 개념을 시각적으로 설명하는 것이 문자보다 우선이다.

## Negative
dark background, 3D, glossy, gradient, circular diagram, photorealistic icons, tiny captions, long sentences, dense paragraph text, poster style
"""


def generate_one(path, force=False):
    slug = os.path.splitext(os.path.basename(path))[0]
    with open(path, encoding="utf-8") as f:
        idea = json.load(f)
    if idea.get("image") and not force:
        return "skip"

    with tempfile.TemporaryDirectory(prefix=f"idea-info-{slug[:20]}-") as tmp:
        prompt_path = os.path.join(tmp, "S1_prompt.md")
        out_dir = os.path.join(tmp, "out")
        os.makedirs(out_dir)
        with open(prompt_path, "w", encoding="utf-8") as f:
            f.write(build_brief(idea))

        print(f"[*] {slug}: generating (codex imagegen, this can take minutes)...")
        proc = subprocess.run(
            [sys.executable, HARNESS, "--prompt", prompt_path, "--output", out_dir, "--variants", "1"],
            capture_output=True, text=True, timeout=PER_IMAGE_TIMEOUT,
        )
        images = sorted(glob.glob(os.path.join(out_dir, "**", "*.png"), recursive=True),
                        key=os.path.getmtime)
        if not images:
            tail = (proc.stdout + proc.stderr)[-400:]
            print(f"[!] {slug}: no image produced (rc={proc.returncode}): {tail}")
            return "fail"

        os.makedirs(ASSETS_DIR, exist_ok=True)
        dest = os.path.join(ASSETS_DIR, f"{slug}.png")
        shutil.copyfile(images[-1], dest)

    idea["image"] = f"/assets/ideas/{slug}.png"
    idea["imageGeneratedBy"] = IMAGE_GENERATED_BY
    with open(path, "w", encoding="utf-8") as f:
        json.dump(idea, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"[+] {slug}: saved public/assets/ideas/{slug}.png")
    return "ok"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="generate at most N images this run")
    ap.add_argument("--slug", help="only this idea (filename without .json)")
    ap.add_argument("--force", action="store_true", help="regenerate even if an image exists")
    args = ap.parse_args()

    if not shutil.which("codex"):
        print("[!] codex CLI not found — skipping infographic generation (DGX-only step).")
        return 0
    if not os.path.exists(HARNESS):
        print(f"[!] infographics harness not found at {HARNESS} — skipping.")
        return 0

    paths = sorted(glob.glob(os.path.join(IDEAS_DIR, "*.json")))
    if args.slug:
        paths = [p for p in paths if os.path.splitext(os.path.basename(p))[0] == args.slug]
        if not paths:
            print(f"[!] no idea named {args.slug}")
            return 1

    done = failed = attempted = 0
    for path in paths:
        if args.limit and attempted >= args.limit:
            break
        try:
            status = generate_one(path, force=args.force)
        except subprocess.TimeoutExpired:
            print(f"[!] {os.path.basename(path)}: timed out after {PER_IMAGE_TIMEOUT}s")
            failed += 1
            attempted += 1
            continue
        if status == "ok":
            done += 1
            attempted += 1
        elif status == "fail":
            failed += 1
            attempted += 1

    print(f"[✓] infographics: generated {done}, failed {failed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
