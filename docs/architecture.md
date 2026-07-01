# `docs/architecture.md`

```markdown
# HireSense_AI — System Architecture

## Overview

HireSense_AI is a production-grade semantic
candidate ranking system for the Redrob AI
Intelligent Candidate Discovery & Ranking Challenge.

## Architecture Diagram

┌─────────────────────────────────────────────┐
│ DATA LAYER │
│ candidates.jsonl (100K candidates, 465MB) │
│ job_description.docx (9572 characters) │
└─────────────────┬───────────────────────────┘
│
┌─────────────────▼───────────────────────────┐
│ PRE-COMPUTATION LAYER │
│ index_data.py │
│ → BAAI/bge-small-en-v1.5 │
│ → 384-dim document embeddings │
│ → ChromaDB vector store │
│ Time: 3-4 hours on CPU │
└─────────────────┬───────────────────────────┘
│
┌─────────────────▼───────────────────────────┐
│ RANKING LAYER (rank.py) │
│ ≤ 5 minutes on CPU │
│ │
│ 1. BGE Query Embedding │
│ "Represent this sentence for │
│ searching relevant passages: " + JD │
│ │
│ 2. ChromaDB Semantic Retrieval │
│ top_k = 30,000 candidates │
│ │
│ 3. Domain Filter │
│ JD vocabulary overlap ≥ 4% │
│ Weighted domain score ≥ 5 │
│ Bigram tokenization │
│ │
│ 4. Feature Vector Builder │
│ All 23 Redrob behavioral signals │
│ Skill proficiency multipliers │
│ Career recency decay │
│ │
│ 5. Multi-Signal Ranker │
│ Similarity: 70% │
│ Skills: 12% │
│ Experience: 8% │
│ Profile: 4% │
│ Behavior: 3% │
│ Trust: 3% │
│ │
│ 6. CSV Reasoning Builder │
│ Tier classification │
│ Signal-rich reasoning strings │
└─────────────────┬───────────────────────────┘
│
┌─────────────────▼───────────────────────────┐
│ OUTPUT LAYER │
│ HireSense_AI.csv │
│ Top 100 AI/ML candidates │
│ Validated ✓ │
└─────────────────┬───────────────────────────┘
│
┌─────────┴──────────┐
│ │
┌───────▼────────┐ ┌────────▼────────┐
│ Go Backend │ │ Gradio Sandbox │
│ Gin API │ │ HuggingFace │
│ Port 8080 │ │ Port 7860 │
└────────────────┘ └─────────────────┘


## Component Details

### Embedding Model
- Model: BAAI/bge-small-en-v1.5
- Dimensions: 384
- Query prefix required for retrieval
- CPU inference, no GPU needed

### Vector Store
- Database: ChromaDB
- Collection: 100K candidate embeddings
- Query: cosine similarity top-K retrieval

### Domain Filter
- Method: JD vocabulary overlap scoring
- Tokenization: Unigrams + bigrams
- Threshold: overlap ≥ 4%, domain score ≥ 5
- Result: Blocks non-IT, passes AI/ML

### Ranker
- Semantic similarity: 70% weight
- Multi-signal feature vector
- Boost/penalty engine
- Score normalization to [0,1]

### API Layer
- Language: Go 1.21, vs code Go Lang extension also need
- Framework: Gin
- Endpoints: 10 REST endpoints
- Format: JSON responses


