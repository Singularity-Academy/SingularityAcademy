package middlewares

import (
	"backend/code"
	"backend/models"
	"backend/response"
	"backend/utils"
	"github.com/gin-gonic/gin"
	"github.com/gorilla/websocket"
	"log"
	"net/http"
	"strings"
)

func JwtMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		// 获取 Authorization 头部中的 Token
		authHeader := c.GetHeader("Authorization")
		if authHeader == "" {
			response.Fail(c, code.Errors.AuthorizationHeaderIsRequired)
			return
		}

		// 去掉 "Bearer " 前缀
		tokenString := strings.TrimPrefix(authHeader, "Bearer ")
		if tokenString == "" {
			response.Fail(c, code.Errors.TokenIsRequired)
			return
		}

		// 解析 Token 并验证
		claims, err := utils.ParseToken(tokenString)
		if err != nil {
			response.Fail(c, code.Errors.InvalidToken)
			return
		}

		var users []models.User
		// 查找id所对应的用户
		users, err = utils.FindUsersByID(claims.ID)
		if err != nil || len(users) == 0 {
			response.Fail(c, code.Errors.InvalidToken)
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
				"error":  "api.auth.invalidContentTypeHeader",
				"detail": "Unsupported content type, expected 'application/json'",
			})
			c.Abort()
			return
		}

		// 绑定 JSON 数据
		if err := c.ShouldBindJSON(&requestTemplate); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{
				"error":  "api.auth.invalidRequestData",
				"detail": "Failed to bind JSON: " + err.Error(),
			})
			c.Abort()
			return
		}
		c.Set("json", requestTemplate)
		c.Next()
	}
}

var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		return true // 允许所有跨域 WebSocket 连接
	},
}

// WebSocketMiddleware WebSocket 认证中间件（可以传入不同的 WebSocket 业务处理函数）
func WebSocketMiddleware(handlerFunc func(*websocket.Conn, models.User)) gin.HandlerFunc {
	return func(c *gin.Context) {
		authHeader := c.Query("token")

		if authHeader == "" {
			c.JSON(http.StatusUnauthorized, gin.H{"error": "api.auth.tokenIsRequired"})
			return
		}

		claims, err := utils.ParseToken(authHeader)
		if err != nil {
			c.JSON(http.StatusUnauthorized, gin.H{"error": "api.auth.invalidToken"})
			return
		}

		users, err := utils.FindUsersByID(claims.ID)
		if err != nil || len(users) == 0 {
			c.JSON(http.StatusUnauthorized, gin.H{"error": "api.auth.userNotFound"})
			return
		}

		user := users[0]

		conn, err := upgrader.Upgrade(c.Writer, c.Request, nil)
		if err != nil {
			log.Println("failed to upgrade the connection:", err)
			return
		}

		go handlerFunc(conn, user)
	}
}
