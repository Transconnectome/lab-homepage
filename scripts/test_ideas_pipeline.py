#!/usr/bin/env python3
"""
Offline tests for the idea generator (scripts/generate_research_ideas.py).

Covers the three balance mechanisms, none of which need an LLM or a network:
round-robin trend sampling, source-based redundancy detection, and the
one-idea-per-category-per-run quota.

Run:  python3 scripts/test_ideas_pipeline.py
"""

import importlib.util
import json
import os
import shutil
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

spec = importlib.util.spec_from_file_location(
    "gen", os.path.join(ROOT, "scripts", "generate_research_ideas.py"))
gen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gen)

FAILURES = []


def check(cond, msg):
    if not cond:
        FAILURES.append(msg)


def test_round_robin_caps_a_prolific_topic():
    """A bucket with far more entries must not crowd the others out."""
    trends = ([{"topic": "EEG", "title": f"eeg {i}", "publishedDate": f"2026-08-{i:02d}"}
               for i in range(1, 21)]
              + [{"topic": "fMRI", "title": "fmri 1", "publishedDate": "2026-07-01"},
                 {"topic": "fMRI", "title": "fmri 2", "publishedDate": "2026-06-01"},
                 {"topic": "Gene", "title": "gene 1", "publishedDate": "2026-05-01"}])

    picked = gen.sample_trends_round_robin(trends, 9)
    by_topic = {}
    for d in picked:
        by_topic[d["topic"]] = by_topic.get(d["topic"], 0) + 1

    check(len(picked) == 9, f"should return exactly the limit, got {len(picked)}")
    check(by_topic.get("fMRI") == 2 and by_topic.get("Gene") == 1,
          f"scarce topics must contribute everything they have, got {by_topic}")
    check(by_topic.get("EEG") == 6,
          f"the prolific topic takes only the remainder, got {by_topic}")
    check(picked[0]["title"] == "eeg 20",
          "within a topic the newest entry must come first")

    # Fewer entries than the limit: everything is kept, nothing invented.
    check(len(gen.sample_trends_round_robin(trends[:3], 14)) == 3,
          "a short catalogue must pass through untouched")
    check(gen.sample_trends_round_robin([], 14) == [],
          "an empty catalogue must not raise")


def test_redundancy_matches_the_real_history():
    """Back-tested against the first twelve published ideas."""
    zipbrain_a = {"title": "Energy-Efficient and Locally Deployable EEG Foundation Models",
                  "category": "foundation-models",
                  "externalInspiration": ["ZIPBrain: Can EEG Foundation Models Be Faster..."]}
    zipbrain_b = {"title": "Edge-Safe EEG Foundation Model",
                  "category": "foundation-models",
                  "externalInspiration": ["ZIPBrain"]}
    check(gen.redundancy_reason(zipbrain_b, [zipbrain_a]) is not None,
          "the same paper mined twice for one category must be caught")

    # EEG-PRIME legitimately produced a genetics idea and a qml idea.
    prime_gen = {"title": "PRS-Conditioned Brain-State Prototypes", "category": "genetics",
                 "externalInspiration": ["EEG-PRIME: Prototype-Aligned Representation Learning"]}
    prime_qml = {"title": "Quantum-Enhanced Prototypes for EEG Decoding Generalization",
                 "category": "qml", "externalInspiration": ["EEG-PRIME"]}
    check(gen.redundancy_reason(prime_qml, [prime_gen]) is None,
          "one paper may inspire different categories — that is not redundancy")

    # A full title with a source suffix must key to the same paper as a bare one.
    long_form = {"title": "Something New", "category": "art-science",
                 "externalInspiration": [
                     "Continuous-Latent Predictive Modeling with Semantic Alignment "
                     "for EEG-Language Foundation Models (arXiv (2026-08))"]}
    short_form = {"title": "Something Else", "category": "art-science",
                  "externalInspiration": ["Continuous-Latent Predictive Modeling"]}
    check(gen.redundancy_reason(short_form, [long_form]) is not None,
          "citation shape must not defeat the source key")

    exact = {"title": "Edge-Safe EEG Foundation Model", "category": "qml",
             "externalInspiration": ["Unrelated Paper"]}
    check(gen.redundancy_reason(exact, [zipbrain_b]) is not None,
          "an identical title is redundant regardless of category")

    fresh = {"title": "Agentic Literature Triage for Neuroimaging", "category": "agentic-ai",
             "externalInspiration": ["Some Agent Paper"]}
    check(gen.redundancy_reason(fresh, [zipbrain_a, prime_gen]) is None,
          "a genuinely new idea must pass")


def test_one_idea_per_category_per_run():
    tmp = tempfile.mkdtemp()
    try:
        gen.IDEAS_DIR = tmp
        payload = {"ideas": [
            make_idea("First Foundation Idea", "foundation-models", "Paper A"),
            make_idea("Second Foundation Idea", "foundation-models", "Paper B"),
            make_idea("A Genetics Idea", "genetics", "Paper C"),
        ]}
        gen.call_openrouter = lambda prompt, key: payload
        os.environ["OPENROUTER_API_KEY"] = "test-key"
        os.environ["IDEAS_BACKEND"] = "openrouter"
        gen.main()

        written = [json.load(open(os.path.join(tmp, f), encoding="utf-8"))
                   for f in os.listdir(tmp) if f.endswith(".json")]
        cats = sorted(d["category"] for d in written)
        check(cats == ["foundation-models", "genetics"],
              f"the second foundation-models idea must be dropped, got {cats}")
        check(len(written) == 2, f"expected 2 ideas written, got {len(written)}")
    finally:
        shutil.rmtree(tmp)
        os.environ.pop("OPENROUTER_API_KEY", None)


def test_recent_category_mix_summarises_the_window():
    existing = [{"category": "foundation-models", "date": "2026-08-24"},
                {"category": "foundation-models", "date": "2026-08-23"},
                {"category": "qml", "date": "2026-08-22"},
                {"category": "genetics", "date": "2020-01-01"}]
    line = gen.recent_category_mix(existing, window=3)
    check("foundation-models x2" in line, f"dominant category must be surfaced: {line}")
    check("genetics" not in line, f"entries outside the window must be excluded: {line}")
    check("none yet" in gen.recent_category_mix([]), "an empty history must not raise")


def make_idea(title, category, source):
    body = {k: "충분히 긴 한국어 본문입니다." if k.endswith("Ko") else "A long enough English body."
            for k in gen.BODY_FIELDS}
    return {"title": title, "titleKo": title + " (KO)", "category": category,
            "labThreads": ["NeuroMamba"], "externalInspiration": [source], **body}


if __name__ == "__main__":
    for fn in (test_round_robin_caps_a_prolific_topic,
               test_redundancy_matches_the_real_history,
               test_one_idea_per_category_per_run,
               test_recent_category_mix_summarises_the_window):
        fn()
    if FAILURES:
        print("\nFAILED:\n  " + "\n  ".join(FAILURES))
        sys.exit(1)
    print("\nAll idea pipeline tests passed.")
