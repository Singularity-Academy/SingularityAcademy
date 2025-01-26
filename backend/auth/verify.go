package auth

import (
	"backend/config"
	"backend/utils"
	"github.com/gin-gonic/gin"
	"net/http"
)

type VerifyRequest struct {
	Token string `json:"token" binding:"required"`
}

func Verify(context *gin.Context) {
	var request VerifyRequest

	// 绑定 JSON 数据到结构体
	if err := context.ShouldBindJSON(&request); err != nil {
		context.JSON(http.StatusBadRequest, gin.H{
			"error":  "invalid request data",
			"detail": err.Error(), // 返回具体的绑定错误信息
		})
		return
	}

	users, err := utils.FindUsersByVerifyToken(request.Token)
	if err != nil {
		context.JSON(http.StatusUnauthorized, gin.H{
			"error":  "invalid verification token",
			"detail": "invalid verification token",
		})
		return
	}

	if len(users) == 0 {
		context.JSON(http.StatusUnauthorized, gin.H{
			"error":  "invalid verification token",
			"detail": "invalid verification token",
		})
		return
	}

	user := users[0]

	if user.IsVerified {
		context.JSON(http.StatusUnauthorized, gin.H{
			"error":  "user already verified",
			"detail": "user already verified",
		})
		return
	}

	user.IsVerified = true

	go config.DB.Save(&user)

	Logger.Println(user.Username + " verified!")

	context.JSON(http.StatusOK, gin.H{
		"message": "user verified",
	})
}
