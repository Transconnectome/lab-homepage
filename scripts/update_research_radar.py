#!/usr/bin/env python3
"""
Connectome Lab - Automated SOTA & Living Research Radar
Crawls arXiv and PubMed for cutting-edge breakthroughs in:
- Brain Foundation Models & LBMs
- fMRI / EEG Dynamics & Equivariance
- Polygenic Risk Scores & Multi-modal Connectomics
- Quantum Machine Learning (QML)

Generates 3-bullet points executive summaries, scientific significance,
and Connectome Lab relevance using OpenRouter / Gemini API or local heuristic parser.
"""

import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import json
import os
import re
import sys

TRENDS_DIR = os.path.join(os.path.dirname(__file__), "..", "src", "content", "trends")
ARXIV_QUERY = 'all:"Large Brain Model" OR all:"fMRI foundation model" OR all:"EEG foundation model" OR all:"state space fMRI" OR all:"polygenic connectome"'
ARXIV_API = f"http://export.arxiv.org/api/query?search_query={urllib.parse.quote(ARXIV_QUERY)}&max_results=8&sortBy=submittedDate&sortOrder=descending"

def clean_filename(title):
    cleaned = re.sub(r'[^a-zA-Z0-9\s-]', '', title).strip().lower()
    return re.sub(r'[\s-]+', '-', cleaned)[:40]

def summarize_with_llm(title, abstract, openrouter_key=None):
    """Optional LLM summarizer using OpenRouter / Gemini."""
    if not openrouter_key:
        # Fallback: High-quality rule-based structured extraction
        sentences = [s.strip() for s in abstract.split('. ') if len(s.strip()) > 20]
        points = sentences[:3] if len(sentences) >= 3 else sentences
        return {
            "summaryPoints": [p.rstrip('.') + '.' for p in points],
            "significance": "Presents important advancements in scaling neural representation learning for physiological brain dynamics.",
            "labRelevance": "Directly interfaces with Connectome Lab's active research in foundation models and multimodal brain decoding."
        }
    
    # If OpenRouter key is configured
    try:
        url = "https://openrouter.ai/api/v1/chat/completions"
        prompt = f"""You are an expert computational neuroscientist at SNU Connectome Lab.
Summarize this paper:
Title: {title}
Abstract: {abstract}

Provide a JSON with:
- "summaryPoints": array of 3 concise bullet points
- "significance": 1 sentence explaining the scientific significance
- "labRelevance": 1 sentence relating it to Connectome Lab (Large Brain Models, Neuro-X, NeuroMamba, DIVER-0, PRS genetics, or QML).
"""
        req_data = {
            "model": "google/gemini-2.5-flash",
            "messages": [{"role": "user", "content": prompt}],
            "response_format": {"type": "json_object"}
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(req_data).encode('utf-8'),
            headers={
                "Authorization": f"Bearer {openrouter_key}",
                "Content-Type": "application/json"
            }
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            content = data['choices'][0]['message']['content']
            return json.loads(content)
    except Exception as e:
        print(f"[!] LLM API fallback due to: {e}")
        sentences = [s.strip() for s in abstract.split('. ') if len(s.strip()) > 20]
        return {
            "summaryPoints": [p.rstrip('.') + '.' for p in sentences[:3]],
            "significance": "Advances representation learning on large-scale neuroimaging datasets.",
            "labRelevance": "Relevant to ongoing Neuro-X Large Brain Model initiatives."
        }

def fetch_arxiv_papers():
    print("[*] Fetching latest papers from arXiv API...")
    try:
        req = urllib.request.Request(ARXIV_API, headers={"User-Agent": "ConnectomeLab-Radar/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            xml_data = resp.read().decode('utf-8')
            root = ET.fromstring(xml_data)
            
            entries = []
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            for entry in root.findall('atom:entry', ns):
                title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
                summary = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')
                published = entry.find('atom:published', ns).text[:10]
                link = entry.find('atom:id', ns).text.strip()
                authors = [a.find('atom:name', ns).text for a in entry.findall('atom:author', ns)]
                
                entries.append({
                    "title": title,
                    "abstract": summary,
                    "publishedDate": published,
                    "url": link,
                    "authors": authors
                })
            print(f"[+] Found {len(entries)} candidate papers on arXiv.")
            return entries
    except Exception as e:
        print(f"[!] Error querying arXiv: {e}")
        return []

def main():
    os.makedirs(TRENDS_DIR, exist_ok=True)
    openrouter_key = os.environ.get("OPENROUTER_API_KEY")
    papers = fetch_arxiv_papers()
    
    count = 0
    for p in papers:
        slug = clean_filename(p["title"])
        out_path = os.path.join(TRENDS_DIR, f"{slug}.json")
        
        if os.path.exists(out_path):
            continue
            
        print(f"[*] Processing: {p['title'][:60]}...")
        analysis = summarize_with_llm(p["title"], p["abstract"], openrouter_key)
        
        topic = "Brain Foundation Models"
        lower = p["title"].lower()
        if "eeg" in lower:
            topic = "fMRI/EEG Dynamics"
        elif "polygenic" in lower or "gene" in lower:
            topic = "Genomics & Connectomics"
        elif "quantum" in lower:
            topic = "Quantum ML"
        elif "language" in lower or "alignment" in lower:
            topic = "Brain-LLM Alignment"

        record = {
            "title": p["title"],
            "authors": p["authors"][:4],
            "publishedDate": p["publishedDate"],
            "source": f"arXiv ({p['publishedDate'][:7]})",
            "topic": topic,
            "url": p["url"],
            "summaryPoints": analysis.get("summaryPoints", []),
            "significance": analysis.get("significance", ""),
            "labRelevance": analysis.get("labRelevance", ""),
            "modality": ["fMRI" if "fmri" in lower else "EEG" if "eeg" in lower else "Genomics" if "gene" in lower else "Multi-Modal"],
            "badge": "Emerging Paper"
        }
        
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(record, f, indent=2, ensure_ascii=False)
            count += 1

    print(f"[✓] Research Radar updated. Added {count} new trend items.")

if __name__ == "__main__":
    main()
