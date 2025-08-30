package info

import (
	"backend/code"
	"backend/response"
	"backend/utils"
	"github.com/gin-gonic/gin"
	"strconv"
)

func Info(context *gin.Context) {
	idStr := context.Param("id")
	id, err := strconv.ParseUint(idStr, 10, 64)
	if err != nil {
		// 如果转换失败，返回 BadRequest
		response.FailCode(context, code.Errors.BadRequest.Code, "Invalid ID")
		return
	}

	users, err := utils.FindUsersByID(id)
	if err != nil {
		// 用户查找失败，返回 NotFound
		response.FailCode(context, code.Errors.NotFound.Code, "User not found")
		return
	}

	if len(users) == 0 {
		// 如果没有找到用户，返回 NotFound
		response.FailCode(context, code.Errors.NotFound.Code, "No users found with the given ID")
		return
	}

	user := users[0]
	response.Success(context, gin.H{
		"id":    user.ID,
		"name":  user.Username,
		"email": user.Email,
	})
}
