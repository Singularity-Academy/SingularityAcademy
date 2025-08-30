package auth

import (
	"backend/code"
	"backend/config"
	"backend/models"
	"backend/response"
	"backend/utils"
	"github.com/gin-gonic/gin"
)

// RegisterRequest 定义注册请求结构
type RegisterRequest struct {
	Username string `json:"name" binding:"required"`
	Password string `json:"password" binding:"required"`
	Email    string `json:"email" binding:"required"`
}

func Register(context *gin.Context) {
	r, _ := context.Get("json")
	request := r.(*RegisterRequest)

	// 验证邮箱格式
	if !utils.IsValidEmail(request.Email) {
		response.Fail(context, code.Errors.InvalidEmailAddress)
		return
	}

	// 检查邮箱是否已注册
	users, err := utils.FindUsersByEmail(request.Email)
	if err != nil {
		response.Fail(context, code.Errors.FailedToCheckEmail)
		return
	}

	if len(users) != 0 {
		response.Fail(context, code.Errors.EmailAlreadyRegistered)
		return
	}

	// 创建新用户
	var user models.User
	user.ID = utils.GenerateSnowflakeID()
	user.Username = request.Username
	user.Email = request.Email
	user.Password, err = utils.Encrypt(request.Password)

	if err != nil {
		response.Fail(context, code.Errors.FailedToEncryptPassword)
		return
	}

	// 初始化其他字段
	user.IsVerified = false
	user.VerificationToken, err = utils.GenerateSecureRandomString(10)

	if err != nil {
		response.Fail(context, code.Errors.FailedToGenerateVerificationToken)
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
	response.Success(context, "Registration successful, please check your email for verification")
}
