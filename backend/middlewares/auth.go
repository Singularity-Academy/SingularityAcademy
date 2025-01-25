package middlewares

import (
	"backend/models"
	"backend/utils"
	"github.com/gin-gonic/gin"
	"net/http"
	"strings"
)

func JwtMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		// 获取 Authorization 头部中的 Token
		authHeader := c.GetHeader("Authorization")
		if authHeader == "" {
			c.JSON(http.StatusUnauthorized, gin.H{"error": "Authorization header is required"})
			c.Abort()
			return
		}

		// 去掉 "Bearer " 前缀
		tokenString := strings.TrimPrefix(authHeader, "Bearer ")
		if tokenString == "" {
			c.JSON(http.StatusUnauthorized, gin.H{"error": "Token is required"})
			c.Abort()
			return
		}

		// 解析 Token 并验证
		claims, err := utils.ParseToken(tokenString)
		if err != nil {
			c.JSON(http.StatusUnauthorized, gin.H{"error": "Invalid token"})
			c.Abort()
			return
		}

		var users []models.User
		users, err = utils.FindUsersByID(claims.ID)
		if err != nil {
			c.JSON(http.StatusUnauthorized, gin.H{"error": "Invalid token"})
		}

		if len(users) == 0 {
			c.JSON(http.StatusUnauthorized, gin.H{"error": "Invalid token"})
		}

		// 将解析出的 Claims 放入上下文中
		c.Set("user", users[0])

		// 继续执行后续处理
		c.Next()
	}
}

func IsJsonMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		if !strings.Contains(c.GetHeader("Content-Type"), "application/json") {
			c.JSON(http.StatusBadRequest, gin.H{
				"detail": "unsupported content type, expected 'application/json'",
			})
			c.Abort()
			return
		}
		c.Next()
	}
}
