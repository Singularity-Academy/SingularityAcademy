package middlewares

import (
	"backend/models"
	"backend/utils"
	"github.com/gin-gonic/gin"
	"net/http"
	"strings"
)

// 提取错误响应函数
func unauthorizedError(c *gin.Context, message, detail string) {
	c.JSON(http.StatusUnauthorized, gin.H{
		"error":  message,
		"detail": detail,
	})
	c.Abort()
}

func JwtMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		// 获取 Authorization 头部中的 Token
		authHeader := c.GetHeader("Authorization")
		if authHeader == "" {
			unauthorizedError(c, "Authorization header is required", "Authorization header is required")
			return
		}

		// 去掉 "Bearer " 前缀
		tokenString := strings.TrimPrefix(authHeader, "Bearer ")
		if tokenString == "" {
			unauthorizedError(c, "Token is required", "Token is required")
			return
		}

		// 解析 Token 并验证
		claims, err := utils.ParseToken(tokenString)
		if err != nil {
			unauthorizedError(c, "Invalid token", "Invalid token")
			return
		}

		var users []models.User
		// 查找id所对应的用户
		users, err = utils.FindUsersByID(claims.ID)
		if err != nil || len(users) == 0 {
			unauthorizedError(c, "Invalid token", "Invalid token")
			return
		}

		// 将解析出的用户放入上下文中
		c.Set("user", users[0])

		// 继续执行后续处理
		c.Next()
	}
}

func JsonMiddleware(requestTemplate interface{}) gin.HandlerFunc {
	return func(c *gin.Context) {
		if !strings.Contains(c.GetHeader("Content-Type"), "application/json") {
			c.JSON(http.StatusBadRequest, gin.H{
				"error":  "Invalid Content-Type header",
				"detail": "Unsupported content type, expected 'application/json'",
			})
			c.Abort()
			return
		}

		// 绑定 JSON 数据
		if err := c.ShouldBindJSON(&requestTemplate); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{
				"error":  "Invalid request data",
				"detail": "Failed to bind JSON: " + err.Error(),
			})
			c.Abort()
			return
		}
		c.Set("json", requestTemplate)
		c.Next()
	}
}
