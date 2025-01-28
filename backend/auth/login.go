package auth

import (
	"backend/utils"
	"github.com/gin-gonic/gin"
	"net/http"
)

// LoginRequest 定义登录请求结构
type LoginRequest struct {
	Email    string `json:"email" binding:"required"`
	Password string `json:"password" binding:"required"`
}

// 错误响应函数
func loginError(c *gin.Context, message string) {
	c.JSON(http.StatusUnauthorized, gin.H{
		"error":  message,
		"detail": message,
	})
}

func Login(context *gin.Context) {
	r, _ := context.Get("json")
	request := r.(*LoginRequest)

	// 查找用户
	users, err := utils.FindUsersByEmail(request.Email)
	if err != nil || len(users) == 0 {
		// 用户不存在或者查询出错，统一返回 "email or password is wrong"
		loginError(context, "email or password is wrong")
		return
	}

	user := users[0]

	// 检查密码
	if !utils.CheckPassword(request.Password, user.Password) {
		loginError(context, "email or password is wrong")
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

	// 记录登录日志
	Logger.Println("User", user.Username, "logged in successfully!")

	// 返回成功响应
	context.JSON(http.StatusOK, gin.H{
		"message": "login success",
		"token":   token,
	})
}
