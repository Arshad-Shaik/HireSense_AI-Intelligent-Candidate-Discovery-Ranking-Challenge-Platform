// ranking.go
// Ranking response models for HireSense_AI Backend

package models

// RankingResponse is the standard API response
// for ranking endpoints
type RankingResponse struct {
	Total      int         `json:"total"`
	Page       int         `json:"page"`
	PageSize   int         `json:"page_size"`
	TotalPages int         `json:"total_pages"`
	Data       []Candidate `json:"data"`
}

// RankingStats contains aggregate statistics
// about the ranking results
type RankingStats struct {
	TotalCandidates int            `json:"total_candidates"`
	ScoreRange      ScoreRange     `json:"score_range"`
	TierBreakdown   map[string]int `json:"tier_breakdown"`
	TopCandidate    Candidate      `json:"top_candidate"`
}

// ScoreRange holds min and max scores
type ScoreRange struct {
	Min float64 `json:"min"`
	Max float64 `json:"max"`
	Avg float64 `json:"avg"`
}

// SearchRequest is the request body for search
type SearchRequest struct {
	Query    string `json:"query"`
	Page     int    `json:"page"`
	PageSize int    `json:"page_size"`
	MinScore float64 `json:"min_score"`
	MaxRank  int    `json:"max_rank"`
}

// FilterRequest for filtering candidates
type FilterRequest struct {
	Tier     string  `json:"tier"`
	MinScore float64 `json:"min_score"`
	MaxScore float64 `json:"max_score"`
	MinRank  int     `json:"min_rank"`
	MaxRank  int     `json:"max_rank"`
	Page     int     `json:"page"`
	PageSize int     `json:"page_size"`
}