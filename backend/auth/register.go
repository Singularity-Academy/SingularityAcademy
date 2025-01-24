package auth

import (
	"github.com/gin-gonic/gin"
	"net/http"
)

func Register(context *gin.Context) {
	context.JSON(http.StatusOK, gin.H{
		"message": "pong",
	})
}
