# HireSense_AI — Database Schema

## `Candidate Schema`

`Source: candidates.jsonl (100K records)`

```json
{
  "candidate_id": "CAND_0000001",
  "profile": {
    "anonymized_name": "string",
    "headline": "string",
    "summary": "string",
    "location": "string",
    "country": "string",
    "years_of_experience": 6.9,
    "current_title": "string",
    "current_company": "string",
    "current_company_size": "10001+",
    "current_industry": "string"
  },
  "career_history": [{
    "company": "string",
    "title": "string",
    "start_date": "2024-03-08",
    "end_date": null,
    "duration_months": 27,
    "is_current": true,
    "industry": "string",
    "company_size": "string",
    "description": "string"
  }],
  "education": [{
    "institution": "string",
    "degree": "string",
    "field_of_study": "string",
    "start_year": 2017,
    "end_year": 2020,
    "grade": "string",
    "tier": "tier_3"
  }],
  "skills": [{
    "name": "string",
    "proficiency": "advanced",
    "endorsements": 37,
    "duration_months": 26
  }],
  "certifications": [{
    "name": "string",
    "issuer": "string",
    "year": 2023
  }],
  "languages": [{
    "language": "English",
    "proficiency": "professional"
  }],
  "redrob_signals": {
    "profile_completeness_score": 86.9,
    "signup_date": "2025-10-16",
    "last_active_date": "2026-05-20",
    "open_to_work_flag": true,
    "profile_views_received_30d": 23,
    "applications_submitted_30d": 2,
    "recruiter_response_rate": 0.34,
    "avg_response_time_hours": 177.8,
    "skill_assessment_scores": {"NLP": 38.8},
    "connection_count": 356,
    "endorsements_received": 35,
    "notice_period_days": 60,
    "expected_salary_range_inr_lpa": {
      "min": 18.7, "max": 36.1
    },
    "preferred_work_mode": "onsite",
    "willing_to_relocate": false,
    "github_activity_score": 9.2,
    "search_appearance_30d": 249,
    "saved_by_recruiters_30d": 4,
    "interview_completion_rate": 0.71,
    "offer_acceptance_rate": 0.58,
    "verified_email": true,
    "verified_phone": true,
    "linkedin_connected": false
  }
}
```

### Submission Output Schema

### `File: HireSense_AI.csv`

| Column | Type | Description |
|---------|---------|-------------|
| `candidate_id` | `string` | `CAND_XXXXXXX` format |
| `rank` | `int` | 1 to 100 |
| `score` | `float` | 0.0 to 1.0 normalized |
| `reasoning` | `string` | Signal-rich explanation |


### ChromaDB Schema

```plaintext
Collection: candidates
Documents: 100K embeddings
Dimension: 384 (BAAI/bge-small-en-v1.5)
Metadata: candidate_id per document
```