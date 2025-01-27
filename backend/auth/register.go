package auth

import (
	"backend/config"
	"backend/models"
	"backend/utils"
	"github.com/gin-gonic/gin"
	"net/http"
)

type RegisterRequest struct {
	Username string `json:"name" binding:"required"`
	Password string `json:"password" binding:"required"`
	Email    string `json:"email" binding:"required"`
}

func Register(context *gin.Context) {

	r, _ := context.Get("json")
	request := r.(*RegisterRequest)

	if !utils.IsValidEmail(request.Email) {
		context.JSON(http.StatusBadRequest, gin.H{
			"error":  "invalid email address",
			"detail": "invalid email address",
		})
	}

	users, err := utils.FindUsersByEmail(request.Email)
	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{
			"error":  "The email has been registered",
			"detail": "The email has been registered",
		})
		return
	}

	if len(users) != 0 {
		context.JSON(http.StatusInternalServerError, gin.H{
			"error":  "The email has been registered",
			"detail": "The email has been registered",
		})
		return
	}

	var user models.User

	user.ID = utils.GenerateSnowflakeID()
	user.Username = request.Username
	user.Email = request.Email
	user.Password, err = utils.Encrypt(request.Password)

	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{
			"error":  "failed to encrypt password",
			"detail": err.Error(), // 返回具体的绑定错误信息
		})
		return
	}

	user.IsVerified = false
	user.VerificationToken, err = utils.GenerateSecureRandomString(10)

	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{
			"error":  "failed to generate verification token",
			"detail": err.Error(), // 返回具体的绑定错误信息
		})
		return
	}

	go config.SendVerifyEmail(user.Email, user.VerificationToken)

	go config.DB.Create(&user)

	Logger.Println(user.Username + " register success!")
	context.JSON(http.StatusOK, gin.H{
		"message": "register success",
	})

}
