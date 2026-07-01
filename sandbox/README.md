# `sandbox/README.md`


# HireSense_AI — Gradio Sandbox

Redrob AI Hackathon — Section 10.5 Sandbox Requirement

### What This Is
```
This Gradio sandbox demonstrates the HireSense_AI
ranking system on small candidate samples.

It satisfies submission_spec.md Section 10.5:
"A working hosted environment where your ranking
system can be run on a small candidate sample."
```

# `Live Demo`

**HuggingFace Spaces:**
https://huggingface.co/spaces/YOUR_USERNAME/hiresense-ai

### Features

- Tab 1: View Top 10 / Top 50 / All 100 ranked candidates
- Tab 2: Search by role, ID, or keyword
- Tab 3: Upload JSON sample → domain filter analysis
- Tab 4: Full system architecture diagram
- Voice: Web Speech Synthesis announcements
- Theme: Professional Dynamic Holographic UI

### Run Locally

```bash
cd sandbox
pip install -r requirements.txt
python app.py
```

Open: `http://127.0.0.1:7860`


### Requirements

```python
gradio==6.19.0
pandas==3.0.3
```

### How It Works

```
1. Loads HireSense_AI.csv (pre-ranked Top 100)
2. Displays rankings with holographic UI
3. Accepts JSON upload of up to 50 candidates
4. Applies simplified domain filter check
5. Shows which candidates would pass/fail
```

### Upload Format

**Accepts:**

- sample_candidates.json (JSON array)
- candidates.jsonl (newline-delimited JSON)
- Maximum: 50 candidates per upload

