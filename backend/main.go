package main

import (
	"backend/auth"
	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

func main() {
	r := gin.Default()
	r.Use(cors.New(cors.Config{
		AllowOrigins:     []string{"http://localhost:3000"},                   // 允许访问的来源
		AllowMethods:     []string{"GET", "POST", "PUT", "DELETE"},            // 允许的方法
		AllowHeaders:     []string{"Origin", "Content-Type", "Authorization"}, // 允许的请求头
		AllowCredentials: true,                                                // 是否允许携带认证信息
	}))
	r.POST("/api/auth/register", auth.Register)
	r.POST("/api/auth/login", auth.Login)
	err := r.Run(":8080")
	if err != nil {
		return
	}
}
