// ranking_service.go
// Ranking business logic for HireSense_AI Backend

package services

import (
	"hiresense-backend/models"
	"hiresense-backend/utils"
)

// RankingService provides ranking business logic
// on top of CSVService
type RankingService struct {
	csv *CSVService
}

// NewRankingService creates a new RankingService
func NewRankingService(csv *CSVService) *RankingService {
	return &RankingService{csv: csv}
}

// GetPaginated returns paginated ranking results
func (s *RankingService) GetPaginated(
	page int,
	pageSize int,
) models.RankingResponse {

	all := s.csv.GetAll()
	total := len(all)

	offset, totalPages := utils.Paginate(page, pageSize, total)

	end := offset + pageSize
	if end > total {
		end = total
	}

	var data []models.Candidate
	if offset < total {
		data = all[offset:end]
	} else {
		data = []models.Candidate{}
	}

	return models.RankingResponse{
		Total:      total,
		Page:       page,
		PageSize:   pageSize,
		TotalPages: totalPages,
		Data:       data,
	}
}

// GetTopN returns top N candidates with pagination
func (s *RankingService) GetTopN(
	n int,
	page int,
	pageSize int,
) models.RankingResponse {

	topN := s.csv.GetTopN(n)
	total := len(topN)

	offset, totalPages := utils.Paginate(page, pageSize, total)

	end := offset + pageSize
	if end > total {
		end = total
	}

	var data []models.Candidate
	if offset < total {
		data = topN[offset:end]
	} else {
		data = []models.Candidate{}
	}

	return models.RankingResponse{
		Total:      total,
		Page:       page,
		PageSize:   pageSize,
		TotalPages: totalPages,
		Data:       data,
	}
}

// GetStats returns ranking statistics
func (s *RankingService) GetStats() models.RankingStats {
	return s.csv.GetStats()
}

// GetByID returns single candidate by ID
func (s *RankingService) GetByID(
	id string,
) (*models.Candidate, bool) {
	return s.csv.GetByID(id)
}

// GetByRank returns single candidate by rank
func (s *RankingService) GetByRank(
	rank int,
) (*models.Candidate, bool) {
	return s.csv.GetByRank(rank)
}

// Search searches candidates by query
func (s *RankingService) Search(
	query string,
	minScore float64,
	maxRank int,
	page int,
	pageSize int,
) models.RankingResponse {

	results := s.csv.Search(query, minScore, maxRank)
	total   := len(results)

	offset, totalPages := utils.Paginate(page, pageSize, total)

	end := offset + pageSize
	if end > total {
		end = total
	}

	var data []models.Candidate
	if offset < total {
		data = results[offset:end]
	} else {
		data = []models.Candidate{}
	}

	return models.RankingResponse{
		Total:      total,
		Page:       page,
		PageSize:   pageSize,
		TotalPages: totalPages,
		Data:       data,
	}
}