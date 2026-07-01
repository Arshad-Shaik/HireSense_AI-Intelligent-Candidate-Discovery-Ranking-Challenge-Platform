// candidates.go
// Candidate handlers for HireSense_AI Backend

package handlers

import (
	"strconv"

	"github.com/gin-gonic/gin"

	"hiresense-backend/services"
	"hiresense-backend/utils"
)

// CandidateHandler handles candidate endpoints
type CandidateHandler struct {
	ranking *services.RankingService
}

// NewCandidateHandler creates a new CandidateHandler
func NewCandidateHandler(
	ranking *services.RankingService,
) *CandidateHandler {
	return &CandidateHandler{ranking: ranking}
}

// GetAll handles GET /api/v1/candidates
// Returns paginated list of all 100 candidates
func (h *CandidateHandler) GetAll(c *gin.Context) {

	page     := parseIntQuery(c, "page", 1)
	pageSize := parseIntQuery(c, "page_size", 10)

	response := h.ranking.GetPaginated(page, pageSize)

	utils.OK(c, response)
}

// GetByID handles GET /api/v1/candidates/:id
// Returns single candidate by candidate_id
func (h *CandidateHandler) GetByID(c *gin.Context) {

	id := c.Param("id")

	if id == "" {
		utils.BadRequest(c, "candidate_id is required")
		return
	}

	candidate, found := h.ranking.GetByID(id)
	if !found {
		utils.NotFound(
			c,
			"Candidate not found: "+id,
		)
		return
	}

	utils.OK(c, candidate)
}

// GetByRank handles GET /api/v1/candidates/rank/:rank
// Returns single candidate by rank position
func (h *CandidateHandler) GetByRank(c *gin.Context) {

	rankStr := c.Param("rank")

	rank, err := strconv.Atoi(rankStr)
	if err != nil || rank < 1 || rank > 100 {
		utils.BadRequest(
			c,
			"rank must be an integer between 1 and 100",
		)
		return
	}

	candidate, found := h.ranking.GetByRank(rank)
	if !found {
		utils.NotFound(
			c,
			"No candidate found at rank "+rankStr,
		)
		return
	}

	utils.OK(c, candidate)
}

// Search handles GET /api/v1/candidates/search
// Query params: q, min_score, max_rank, page, page_size
func (h *CandidateHandler) Search(c *gin.Context) {

	query    := c.Query("q")
	page     := parseIntQuery(c, "page", 1)
	pageSize := parseIntQuery(c, "page_size", 10)
	maxRank  := parseIntQuery(c, "max_rank", 0)

	minScoreStr := c.Query("min_score")
	minScore    := 0.0
	if minScoreStr != "" {
		if v, err := strconv.ParseFloat(
			minScoreStr, 64,
		); err == nil {
			minScore = v
		}
	}

	response := h.ranking.Search(
		query,
		minScore,
		maxRank,
		page,
		pageSize,
	)

	utils.OK(c, response)
}

// parseIntQuery safely parses an integer query param
func parseIntQuery(
	c *gin.Context,
	key string,
	defaultVal int,
) int {
	val := c.Query(key)
	if val == "" {
		return defaultVal
	}
	parsed, err := strconv.Atoi(val)
	if err != nil || parsed < 1 {
		return defaultVal
	}
	return parsed
}