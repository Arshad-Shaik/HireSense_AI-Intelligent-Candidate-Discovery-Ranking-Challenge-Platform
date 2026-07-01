# HireSense_AI Intelligent Candidate Discovery & Ranking Platform

- Redrob AI Hackathon — Intelligent Candidate Discovery
- Team: HireSense_AI

---

## Overview

`HireSense_AI` is a production-grade semantic candidate
ranking system that discovers and ranks the Top 100
AI/ML candidates from a 100,000-candidate dataset
against a Senior AI/ML Engineer job description.

### HireSense_AI System Architecture

```plaintext
candidates.jsonl (100K)
        ↓
candidate_embedding.py
  BAAI/bge-small-en-v1.5
  Document embedding (no prefix)
        ↓
ChromaDB Vector Store
  384-dim embeddings
  100K indexed candidates
        ↓
semantic_ranking_pipeline.py
        ↓
┌───────────────────────────┐
│  BGE Query Embedding      │
│  "Represent this sentence │
│  for searching relevant   │
│  passages: " + JD text    │
└───────────────────────────┘
        ↓
ChromaDB.query(top_k=30,000)
        ↓
candidate_domain_filter.py
  JD vocabulary overlap
  Weighted domain score
  Bigram tokenization
  → Blocks Civil/HR/Sales
  → Passes AI/ML/NLP/DS
        ↓
feature_vector_builder.py
  23 Redrob signals used
  Skill proficiency
  Career recency decay
  GitHub activity
  Assessment scores
        ↓
ranker.py + weighted_score.py
  Similarity:   70%
  Skills:       12%
  Experience:    8%
  Profile:       4%
  Behavior:      3%
  Trust:         3%
        ↓
csv_reasoning_builder.py
  Tier classification
  Signal-rich reasoning
  All 23 redrob signals
        ↓
HireSense_AI.csv
  Top 100 AI/ML candidates
  Validated ✓

```

### Project Structure

```plaintext
hiresense-ai/
├── ai-service/
│   ├── embeddings/
│   │   ├── embedding_model.py           # BAAI/bge-small-en-v1.5
│   │   ├── embedding_builder.py         # BGE query prefix applied
│   │   └── candidate_embedding.py       # Candidate text builder
│   ├── filters/
│   │   └── candidate_domain_filter.py   # Semantic JD filter
│   ├── features/
│   │   ├── feature_vector_builder.py
│   │   ├── skill_features.py
│   │   ├── experience_features.py
│   │   ├── behavior_features.py          # 23 Redrob signals
│   │   ├── trust_features.py
│   │   ├── profile_features.py
│   │   ├── boost_features.py
│   │   └── penalty_features.py
│   ├── ranking/
│   │   ├── ranker.py                    # rank_candidate_with_breakdown
│   │   ├── scorer.py                    # Component scorers
│   │   ├── weighted_score.py            # Weight configuration
│   │   ├── boost_engine.py
│   │   └── penalty_engine.py
│   ├── pipeline/
│   │   └── semantic_ranking_pipeline.py
│   ├── explainability/
│   │   └── csv_reasoning_builder.py
│   ├── ingestion/
│   │   ├── candidate_loader.py
│   │   └── job_description_loader.py
│   ├── output/
│   │   └── csv_writer.py
│   ├── utils/
│   │   ├── candidate_lookup.py
│   │   └── score_normalizer.py
│   ├── chromadb_store/
│   │   └── candidate_collection.py
│   ├── index_data.py                   # Pre-computation step
│   ├── rank.py                         # Ranking step (≤5 min)
│   └── requirements.txt
├── backend/
│   ├── cmd/main.go                     # Go + Gin API server
│   ├── handlers/                       # API handlers
│   ├── services/                       # Business logic
│   ├── models/                         # Data models
│   ├── routes/                         # Route definitions
│   └── middleware/                     # CORS + Logger
├── sandbox/
│   └── app.py                          # Gradio sandbox
├── outputs/
│   └── HireSense_AI.csv                # Final submission
├── submission_metadata.yaml
└── README.md


```

## Requirements

### System Requirements
- Python: 3.10 or higher
- RAM: 8GB minimum (16GB recommended)
- CPU: Any modern CPU (no GPU required)
- Disk: 10GB free space
- OS: Windows / Linux / macOS


