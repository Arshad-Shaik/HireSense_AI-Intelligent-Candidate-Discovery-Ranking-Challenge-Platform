// health.go
// Health check handler for HireSense_AI Backend

package handlers

import (
	"net/http"
	"time"

	"github.com/gin-gonic/gin"

	"hiresense-backend/services"
	"hiresense-backend/utils"
)

// HealthHandler handles health check endpoints
type HealthHandler struct {
	csv *services.CSVService
}

// NewHealthHandler creates a new HealthHandler
func NewHealthHandler(
	csv *services.CSVService,
) *HealthHandler {
	return &HealthHandler{csv: csv}
}

// HealthResponse is the health check response
type HealthResponse struct {
	Status    string `json:"status"`
	Service   string `json:"service"`
	Version   string `json:"version"`
	Timestamp string `json:"timestamp"`
	CSVLoaded bool   `json:"csv_loaded"`
}

// Check handles GET /health
// Returns service health status
func (h *HealthHandler) Check(c *gin.Context) {
	utils.OK(c, HealthResponse{
		Status:    "healthy",
		Service:   "HireSense_AI Backend",
		Version:   "1.0.0",
		Timestamp: time.Now().UTC().Format(time.RFC3339),
		CSVLoaded: h.csv.IsLoaded(),
	})
}

// Ping handles GET /ping
// Simple liveness check
func (h *HealthHandler) Ping(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{
		"message": "pong",
		"service": "HireSense_AI",
	})
}