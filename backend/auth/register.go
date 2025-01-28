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

// 错误响应函数
func registerError(c *gin.Context, errorMessage, detailMessage string) {
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
		registerError(context, "Invalid email address", "Invalid email address")
		return
	}

	// 检查邮箱是否已注册
	users, err := utils.FindUsersByEmail(request.Email)
	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{
			"error":  "Failed to check email",
			"detail": err.Error(),
		})
		return
	}

	if len(users) != 0 {
		registerError(context, "Email already registered", "This email is already registered")
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
			"error":  "Failed to encrypt password",
			"detail": err.Error(),
		})
		return
	}

	// 初始化其他字段
	user.IsVerified = false
	user.VerificationToken, err = utils.GenerateSecureRandomString(10)

	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{
			"error":  "Failed to generate verification token",
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
