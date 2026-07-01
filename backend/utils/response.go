// response.go
// Standard API response helpers for HireSense_AI Backend

package utils

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

// APIResponse is the standard response envelope
type APIResponse struct {
	Success bool        `json:"success"`
	Message string      `json:"message,omitempty"`
	Data    interface{} `json:"data,omitempty"`
	Error   string      `json:"error,omitempty"`
}

// OK sends a 200 success response
func OK(c *gin.Context, data interface{}) {
	c.JSON(http.StatusOK, APIResponse{
		Success: true,
		Data:    data,
	})
}

// OKWithMessage sends a 200 success response with message
func OKWithMessage(
	c *gin.Context,
	message string,
	data interface{},
) {
	c.JSON(http.StatusOK, APIResponse{
		Success: true,
		Message: message,
		Data:    data,
	})
}

// BadRequest sends a 400 error response
func BadRequest(c *gin.Context, message string) {
	c.JSON(http.StatusBadRequest, APIResponse{
		Success: false,
		Error:   message,
	})
}

// NotFound sends a 404 error response
func NotFound(c *gin.Context, message string) {
	c.JSON(http.StatusNotFound, APIResponse{
		Success: false,
		Error:   message,
	})
}

// InternalError sends a 500 error response
func InternalError(c *gin.Context, message string) {
	c.JSON(http.StatusInternalServerError, APIResponse{
		Success: false,
		Error:   message,
	})
}

// Paginate calculates pagination values
func Paginate(page, pageSize, total int) (
	offset int,
	totalPages int,
) {
	if page < 1 {
		page = 1
	}
	if pageSize < 1 {
		pageSize = 10
	}
	if pageSize > 100 {
		pageSize = 100
	}
	offset     = (page - 1) * pageSize
	totalPages = (total + pageSize - 1) / pageSize
	return offset, totalPages
}