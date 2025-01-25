package me

import (
	"backend/models"
	"github.com/gin-gonic/gin"
)

func Me(context *gin.Context) {
	user, _ := context.Get("user")
	context.JSON(200, gin.H{
		"id":    user.(models.User).ID,
		"name":  user.(models.User).Username,
		"email": user.(models.User).Email,
	})
}
