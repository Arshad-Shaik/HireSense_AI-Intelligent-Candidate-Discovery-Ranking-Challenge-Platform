// ranking.go
// Ranking handlers for HireSense_AI Backend

package handlers

import (
	"github.com/gin-gonic/gin"

	"hiresense-backend/services"
	"hiresense-backend/utils"
)

// RankingHandler handles ranking endpoints
type RankingHandler struct {
	ranking *services.RankingService
}

// NewRankingHandler creates a new RankingHandler
func NewRankingHandler(
	ranking *services.RankingService,
) *RankingHandler {
	return &RankingHandler{ranking: ranking}
}

// GetTop10 handles GET /api/v1/ranking/top10
// Returns top 10 candidates — highest NDCG@10 weight
func (h *RankingHandler) GetTop10(c *gin.Context) {

	page     := parseIntQuery(c, "page", 1)
	pageSize := parseIntQuery(c, "page_size", 10)

	response := h.ranking.GetTopN(10, page, pageSize)

	utils.OKWithMessage(
		c,
		"Top 10 AI/ML candidates by HireSense_AI ranking",
		response,
	)
}

// GetTop50 handles GET /api/v1/ranking/top50
// Returns top 50 candidates
func (h *RankingHandler) GetTop50(c *gin.Context) {

	page     := parseIntQuery(c, "page", 1)
	pageSize := parseIntQuery(c, "page_size", 25)

	response := h.ranking.GetTopN(50, page, pageSize)

	utils.OKWithMessage(
		c,
		"Top 50 AI/ML candidates by HireSense_AI ranking",
		response,
	)
}

// GetTop100 handles GET /api/v1/ranking/top100
// Returns all 100 ranked candidates
func (h *RankingHandler) GetTop100(c *gin.Context) {

	page     := parseIntQuery(c, "page", 1)
	pageSize := parseIntQuery(c, "page_size", 25)

	response := h.ranking.GetTopN(100, page, pageSize)

	utils.OKWithMessage(
		c,
		"Top 100 AI/ML candidates by HireSense_AI ranking",
		response,
	)
}

// GetStats handles GET /api/v1/ranking/stats
// Returns aggregate statistics about the ranking
func (h *RankingHandler) GetStats(c *gin.Context) {

	stats := h.ranking.GetStats()

	utils.OKWithMessage(
		c,
		"HireSense_AI ranking statistics",
		stats,
	)
}