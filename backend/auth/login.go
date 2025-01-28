package auth

import (
	"backend/utils"
	"github.com/gin-gonic/gin"
	"net/http"
)

type LoginRequest struct {
	Email    string `json:"email" binding:"required"`
	Password string `json:"password" binding:"required"`
}

func Login(context *gin.Context) {
	r, _ := context.Get("json")
	request := r.(*LoginRequest)

	users, err := utils.FindUsersByEmail(request.Email)
	if err != nil {
		context.JSON(http.StatusNotFound, gin.H{
			"error":  "email or password is wrong",
			"detail": "email or password is wrong",
		})
		return
	}

	if len(users) == 0 {
		context.JSON(http.StatusNotFound, gin.H{
			"error":  "email or password is wrong",
			"detail": "email or password is wrong",
		})
		return
	}

	user := users[0]

	if !utils.CheckPassword(request.Password, user.Password) {
		context.JSON(http.StatusNotFound, gin.H{
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
