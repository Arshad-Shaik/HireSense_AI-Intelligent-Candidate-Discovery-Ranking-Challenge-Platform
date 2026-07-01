# HireSense_AI — API Design

### Overview

```plaintext
REST API built with Go + Gin Framework.
Serves Top 100 ranked AI/ML candidates
from HireSense_AI.csv.
```

Base URL: http://localhost:8080

## API Endpoints

### Health

| Method | Path    | Description     |
|--------|---------|-----------------|
| GET    | /health | Full health check |
| GET    | /ping   | Liveness probe  |

#### GET /health

Response:
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "service": "HireSense_AI Backend",
    "version": "1.0.0",
    "timestamp": "2026-06-28T08:16:54Z",
    "csv_loaded": true
  }
}

```

### Candidates

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/candidates` | All candidates (paginated) |
| GET | `/api/v1/candidates/:id` | Get candidate by candidate ID |
| GET | `/api/v1/candidates/rank/:rank` | Get candidate by rank position |
| GET | `/api/v1/candidates/search` | Search candidates |



### `GET /api/v1/candidates`

**Query params:**

- page (int, default: 1)
- page_size (int, default: 10, max: 100)


**Response:**

```bash
{
  "success": true,
  "data": {
    "total": 100,
    "page": 1,
    "page_size": 10,
    "total_pages": 10,
    "data": [...]
  }
}
```

### `GET /api/v1/candidates/search`

**Query params:**

- q (string) — search query
- min_score (float, default: 0)
- max_rank (int, default: 0 = all)
- page (int, default: 1)
- page_size (int, default: 10)


### Ranking Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/ranking/top10` | Get Top 10 candidates |
| GET | `/api/v1/ranking/top50` | Get Top 50 candidates |
| GET | `/api/v1/ranking/top100` | Get all Top 100 candidates |
| GET | `/api/v1/ranking/stats` | Get ranking statistics |


### `GET /api/v1/ranking/stats`

**Response:**

```bash
{
  "success": true,
  "data": {
    "total_candidates": 100,
    "score_range": {
      "min": 0.697864,
      "max": 1.0,
      "avg": 0.773319
    },
    "tier_breakdown": {
      "Good Match": 22,
      "Moderate Match": 78
    },
    "top_candidate": {...}
  }
}
```

### Candidate Object

```bash
{
  "candidate_id": "CAND_0039754",
  "rank": 1,
  "score": 1.0,
  "reasoning": "Good Match, Senior Applied Scientist..."
}
```

### Error Responses

```bash
{
  "success": false,
  "error": "Candidate not found: CAND_XXXXXXX"
}
```

### HTTP Status Codes

| Status | Meaning |
|--------|---------|
| `200` | Success |
| `400` | Bad Request |
| `404` | Not Found |
| `500` | Internal Server Error |


