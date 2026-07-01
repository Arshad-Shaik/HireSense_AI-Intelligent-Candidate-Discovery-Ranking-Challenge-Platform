# `docs/ranking_formula.md`


### HireSense_AI — Ranking Formula

### Final Score Formula

```plaintext
final_score = compute_weighted_score(
similarity_score,
experience_score,
skill_score,
behavior_score,
trust_score,
profile_score,
boost_score,
penalty_score
)
```


### Weight Configuration

```python
WEIGHTS = {
    "similarity": 0.70,  # Semantic relevance dominates
    "skills":     0.12,  # Technical skill alignment
    "experience": 0.08,  # Professional maturity
    "profile":    0.04,  # Profile quality
    "behavior":   0.03,  # Recruiter engagement
    "trust":      0.03,  # Verification signals
}
```

### Component Score Formulas

### Similarity Score

```python
similarity = max(0.0, 1.0 - chromadb_distance)
Range: 0.455 to 0.650 (bge-small on this dataset)
```

### Experience Score

```python
experience_score = min(years_of_experience / 15.0, 1.0)
Saturation at 15 years
```

### Skill Score

```python
skill_score =
    (skill_count / 20.0)          * 0.30
  + (endorsements / 50.0)         * 0.20
  + (avg_duration_months / 48.0)  * 0.15
  + (avg_assessment / 100.0)      * 0.20
  + (github_activity / 100.0)     * 0.15
```

### Behavior Score

```python
behavior_score =
    recruiter_response_rate    * 0.25
  + offer_acceptance_rate      * 0.15
  + interview_completion_rate  * 0.20
  + recency_score              * 0.20
  + response_speed_score       * 0.10
  + open_to_work               * 0.10
```

### Trust Score

```python
trust_score =
    verified_email     * 0.30
  + verified_phone     * 0.30
  + linkedin_connected * 0.20
  + github_linked      * 0.20
```

### Profile Score

```python
profile_score =
    (completeness / 100.0)          * 0.35
  + (text_length / 1000.0)          * 0.15
  + career_stability_score          * 0.15
  + (saved_by_recruiters / 20.0)    * 0.15
  + (search_appearance / 500.0)     * 0.10
  + (connection_count / 1000.0)     * 0.10
```

### Weighted Core Score

```python
weighted_core = (
    0.70 * similarity_score
  + 0.12 * skill_score
  + 0.08 * experience_score
  + 0.04 * profile_score
  + 0.03 * behavior_score
  + 0.03 * trust_score
)
```

### Boost and Penalty

```python
boost_adjustment   = min(boost_score, 0.08)
penalty_adjustment = min(penalty_score, 0.10)

final_score = weighted_core + boost - penalty
final_score = max(0.0, final_score)
```

### Score Normalization

```python
normalized = (score - min_score) / (max_score - min_score)
Tie-break: candidate_id ascending
```

### Tier Classification

| Score Range | Tier |
|-------------|------|
| ≥ 0.90 | Elite Match |
| ≥ 0.80 | Strong Match |
| ≥ 0.70 | Good Match |
| ≥ 0.60 | Moderate Match |
| ≥ 0.50 | Partial Match |
| < 0.50 | Weak Match |


