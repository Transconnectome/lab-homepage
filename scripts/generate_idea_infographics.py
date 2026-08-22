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
- Image prompts are "design-mode" briefs, explanation-first: the actual
  hypothesis/experiment/risk content is rendered inside the image in easy
  Korean so a layperson can understand the idea from the image alone
  (codex rendered 130-363 Korean words accurately in measured runs).
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
    """Design-mode brief for the infographics harness (## Prompt header is parsed by it).

    Explanation-first: the image must be understandable on its own by a
    science-curious layperson, so the actual hypothesis/experiment/risk text
    is rendered inside the image in simplified everyday Korean (codex has
    rendered 130-363 Korean words accurately in measured runs).
    """
    title_ko = idea.get("titleKo") or idea.get("title", "")
    hypothesis = idea.get("hypothesisKo") or idea.get("hypothesis", "")
    rationale = idea.get("rationaleKo") or idea.get("rationale", "")
    experiment = idea.get("firstExperimentKo") or idea.get("firstExperiment", "")
    risks = idea.get("risksKo") or idea.get("risks", "")
    threads = " · ".join(idea.get("labThreads", [])[:3])
    inspiration = " · ".join(idea.get("externalInspiration", [])[:2])
    return f"""# S1 Brief — {title_ko}

## Prompt for nanobanana2
과학에 관심 있는 일반 독자를 위한 설명형 인포그래픽 한 장. 사전 지식 없이 이 그림 하나만 보고
연구 아이디어를 이해할 수 있어야 한다. 설명 텍스트가 주인공이고 그림은 이해를 돕는 보조다.

원자료 (아래 내용을 비전공 성인이 읽기 쉬운 한국어로 다듬어 이미지 안에 렌더한다.
전문용어는 영어를 남기되 짧은 한국어 풀이를 괄호로 덧붙인다. 어려운 개념에는 일상 비유를 한 줄 더한다):
- 제목: {title_ko}
- 이 연구가 답하려는 질문(가설): {hypothesis}
- 왜 지금 이 연구실이 하는가: {rationale}
- 어떻게 확인하는가(첫 실험): {experiment}
- 딛고 서 있는 것: 연구실 기반 = {threads} / 외부 영감 = {inspiration}
- 조심할 점: {risks}

레이아웃 요구:
- 맨 위: 쉬운 한국어로 바꾼 큰 제목 + 연구 질문을 일상어로 쓴 부제 한 줄.
- 본문: "무엇을 하려는가 → 어떻게 확인하는가 → 무엇을 딛고 서 있는가 → 조심할 점" 순서의
  읽기 흐름이 명확한 블록 구성. 각 블록은 소제목 + 설명 문장 1-2줄 + 내용을 표현하는 아이콘/도해.
- 텍스트 블록당 한글 최대 2줄, 문장은 짧게. 이미지 전체 단어 수 300 이하.
- 밝은 배경(#FAF9F6 계열), 플랫 디자인, 가로형(16:9), 색 4개 이하, 글자는 멀리서도 읽히는 크기.

## Negative
dark background, 3D, glossy, gradient, circular diagram, photorealistic icons, tiny unreadable text, English-only text, unlabeled decorative diagrams, dense wall of text
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
