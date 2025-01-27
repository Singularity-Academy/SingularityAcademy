package main

import (
	"backend/auth"
	"backend/config"
	"backend/me"
	"backend/middlewares"
	"backend/models"
	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

func main() {
	config.LoadConfig()
	config.ConnectSMTP()
	config.ConnectDatabase()
	err := config.DB.AutoMigrate(&models.User{})
	if err != nil {
		return
	}
	r := gin.Default()
	r.Use(cors.New(cors.Config{
		AllowOrigins:     []string{"*"},                                                    // 允许访问的来源
		AllowMethods:     []string{"GET", "POST", "PUT", "DELETE"},                         // 允许的方法
		AllowHeaders:     []string{"Origin", "Content-Type", "Authorization", "X-Real-IP"}, // 允许的请求头
		AllowCredentials: true,                                                             // 是否允许携带认证信息
	}))
	r.POST("/api/auth/register", middlewares.JsonMiddleware(auth.RegisterRequest{}), auth.Register)
	r.POST("/api/auth/login", middlewares.JsonMiddleware(auth.LoginRequest{}), auth.Login)
	r.POST("/api/auth/verify", middlewares.JsonMiddleware(auth.VerifyRequest{}), auth.Verify)
	r.GET("/api/me", middlewares.JwtMiddleware(), me.Me)

	err = r.Run("0.0.0.0:8080")
	if err != nil {
		return
	}
}
