// router.go
// Route definitions for HireSense_AI Backend
// Gin Framework | Port 8080

package routes

import (
	"github.com/gin-gonic/gin"

	"hiresense-backend/config"
	"hiresense-backend/handlers"
	"hiresense-backend/middleware"
	"hiresense-backend/services"
)

// SetupRouter initializes Gin router with all routes
// and middleware for HireSense_AI Backend
func SetupRouter(cfg *config.Config) *gin.Engine {

	// Set Gin mode
	if cfg.Environment == "production" {
		gin.SetMode(gin.ReleaseMode)
	} else {
		gin.SetMode(gin.DebugMode)
	}

	router := gin.New()

	// Global middleware
	router.Use(middleware.Logger())
	router.Use(middleware.CORS(cfg))
	router.Use(gin.Recovery())

	// Initialize services
	csvService     := services.NewCSVService(cfg.CSVPath)
	rankingService := services.NewRankingService(csvService)

	// Initialize handlers
	healthHandler    := handlers.NewHealthHandler(csvService)
	candidateHandler := handlers.NewCandidateHandler(rankingService)
	rankingHandler   := handlers.NewRankingHandler(rankingService)

	// ----------------------------------------------------------------
	// Health routes
	// ----------------------------------------------------------------

	router.GET("/health", healthHandler.Check)
	router.GET("/ping",   healthHandler.Ping)

	// ----------------------------------------------------------------
	// API v1 routes
	// ----------------------------------------------------------------

	v1 := router.Group("/api/v1")
	{
		// Candidate routes
		candidates := v1.Group("/candidates")
		{
			// GET /api/v1/candidates
			// Returns paginated list of all candidates
			// Query: page, page_size
			candidates.GET("", candidateHandler.GetAll)

			// GET /api/v1/candidates/search
			// Search candidates by query
			// Query: q, min_score, max_rank, page, page_size
			candidates.GET(
				"/search",
				candidateHandler.Search,
			)

			// GET /api/v1/candidates/rank/:rank
			// Get candidate by rank position (1-100)
			candidates.GET(
				"/rank/:rank",
				candidateHandler.GetByRank,
			)

			// GET /api/v1/candidates/:id
			// Get candidate by candidate_id
			candidates.GET(
				"/:id",
				candidateHandler.GetByID,
			)
		}

		// Ranking routes
		ranking := v1.Group("/ranking")
		{
			// GET /api/v1/ranking/top10
			ranking.GET("/top10",  rankingHandler.GetTop10)

			// GET /api/v1/ranking/top50
			ranking.GET("/top50",  rankingHandler.GetTop50)

			// GET /api/v1/ranking/top100
			ranking.GET("/top100", rankingHandler.GetTop100)

			// GET /api/v1/ranking/stats
			ranking.GET("/stats",  rankingHandler.GetStats)
		}
	}

	return router
}