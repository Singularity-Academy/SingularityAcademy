package response

/*
类说明：
HTTP响应封装类，对应Code状态码详见../code/error.go

结构为{状态码，消息，数据}
成功的消息状态码为0，消息为success
*/

import (
	"backend/code"
	"github.com/gin-gonic/gin"
	"net/http"
)

type Response struct {
	Code    int         `json:"code"`
	Message string      `json:"message"`
	Data    interface{} `json:"data"`
}

func Success(c *gin.Context, data interface{}) {
	c.JSON(http.StatusOK, Response{
		Code:    0,
		Message: "success",
		Data:    data,
	})
}

func FailCode(c *gin.Context, code int, message string) {
	c.JSON(http.StatusOK, Response{
		Code:    code,
		Message: message,
		Data:    nil,
	})
}

func Fail(c *gin.Context, error code.Error) {
	c.JSON(http.StatusOK, Response{
		Code:    error.Code,
		Message: error.Message,
		Data:    nil,
	})
}
