package auth

import (
	"backend/code"
	"backend/config"
	"backend/response"
	"backend/utils"
	"github.com/gin-gonic/gin"
)

type VerifyRequest struct {
	Token string `json:"token" binding:"required"`
}

func Verify(context *gin.Context) {
	r, _ := context.Get("json")
	request := r.(*VerifyRequest)

	users, err := utils.FindUsersByVerifyToken(request.Token)
	if err != nil {
		response.Fail(context, code.Errors.InvalidToken)
		return
	}

	if len(users) == 0 {
		response.Fail(context, code.Errors.InvalidToken)
		return
	}

	user := users[0]

	if user.IsVerified {
		response.FailCode(context, code.Errors.BadRequest.Code, "user already verified")
		return
	}

	user.IsVerified = true

	go config.DB.Save(&user)

	Logger.Println(user.Username + " verified!")

	response.Success(context, "user verified")
}
