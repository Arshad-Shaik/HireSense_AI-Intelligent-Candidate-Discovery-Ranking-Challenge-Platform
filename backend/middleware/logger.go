// logger.go
// Request logger middleware for HireSense_AI Backend

package middleware

import (
	"log"
	"time"

	"github.com/gin-gonic/gin"
)

// Logger logs all incoming HTTP requests
// with method, path, status, latency
func Logger() gin.HandlerFunc {
	return func(c *gin.Context) {

		start  := time.Now()
		path   := c.Request.URL.Path
		method := c.Request.Method

		c.Next()

		latency    := time.Since(start)
		statusCode := c.Writer.Status()
		clientIP   := c.ClientIP()

		log.Printf(
			"[HireSense] %s | %3d | %13v | %15s | %s %s",
			time.Now().Format("2006/01/02 - 15:04:05"),
			statusCode,
			latency,
			clientIP,
			method,
			path,
		)

		// Log errors if any
		if len(c.Errors) > 0 {
			for _, e := range c.Errors {
				log.Printf(
					"[HireSense] ERROR: %s",
					e.Error(),
				)
			}
		}
	}
}