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

    Deliberately style-agnostic: earlier versions dictated a fixed palette,
    flat-icon treatment, and numbered-box layout — all borrowed from the
    lab's cha-marp slide brand — and the result read as generic academic
    slides regardless of topic. This version states only the content and
    two hard constraints (readable, 16:9); visual style, palette, and
    composition are left to the model's own creative judgment per idea.
    """
    title_ko = idea.get("titleKo") or idea.get("title", "")
    hypothesis = idea.get("hypothesisKo") or idea.get("hypothesis", "")
    rationale = idea.get("rationaleKo") or idea.get("rationale", "")
    return f"""# S1 Brief — {title_ko}

## Prompt for nanobanana2
이 연구 아이디어를 표현하는 인포그래픽 한 장을 만들어 주세요. 비주얼 스타일, 색감, 구도,
시각적 은유는 전적으로 당신의 창의적 판단에 맡깁니다. 네이비·틸·오렌지 아이콘 조합, 번호
매겨진 박스, 대시보드형 카드처럼 뻔한 학술 발표 슬라이드 톤은 피해 주세요. 잡지 화보처럼
개성 있어도 좋고, 과학 저널리즘 일러스트처럼 은유적이어도 좋습니다 — 이 이야기를 가장 잘
전달한다고 판단하는 방식을 스스로 선택하세요. 매번 다른 아이디어이니 스타일도 아이디어마다
달라져야 자연스럽습니다.

연구 아이디어: {title_ko}
핵심 메시지: {hypothesis}
(배경: {rationale})

분량은 지금까지보다 훨씬 적어야 합니다. 하나의 장면, 하나의 중심 은유만 그려 주세요.
비교 패널, 보조 다이어그램, 사이드바처럼 화면을 여러 구역으로 나누는 구성은 만들지 마세요.
이미지 안 텍스트 총량은 80단어를 넘지 않게: 제목 한 줄 + 핵심 메시지를 쉬운 한국어로 옮긴
문장 한두 개 + 장면 속 라벨 몇 개면 충분합니다 (전문용어는 영어 옆에 짧은 한글 풀이 가능).
글자보다 여백이 넉넉해야 하고, 가로형(16:9)이며 글자는 실제로 읽힐 만큼 커야 합니다.

그 외 색상 수, 구도, 아이콘/일러스트 스타일은 전부 당신의 선택에 맡깁니다.

## Negative
navy-teal-orange corporate palette, numbered box grid, dashboard-card layout, multi-panel composition, side-by-side comparison panels, generic academic slide look, cluttered scene, dark background, glossy or glowing sci-fi look, photorealistic human faces or photo-style portraits, movie-poster style, tiny illegible text, warped or stylized title lettering, text overflowing its box, garbled or malformed characters
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
