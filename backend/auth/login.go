package auth

import (
	"backend/code"
	"backend/response"
	"backend/utils"
	"github.com/gin-gonic/gin"
)

// LoginRequest 定义登录请求结构
type LoginRequest struct {
	Email    string `json:"email" binding:"required"`
	Password string `json:"password" binding:"required"`
}

func Login(context *gin.Context) {
	r, _ := context.Get("json")
	request := r.(*LoginRequest)

	// 查找用户
	users, err := utils.FindUsersByEmail(request.Email)
	if err != nil || len(users) == 0 {
		response.Fail(context, code.Errors.IncorrectEmailOrPassword)
		return
	}

	user := users[0]

	// 检查密码
	if !utils.CheckPassword(request.Password, user.Password) {
		response.Fail(context, code.Errors.IncorrectEmailOrPassword)
		return
	}

	// 生成 JWT Token
	token, err := utils.GenerateToken(user.ID)
	if err != nil {
		response.Fail(context, code.Errors.FailedToGenerateToken)
		return
	}

	// 记录登录日志
	Logger.Println("User", user.Username, "logged in successfully!")

	// 返回成功响应
	response.Success(context, token)
}
