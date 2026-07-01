// config.go
// Configuration loader for HireSense_AI Backend

package config

import (
	"os"
)

// Config holds all application configuration
type Config struct {
	Port        string
	Environment string
	CSVPath     string
	AllowOrigin string
}

// Load reads configuration from environment variables
// with sensible defaults for local development
func Load() *Config {
	return &Config{
		Port:        getEnv("PORT", "8080"),
		Environment: getEnv("ENVIRONMENT", "production"),
		CSVPath:     getEnv("CSV_PATH", "../outputs/HireSense_AI.csv"),
		AllowOrigin: getEnv("ALLOW_ORIGIN", "*"),
	}
}

func getEnv(key, defaultValue string) string {
	value := os.Getenv(key)
	if value == "" {
		return defaultValue
	}
	return value
}
