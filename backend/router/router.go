package router

import (
	"net/http"
	"github.com/gin-gonic/gin"
)

func SetupRouter() *gin.Engine {
	// Create a new Gin router with default middleware (logging and recovery)
	r := gin.Default()

	// Define a route group for authentication-related endpoints
	auth := r.Group("/api/auth")
	{
		// Login route
		auth.POST("/login", func(ctx *gin.Context) {
			// Example response for login
			ctx.JSON(http.StatusOK, gin.H{
				"message": "Login endpoint hit",
			})
		})

		// Register route
		auth.POST("/register", func(ctx *gin.Context) {
			// Example response for registration
			ctx.JSON(http.StatusOK, gin.H{
				"message": "Register endpoint hit",
			})
		})
	}

	// Return the configured router
	return r
}