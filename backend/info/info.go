package info

import (
	"backend/utils"
	"github.com/gin-gonic/gin"
	"strconv"
)

func Info(context *gin.Context) {
	idStr := context.Param("id")
	id, err := strconv.ParseUint(idStr, 10, 64)
	if err != nil {
		// 如果转换失败，返回错误信息
		context.JSON(400, gin.H{
			"error":  "Invalid ID",
			"detail": err.Error(),
		})
		return
	}

	users, err := utils.FindUsersByID(id)
	if err != nil {
		// 用户查找失败，返回 404
		context.JSON(404, gin.H{
			"error":  "User not found",
			"detail": err.Error(),
		})
		return
	}

	if len(users) == 0 {
		// 如果没有找到用户，返回 404
		context.JSON(404, gin.H{
			"error":  "User not found",
			"detail": "No users found with the given ID",
		})
		return
	}

	user := users[0]
	context.JSON(200, gin.H{
		"id":    user.ID,
		"name":  user.Username,
		"email": user.Email,
	})
}
