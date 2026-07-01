// cors.go
// CORS middleware for HireSense_AI Backend
// Allows Gradio frontend and Next.js to connect

package middleware

import (
	"hiresense-backend/config"

	"github.com/gin-gonic/gin"
)

// CORS sets Cross-Origin Resource Sharing headers
// Allows Gradio sandbox and Next.js frontend to connect
func CORS(cfg *config.Config) gin.HandlerFunc {
	return func(c *gin.Context) {

		origin := c.Request.Header.Get("Origin")
		if origin == "" {
			origin = cfg.AllowOrigin
		}

		c.Header("Access-Control-Allow-Origin", origin)
		c.Header("Access-Control-Allow-Methods",
			"GET, POST, PUT, DELETE, OPTIONS, PATCH",
		)
		c.Header("Access-Control-Allow-Headers",
			"Origin, Content-Type, Accept, Authorization, "+
				"X-Requested-With, X-API-Key",
		)
		c.Header("Access-Control-Allow-Credentials", "true")
		c.Header("Access-Control-Max-Age", "86400")

		if c.Request.Method == "OPTIONS" {
			c.AbortWithStatus(204)
			return
		}

		c.Next()
	}
}