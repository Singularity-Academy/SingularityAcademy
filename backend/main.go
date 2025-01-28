package main

import (
	"backend/auth"
	"backend/config"
	"backend/info"
	"backend/me"
	"backend/middlewares"
	"backend/models"
	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"log"
)

func main() {
	// 加载配置文件
	config.LoadConfig()

	// 连接 SMTP 和数据库
	config.ConnectSMTP()
	config.ConnectDatabase()

	// 执行数据库自动迁移
	err := config.DB.AutoMigrate(&models.User{})
	if err != nil {
		log.Fatal("Database migration failed: ", err) // 打印错误日志
		return
	}

	// 创建 Gin 引擎
	r := gin.Default()

	// 设置 CORS 配置
	r.Use(cors.New(cors.Config{
		AllowOrigins:     []string{"*"}, // 生产环境应该指定允许的域名
		AllowMethods:     []string{"GET", "POST", "PUT", "DELETE"},
		AllowHeaders:     []string{"Origin", "Content-Type", "Authorization", "X-Real-IP"},
		AllowCredentials: true,
	}))
	r.POST("/api/auth/register", middlewares.JsonMiddleware(&auth.RegisterRequest{}), auth.Register)
	r.POST("/api/auth/login", middlewares.JsonMiddleware(&auth.LoginRequest{}), auth.Login)
	r.POST("/api/auth/verify", middlewares.JsonMiddleware(&auth.VerifyRequest{}), auth.Verify)
	r.GET("/api/me", middlewares.JwtMiddleware(), me.Me)
	r.GET("/api/info/:id", middlewares.JwtMiddleware(), info.Info)

	// 启动服务器
	err = r.Run("0.0.0.0:8080")
	if err != nil {
		log.Fatal("Server failed to start: ", err) // 打印错误日志
		return
	}
}
