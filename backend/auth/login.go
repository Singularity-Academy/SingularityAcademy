package auth

import (
	"backend/config"
	"backend/models"
	"backend/utils"
	"github.com/gin-gonic/gin"
	"net/http"
)

type LoginRequest struct {
	Email    string `json:"email" binding:"required"`
	Password string `json:"password" binding:"required"`
}

func Login(context *gin.Context) {

	var request LoginRequest

	// 绑定 JSON 数据到结构体
	if err := context.ShouldBindJSON(&request); err != nil {
		context.JSON(http.StatusBadRequest, gin.H{
			"error":  "invalid request data",
			"detail": err.Error(), // 返回具体的绑定错误信息
		})
		return
	}

	var users []models.User

	if err := config.DB.Where("email = ?", request.Email).Find(&users).Error; err != nil {
		context.JSON(http.StatusBadRequest, gin.H{
			"error":  "email or password is wrong",
			"detail": "email or password is wrong",
		})
		return
	}

	user := users[0]

	if !utils.CheckPassword(request.Password, user.Password) {
		context.JSON(http.StatusBadRequest, gin.H{
			"error":  "email or password is wrong",
			"detail": "email or password is wrong",
		})
		return
	}
	// 生成 JWT Token
	token, err := utils.GenerateToken(user.ID)
	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{
			"error":  "Failed to generate token",
			"detail": err.Error(),
		})
		return
	}
	Logger.Println(user.Username + " login success!")
	context.JSON(http.StatusOK, gin.H{
		"message": "login success",
		"token":   token,
	})
}
