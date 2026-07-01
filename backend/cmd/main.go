// main.go
// HireSense_AI Backend Entry Point
// Redrob AI Intelligent Candidate Discovery & Ranking Challenge
// Go + Gin Framework | Port 8080

package main

import (
	"context"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"hiresense-backend/config"
	"hiresense-backend/routes"
)

func main() {

	// Load configuration
	cfg := config.Load()

	// Initialize router
	router := routes.SetupRouter(cfg)

	// HTTP server
	server := &http.Server{
		Addr:         ":" + cfg.Port,
		Handler:      router,
		ReadTimeout:  30 * time.Second,
		WriteTimeout: 30 * time.Second,
		IdleTimeout:  60 * time.Second,
	}

	// Start server in goroutine
	go func() {
		log.Printf("HireSense_AI Backend starting on port %s", cfg.Port)
		log.Printf("Environment : %s", cfg.Environment)
		log.Printf("CSV Path    : %s", cfg.CSVPath)

		if err := server.ListenAndServe(); err != nil &&
			err != http.ErrServerClosed {
			log.Fatalf("Server failed to start: %v", err)
		}
	}()

	// Graceful shutdown
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	log.Println("Shutting down HireSense_AI Backend...")

	ctx, cancel := context.WithTimeout(
		context.Background(),
		10*time.Second,
	)
	defer cancel()

	if err := server.Shutdown(ctx); err != nil {
		log.Fatalf("Server forced to shutdown: %v", err)
	}

	log.Println("HireSense_AI Backend stopped.")
}