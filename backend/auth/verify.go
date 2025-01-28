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

// 错误响应函数
func verifyError(c *gin.Context, errorMessage, detailMessage string) {
	c.JSON(http.StatusUnauthorized, gin.H{
		"error":  errorMessage,
		"detail": detailMessage,
	})
}

func Verify(context *gin.Context) {
	r, _ := context.Get("json")
	request := r.(*VerifyRequest)

	// 查找用户
	users, err := utils.FindUsersByVerifyToken(request.Token)
	if err != nil || len(users) == 0 {
		verifyError(context, "Invalid verification token", "Invalid verification token")
		return
	}

	user := users[0]

	// 用户已验证
	if user.IsVerified {
		verifyError(context, "User already verified", "User already verified")
	}

	// 更新用户为已验证状态
	user.IsVerified = true

	// 异步保存用户信息
	go func() {
		err := config.DB.Save(&user).Error
		if err != nil {
			Logger.Println("Failed to save user verification status:", err.Error())
		}
	}()

	Logger.Println(user.Username + " verified!")

	// 返回成功消息
	context.JSON(http.StatusOK, gin.H{
		"message": "User verified successfully",
	})
}
