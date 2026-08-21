# SNU Connectome Laboratory — Intelligent Academic Web Platform

Official next-generation academic web platform for the **Connectome Laboratory** at **Seoul National University** (PI: **Prof. Jiook Cha** / 차지욱 교수).

🔗 **Website**: [https://www.connectomelab.com/](https://www.connectomelab.com/)  
🏛️ **Affiliations**: Department of Psychology • Interdisciplinary Program in AI (GSAI) • Department of Brain and Cognitive Sciences (BCS)

---

## 🌟 Key Features & Innovations

1. **🧠 Interactive 3D Connectome Viewer (WebGL / Three.js)**
   - Dynamic 3D neural tractography and functional network visualization (DMN, FPN, Salience, Visual, EEG point cloud).
   - Clickable nodes linked to real lab research projects (NeuroMamba, SwiFT, DIVER-0, PRS genetics).

2. **⚡ Living SOTA Research Radar (LLM-Powered Intelligence)**
   - Autonomous crawlers monitoring arXiv, PubMed, and OpenAlex for breakthroughs in:
     - *Large Brain Models (LBMs) & 4D Spatiotemporal Foundation Models*
     - *fMRI & EEG Dynamics (NeuroMamba, DIVER-0, SwiFT)*
     - *Multi-Modal Genetics & Connectomics (Nature Comms, Molecular Psychiatry)*
     - *Quantum Machine Learning (QML) in Neuroscience*
   - Automatic 3-bullet point executive summaries, scientific significance, and Connectome Lab context.

3. **🤖 Ask Connectome AI (Interactive Lab Copilot)**
   - Embedded intelligent chat assistant answering queries about lab research, papers, datasets, recruitment guidelines, and lab culture in real-time.

4. **🔄 Self-Updating Publication & News Engine**
   - Scheduled GitHub Actions cron and local DGX-Spark scripts that automatically fetch newly indexed papers and preprints.

5. **🎨 Vibrant Lab Culture & History Chronicles**
   - Visual timeline of Hongcheon retreats, international fellowships (MILA, Brookhaven National Lab), OB/Scene Focus EEG art exhibitions, and graduation archives.

---

## 🛠️ Tech Stack

- **Framework**: [Astro 5.x](https://astro.build/) (Static Site Generation with zero JS baseline)
- **UI & 3D Components**: React 18, [Three.js](https://threejs.org/), [Tailwind CSS](https://tailwindcss.com/), [Lucide React](https://lucide.dev/)
- **Data Collections**: Type-safe Git-based Markdown & JSON schemas with Zod
- **AI Pipelines**: Python 3.11, OpenAlex API, arXiv API, OpenRouter / Gemini LLM
- **CI/CD & Hosting**: GitHub Pages + GitHub Actions (`deploy.yml`, `research-radar.yml`)

---

## 🚀 Getting Started

### Prerequisites
- Node.js `v18.0+` or `v20.0+`
- Python `3.10+`

### 1. Installation
```bash
git clone https://github.com/snuconnectome/lab-homepage.git
cd lab-homepage
npm install
```

### 2. Development Server
```bash
npm run dev
```
Open `http://localhost:4321` in your browser.

### 3. Build & Preview
```bash
npm run build
npm run preview
```

---

## 🤖 Automated Intelligence Pipelines

### A. Run Scholar & Publications Sync
```bash
python3 scripts/sync_scholar.py
```

### B. Run SOTA Research Radar Sync
```bash
# Optional: Provide OpenRouter API Key for live LLM synthesis
export OPENROUTER_API_KEY="sk-or-v1-..."
python3 scripts/update_research_radar.py
```

### C. Run Local DGX-Spark Cron Runner
```bash
chmod +x scripts/run_dgx_spark_sync.sh
./scripts/run_dgx_spark_sync.sh
```

---

## 🌐 Custom Domain & GitHub Pages Setup

1. In GitHub Repository Settings:
   - Navigate to **Settings** → **Pages**.
   - Under **Build and deployment** → **Source**, select **GitHub Actions**.
   - Under **Custom domain**, enter `www.connectomelab.com` and ensure `Enforce HTTPS` is checked.
2. In DNS Provider (e.g. Domain registrar / DNS manager):
   - Set **CNAME record**: `www` → `snuconnectome.github.io`
   - (Optional) Set **A records** for apex domain `@`:
     - `185.199.108.153`
     - `185.199.109.153`
     - `185.199.110.153`
     - `185.199.111.153`

---

## 📄 License & Contact

- **PI**: Prof. Jiook Cha (차지욱 교수) — `connectome@snu.ac.kr`
- **Lab**: Seoul National University Connectome Laboratory
- © 2026 Connectome Lab. All rights reserved.