### Python Dependencies

```bash
cd ai-service
pip install -r requirements.txt

```

### Go Dependencies (Backend only)

```bash
cd backend
go mod tidy

```

## Dataset Setup

- The dataset files are not included in this repository.  
- Place them in the `data/` folder before running.

**Structure**

```plaintext
hiresense-ai/
└── data/    
    ├── candidates.jsonl        # 100K candidates (465MB)    
    ├── job_description.docx    # JD for ranking    
    ├── candidate_schema.json   # Schema reference    
    └── redrob_signals_doc.docx # Signal reference
```

Download `candidates.jsonl` from the Redrob hackathon bundle and place it in the `data/` folder.


# Reproduction Instructions

⚠️ **Important: Two-Step Process**  
This system uses pre-computed embeddings stored in ChromaDB for fast semantic retrieval.

- `Pre-computation` is `required before ranking.`
- Pre-computation time may exceed 5 minutes, but the ranking step completes within 5 minutes, as permitted by `submission_spec.md` Section 3.


## Step 1: Pre-computation (Run Once)

**Estimated time:**  
- 3-4 hours on 8GB CPU  `depending on system configuration speed`
- 1-2 hours on 16GB CPU `depending on system configuration speed`

```bash
cd ai-service
python index_data.py
```

**This command:**

- Loads all `100,000` candidates from data/candidates.jsonl
- Generates 384-dimensional embeddings using `BAAI/bge-small-en-v1.5`
- Stores all embeddings in ChromaDB vector store at `ai-service/chroma_db/`
- Shows progress: `1000/100000 candidates indexed`

**Expected output:**

```
Step 1
Loaded: 100000

Step 2
Starting indexing of 100000 candidates...
1000/100000 candidates indexed.
2000/100000 candidates indexed.
...
100000/100000 candidates indexed.
Bulk indexing completed.

Step 3
<!-- (Additional instructions or next steps can be added here) -->

```

## Step 2: Ranking (≤ 5 minutes)

```bash
cd ai-service
python rank.py
```

**This command:**

- Loads all `100K candidates into memory`
- Loads job description from `data/job_description.docx`
- Embeds JD query with `BGE query prefix`
- Retrieves top 30,000 candidates from ChromaDB
- Applies semantic domain filter
- Computes multi-signal ranking scores
- Writes Top 100 to `outputs/HireSense_AI.csv`


**Expected output:**

```plaintext

Step 1: Loading candidates...
        Loaded 100000 candidates.
Step 2: Loading job description...
        JD length: 9572 characters.
Step 3: Building candidate lookup...
        Lookup ready: 100000 entries.
Step 4: Running semantic ranking pipeline (top_k=30000)...

----- RETRIEVAL STATS -----
Total retrieved      : 30000
Min Similarity       : 0.455567
Max Similarity       : 0.649921

----- PIPELINE STATS -----
Domain filter PASS   : 6792
Domain filter FAIL   : 23208
Final candidates     : 6792

Step 5: Normalizing scores...
Step 6: Selected Top 100 candidates.
Step 7: Writing submission CSV...

==================================================
HireSense_AI ranking complete.
Top 100 candidates written to HireSense_AI.csv
Score range: 0.697900 → 1.000000
==================================================

```

## Step 3: Validate Submission

```bash

cd ..
python validate_submission.py outputs/HireSense_AI.csv

```

**Expected output:**

```
Submission is valid.
```

# Single Reproduce Command

**As required by submission_spec.md Section 10.3:**

```bash

cd ai-service && python rank.py

```

`Note: Requires ChromaDB pre-built by index_data.py. See Step 1 above for pre-computation instructions.`


# Go Backend API

### Start Backend

```bash

cd backend
go mod tidy
go run cmd/main.go

```

Backend runs on `http://localhost:8080`


### API Endpoints

```bash

GET /health                       → Health check
GET /ping                         → Liveness probe

GET /api/v1/candidates            → All 100 candidates
GET /api/v1/candidates/:id        → By candidate ID
GET /api/v1/candidates/rank/:rank → By rank position
GET /api/v1/candidates/search     → Search candidates

GET /api/v1/ranking/top10         → Top 10 candidates
GET /api/v1/ranking/top50         → Top 50 candidates
GET /api/v1/ranking/top100        → All 100 candidates
GET /api/v1/ranking/stats         → Ranking statistics

```

