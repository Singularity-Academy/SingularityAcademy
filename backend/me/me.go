package me

import (
	"backend/models"
	"backend/response"
	"github.com/gin-gonic/gin"
)

func Me(context *gin.Context) {
	user, _ := context.Get("user")
	response.Success(context, gin.H{
		"id":    user.(models.User).ID,
		"name":  user.(models.User).Username,
		"email": user.(models.User).Email,
	})
}
