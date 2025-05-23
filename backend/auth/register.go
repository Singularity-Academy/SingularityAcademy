package auth

import (
	"backend/config"
	"backend/models"
	"backend/utils"
	"github.com/gin-gonic/gin"
	"net/http"
)

// RegisterRequest 定义注册请求结构
type RegisterRequest struct {
	Username string `json:"name" binding:"required"`
	Password string `json:"password" binding:"required"`
	Email    string `json:"email" binding:"required"`
}


func registerError(c *gin.Context, errorMessage, detailMessage string) {
	if detailMessage == "" {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": errorMessage,
		})
		return
	}
	c.JSON(http.StatusBadRequest, gin.H{
		"error":  errorMessage,
		"detail": detailMessage,
	})
}

func Register(context *gin.Context) {
	r, _ := context.Get("json")
	request := r.(*RegisterRequest)

	// 验证邮箱格式
	if !utils.IsValidEmail(request.Email) {
		registerError(context, "api.auth.invalidEmailAddress", "")
		return
	}

	// 检查邮箱是否已注册
	users, err := utils.FindUsersByEmail(request.Email)
	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{
			"error":  "api.auth.failedToCheckEmail",
			"detail": err.Error(),
		})
		return
	}

	if len(users) != 0 {
		registerError(context, "api.auth.emailAlreadyRegistered", "")
		return
	}

	// 创建新用户
	var user models.User
	user.ID = utils.GenerateSnowflakeID()
	user.Username = request.Username
	user.Email = request.Email
	user.Password, err = utils.Encrypt(request.Password)

	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{
			"error":  "api.auth.failedToEncryptPassword",
			"detail": err.Error(),
		})
		return
	}

	// 初始化其他字段
	user.IsVerified = false
	user.VerificationToken, err = utils.GenerateSecureRandomString(10)

	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{
			"error":  "api.auth.failedToGenerateVerificationToken",
			"detail": err.Error(),
		})
		return
	}

	// 异步发送验证邮件
	go config.SendVerifyEmail(user.Email, user.VerificationToken)

	// 异步创建用户
	go func() {
		err := config.DB.Create(&user).Error
		if err != nil {
			Logger.Println("Failed to create user:", err.Error())
		}
	}()

	// 注册成功
	Logger.Println(user.Username + " register success!")
	context.JSON(http.StatusOK, gin.H{
		"message": "Registration successful, please check your email for verification",
	})
}