### Example Requests

```bash

# Health check
curl http://localhost:8080/health

# Top 10 candidates
curl http://localhost:8080/api/v1/ranking/top10

# Ranking statistics
curl http://localhost:8080/api/v1/ranking/stats

# Ranking Top 100
curl http://localhost:8080/api/v1/ranking/top100

# Search AI Engineers
curl "http://localhost:8080/api/v1/candidates/search?q=AI+Engineer"

# Get rank 1 candidate
curl http://localhost:8080/api/v1/candidates/rank/1

```


# Gradio Sandbox

**The sandbox demonstrates the ranking system on small candidate samples as required by submission_spec.md Section 10.5.**

### Run Locally

```bash

cd sandbox
pip install gradio pandas
python app.py

```

Opens at `http://localhost:7860`


### Features

```plaintext

Tab 1: Top Rankings
    → View Top 10 / Top 50 / Top 100
    → Holographic data table

Tab 2: Search Candidates
    → Search by role, ID, or keyword
    → Real-time results

Tab 3: Upload and Analyze
    → Upload sample_candidates.json
    → Domain filter analysis
    → Shows which candidates pass/fail

Tab 4: Architecture
    → Full system architecture diagram
    → Design decisions explained
    → Evaluation metrics strategy

```


### Key Design Decisions

| Decision | Reason |
|----------|--------|
| BAAI/bge-small-en-v1.5 | BGE family, query prefix support, fast CPU inference |
| BGE query prefix | Required for correct retrieval quality |
| ChromaDB | Fast vector retrieval from 100K candidates |
| Similarity weight 70% | Semantic relevance dominates ranking |
| Bigram tokenization | Catches compound terms like machine_learning |
| Career recency decay | Recent roles weighted higher than old ones |
| Skill proficiency multiplier | Expert skills weighted 2× over beginner |
| GitHub activity signal | Real technical evidence beyond keywords |
| 23 Redrob signals used | Full behavioral profile utilized |
| Domain filter | Blocks Civil / HR / Sales, passes AI / ML / NLP |


### Evaluation Metrics Strategy

| Metric | Weight | Strategy |
|--------|:------:|----------|
| NDCG@10 | 50% | Top 10 are strongest AI/ML profiles with highest semantic similarity and GitHub evidence |
| NDCG@50 | 30% | Domain filter ensures only AI/ML candidates in the top 50 |
| MAP | 15% | Semantic similarity drives precision across all levels |
| P@10 | 5% | 100% relevant roles in the top 10 |


### Compute Environment

```bash

Platform : Windows 11 / Local Machine
CPU      : Intel i3
RAM      : 8GB
Python   : 3.14.0
GPU      : None (CPU only)
Network  : Offline during ranking step - without Internet access

```

### AI Tools Declaration

```bash

Claude & ChatGPT  : Architecture discussion, code review, debugging assistance, No candidate data was fed to any LLM. All engineering decisions made by team leader - SHAIK ARSHAD WASIB.

```

# Environment Variables

**Create `ai-service/.env:`**

```bash

HF_TOKEN=your_huggingface_token_here

```

`HuggingFace token is required to download BAAI/bge-small-en-v1.5 model on first run.Subsequent runs use cached model weights.`



# Dependencies

**create `ai-service/requirements.txt`**

```bash
sentence-transformers
chromadb
python-docx
python-dotenv
numpy
```

### sandbox/requirements.txt

```bash
gradio
pandas
```


### backend/go.mod

```bash
module hiresense-backend
go 1.21
require github.com/gin-gonic/gin v1.12.0
```


### Submission Files

```plaintext
outputs/HireSense_AI.csv    → Top 100 ranked candidates
submission_metadata.yaml    → Submission metadata
README.md                   → This file
```


### Contact

```plaintext

Team Name: HireSense_AI
Challenge: Redrob AI Intelligent Candidate Discovery & Ranking Hackathon 2026
Project Name: HireSense_AI Intelligent Candidate Discovery & Ranking Platform

```
