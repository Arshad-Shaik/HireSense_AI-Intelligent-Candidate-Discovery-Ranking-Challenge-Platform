// candidate.go
// Candidate data models for HireSense_AI Backend

package models

// Candidate represents a ranked candidate
// from HireSense_AI.csv submission file
type Candidate struct {
	CandidateID string  `json:"candidate_id"`
	Rank        int     `json:"rank"`
	Score       float64 `json:"score"`
	Reasoning   string  `json:"reasoning"`
}

// CandidateDetail represents enriched candidate
// with parsed reasoning signals
type CandidateDetail struct {
	CandidateID string   `json:"candidate_id"`
	Rank        int      `json:"rank"`
	Score       float64  `json:"score"`
	Reasoning   string   `json:"reasoning"`
	Tier        string   `json:"tier"`
	Signals     []string `json:"signals"`
}

// ParseTierFromReasoning extracts match tier
// from reasoning string
func ParseTierFromReasoning(reasoning string) string {
	tiers := []string{
		"Elite Match",
		"Strong Match",
		"Good Match",
		"Moderate Match",
		"Partial Match",
		"Weak Match",
	}
	for _, tier := range tiers {
		if len(reasoning) >= len(tier) {
			if reasoning[:len(tier)] == tier {
				return tier
			}
		}
	}
	return "Unknown"
}