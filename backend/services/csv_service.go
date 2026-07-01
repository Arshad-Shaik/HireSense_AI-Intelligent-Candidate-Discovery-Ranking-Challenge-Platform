// csv_service.go
// CSV loader service for HireSense_AI Backend
// Reads and caches HireSense_AI.csv ranking results

package services

import (
	"encoding/csv"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
	"sync"

	"hiresense-backend/models"
)

// CSVService handles loading and caching
// of HireSense_AI.csv ranking results
type CSVService struct {
	mu         sync.RWMutex
	candidates []models.Candidate
	csvPath    string
	loaded     bool
}

// NewCSVService creates a new CSVService instance
func NewCSVService(csvPath string) *CSVService {
	svc := &CSVService{
		csvPath: csvPath,
	}
	if err := svc.Load(); err != nil {
		log.Printf(
			"[CSVService] Warning: Could not load CSV: %v", err,
		)
	}
	return svc
}

// Load reads HireSense_AI.csv into memory
// Thread-safe. Can be called to reload.
func (s *CSVService) Load() error {
	s.mu.Lock()
	defer s.mu.Unlock()

	file, err := os.Open(s.csvPath)
	if err != nil {
		return fmt.Errorf(
			"cannot open CSV at %s: %w", s.csvPath, err,
		)
	}
	defer file.Close()

	reader := csv.NewReader(file)
	reader.LazyQuotes      = true
	reader.TrimLeadingSpace = true

	// Read header
	header, err := reader.Read()
	if err != nil {
		return fmt.Errorf("cannot read CSV header: %w", err)
	}

	// Validate header
	expected := []string{
		"candidate_id", "rank", "score", "reasoning",
	}
	for i, col := range expected {
		if i >= len(header) || header[i] != col {
			return fmt.Errorf(
				"invalid CSV header: expected %v got %v",
				expected, header,
			)
		}
	}

	// Read all rows
	var candidates []models.Candidate

	rows, err := reader.ReadAll()
	if err != nil {
		return fmt.Errorf("cannot read CSV rows: %w", err)
	}

	for i, row := range rows {
		if len(row) < 4 {
			log.Printf(
				"[CSVService] Skipping malformed row %d", i+2,
			)
			continue
		}

		rank, err := strconv.Atoi(strings.TrimSpace(row[1]))
		if err != nil {
			log.Printf(
				"[CSVService] Invalid rank at row %d: %v",
				i+2, err,
			)
			continue
		}

		score, err := strconv.ParseFloat(
			strings.TrimSpace(row[2]), 64,
		)
		if err != nil {
			log.Printf(
				"[CSVService] Invalid score at row %d: %v",
				i+2, err,
			)
			continue
		}

		candidates = append(candidates, models.Candidate{
			CandidateID: strings.TrimSpace(row[0]),
			Rank:        rank,
			Score:       score,
			Reasoning:   strings.TrimSpace(row[3]),
		})
	}

	s.candidates = candidates
	s.loaded     = true

	log.Printf(
		"[CSVService] Loaded %d candidates from %s",
		len(candidates), s.csvPath,
	)

	return nil
}

// GetAll returns all candidates
func (s *CSVService) GetAll() []models.Candidate {
	s.mu.RLock()
	defer s.mu.RUnlock()
	result := make([]models.Candidate, len(s.candidates))
	copy(result, s.candidates)
	return result
}

// GetByRank returns a candidate by rank (1-100)
func (s *CSVService) GetByRank(rank int) (
	*models.Candidate, bool,
) {
	s.mu.RLock()
	defer s.mu.RUnlock()

	for _, c := range s.candidates {
		if c.Rank == rank {
			return &models.Candidate{
				CandidateID: c.CandidateID,
				Rank:        c.Rank,
				Score:       c.Score,
				Reasoning:   c.Reasoning,
			}, true
		}
	}
	return nil, false
}

// GetByID returns a candidate by candidate_id
func (s *CSVService) GetByID(id string) (
	*models.Candidate, bool,
) {
	s.mu.RLock()
	defer s.mu.RUnlock()

	for _, c := range s.candidates {
		if c.CandidateID == id {
			return &models.Candidate{
				CandidateID: c.CandidateID,
				Rank:        c.Rank,
				Score:       c.Score,
				Reasoning:   c.Reasoning,
			}, true
		}
	}
	return nil, false
}

// GetTopN returns top N candidates
func (s *CSVService) GetTopN(n int) []models.Candidate {
	s.mu.RLock()
	defer s.mu.RUnlock()

	if n > len(s.candidates) {
		n = len(s.candidates)
	}

	result := make([]models.Candidate, n)
	copy(result, s.candidates[:n])
	return result
}

// GetStats returns aggregate statistics
func (s *CSVService) GetStats() models.RankingStats {
	s.mu.RLock()
	defer s.mu.RUnlock()

	if len(s.candidates) == 0 {
		return models.RankingStats{}
	}

	minScore := s.candidates[0].Score
	maxScore := s.candidates[0].Score
	totalScore := 0.0
	tierBreakdown := make(map[string]int)

	for _, c := range s.candidates {
		if c.Score < minScore {
			minScore = c.Score
		}
		if c.Score > maxScore {
			maxScore = c.Score
		}
		totalScore += c.Score

		tier := models.ParseTierFromReasoning(c.Reasoning)
		tierBreakdown[tier]++
	}

	avgScore := totalScore / float64(len(s.candidates))

	return models.RankingStats{
		TotalCandidates: len(s.candidates),
		ScoreRange: models.ScoreRange{
			Min: minScore,
			Max: maxScore,
			Avg: avgScore,
		},
		TierBreakdown: tierBreakdown,
		TopCandidate:  s.candidates[0],
	}
}

// Search returns candidates matching query string
// in candidate_id or reasoning field
func (s *CSVService) Search(
	query string,
	minScore float64,
	maxRank int,
) []models.Candidate {
	s.mu.RLock()
	defer s.mu.RUnlock()

	query = strings.ToLower(strings.TrimSpace(query))
	var results []models.Candidate

	for _, c := range s.candidates {
		if maxRank > 0 && c.Rank > maxRank {
			continue
		}
		if c.Score < minScore {
			continue
		}
		if query == "" {
			results = append(results, c)
			continue
		}
		if strings.Contains(
			strings.ToLower(c.CandidateID), query,
		) || strings.Contains(
			strings.ToLower(c.Reasoning), query,
		) {
			results = append(results, c)
		}
	}

	return results
}

// IsLoaded returns whether CSV was loaded successfully
func (s *CSVService) IsLoaded() bool {
	s.mu.RLock()
	defer s.mu.RUnlock()
	return s.loaded
}