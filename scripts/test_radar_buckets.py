#!/usr/bin/env python3
"""
Offline tests for the Research Radar bucket logic (scripts/update_research_radar.py).

The radar's collection path now has real branching — per-bucket quotas, a
deterministic neuro-term gate, an LLM relevance gate, and cross-bucket dedup —
and arXiv is not always reachable from a dev box. These tests drive the whole
path through ARXIV_CACHE with synthetic feeds, so no network is involved.

Run:  python3 scripts/test_radar_buckets.py
"""

import importlib.util
import json
import os
import shutil
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

spec = importlib.util.spec_from_file_location(
    "radar", os.path.join(ROOT, "scripts", "update_research_radar.py"))
radar = importlib.util.module_from_spec(spec)
spec.loader.exec_module(radar)

FAILURES = []


def check(cond, msg):
    if not cond:
        FAILURES.append(msg)


def entry(uid, title, abstract="An abstract about methods.", date="2026-08-20"):
    return {"id": uid, "title": title, "abstract": abstract, "publishedDate": date,
            "url": f"http://arxiv.org/abs/{uid}", "authors": ["A. Author", "B. Author"]}


def run_with_cache(cache):
    """Run the radar against a synthetic feed; return {topic: [titles]}."""
    tmp = tempfile.mkdtemp()
    try:
        radar.TRENDS_DIR = tmp
        cache_path = os.path.join(tmp, "cache.json")
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(cache, f)
        os.environ["ARXIV_CACHE"] = cache_path
        os.environ.pop("OPENROUTER_API_KEY", None)
        radar.main()

        out = {}
        for name in sorted(os.listdir(tmp)):
            if not name.endswith(".json") or name == "cache.json":
                continue
            d = json.load(open(os.path.join(tmp, name), encoding="utf-8"))
            out.setdefault(d["topic"], []).append(d)
        return out
    finally:
        shutil.rmtree(tmp)


def test_gates_quotas_and_dedup():
    got = run_with_cache({
        "Brain Foundation Models (fMRI)": [
            entry("1", "A Scalable fMRI Foundation Model for 4D Dynamics"),
            entry("2", "State Space fMRI Encoding at Scale"),
            entry("3", "Yet Another fMRI Foundation Model"),
            entry("4", "A Fourth fMRI Paper Beyond Quota"),
        ],
        "Gene & Brain": [
            entry("6", "Polygenic Risk Scores Predict Cortical Thickness",
                  "We link PRS to brain structure."),
            entry("7", "Polygenic Risk Score for Crop Yield",
                  "Agricultural genomics for crop traits."),
        ],
        "Agentic AI": [
            entry("9", "An LLM Agent for Web Shopping",
                  "A shopping agent benchmark over web pages."),
            entry("10", "Agentic Pipelines for Neuroimaging Analysis",
                  "An LLM agent that runs fMRI preprocessing."),
            entry("1", "A Scalable fMRI Foundation Model for 4D Dynamics"),  # dup id
        ],
    })
    titles = [d["title"] for ds in got.values() for d in ds]

    check(len(got.get("Brain Foundation Models (fMRI)", [])) == 3,
          "per-bucket quota should cap the fMRI bucket at 3")
    check(not any("Crop Yield" in t for t in titles),
          "neuro gate should drop the agricultural PRS paper")
    check(not any("Web Shopping" in t for t in titles),
          "neuro gate should drop the shopping-agent paper")
    check(any("Neuroimaging Analysis" in d["title"] for d in got.get("Agentic AI", [])),
          "an agent paper applied to neuroimaging must survive (scope A)")
    check(sum("4D Dynamics" in t for t in titles) == 1,
          "a paper matching two buckets must be written once, to the first bucket")

    fmri = got.get("Brain Foundation Models (fMRI)", [])
    check(all(d["modality"] == ["fMRI"] for d in fmri),
          f"modality should follow the title/bucket, got {[d['modality'] for d in fmri]}")


def test_relevance_gate():
    scores = {"Quantum Kernels for Brain Network Classification": 0.8,
              "Quantum Advantage in Brain-Inspired Optimization": 0.2}
    original = radar.summarize_with_llm
    radar.summarize_with_llm = lambda title, abstract, topic, key=None: {
        "summaryPoints": ["p1", "p2", "p3"], "significance": "s", "labRelevance": "r",
        "labRelevanceScore": scores[title], "generatedBy": "llm:stub"}
    try:
        got = run_with_cache({"Quantum ML": [
            entry("20", "Quantum Kernels for Brain Network Classification",
                  "We classify connectomes."),
            entry("21", "Quantum Advantage in Brain-Inspired Optimization",
                  "A brain-inspired metaphor only."),
        ]})
    finally:
        radar.summarize_with_llm = original

    kept = [d["title"] for ds in got.values() for d in ds]
    check(kept == ["Quantum Kernels for Brain Network Classification"],
          f"relevance gate should keep only the 0.8 paper, kept={kept}")
    check(got["Quantum ML"][0]["labRelevanceScore"] == 0.8,
          "the passing score must be recorded on the entry")


def test_buckets_mirror_config_enum():
    cfg = open(os.path.join(ROOT, "src", "content", "config.ts"), encoding="utf-8").read()
    block = cfg.split("topic: z.enum([")[1].split("]),")[0]
    enum_vals = {v.strip().strip("',") for v in block.strip().splitlines()}
    check(enum_vals == set(radar.BUCKETS),
          f"BUCKETS keys and the config.ts topic enum diverge: {enum_vals ^ set(radar.BUCKETS)}")


def test_extractive_fallback_passes_the_gate():
    """No API key means no score, and a scoreless entry must not be silently dropped."""
    out = radar.extractive_fallback("First sentence here. Second sentence here. Third one here.")
    check(out["labRelevanceScore"] is None, "fallback must not invent a relevance score")
    check(out["generatedBy"] == "extractive-fallback", "fallback must label itself")


if __name__ == "__main__":
    for fn in (test_gates_quotas_and_dedup, test_relevance_gate,
               test_buckets_mirror_config_enum, test_extractive_fallback_passes_the_gate):
        fn()
    if FAILURES:
        print("\nFAILED:\n  " + "\n  ".join(FAILURES))
        sys.exit(1)
    print("\nAll radar bucket tests passed.")
