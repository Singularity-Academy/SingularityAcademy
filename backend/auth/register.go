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

	var request RegisterRequest

	// 绑定 JSON 数据到结构体
	if err := context.ShouldBindJSON(&request); err != nil {
		context.JSON(http.StatusBadRequest, gin.H{
			"error":  "invalid request data",
			"detail": err.Error(), // 返回具体的绑定错误信息
		})
		return
	}

	var user models.User
	var err error

	user.ID = utils.GenerateSnowflakeID()
	user.Username = request.Username
	user.Email = request.Email
	user.Password, err = utils.Encrypt(request.Password)

	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{
			"error":  "invalid request data",
			"detail": err.Error(), // 返回具体的绑定错误信息
		})
		return
	}

	config.DB.Create(&user)
	Logger.Println(user.Username + " register success!")
	context.JSON(http.StatusOK, gin.H{
		"message": "register success",
	})

}
