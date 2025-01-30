package handlers

import (
	"backend/models"
	"backend/utils"
	"fmt"
	"github.com/gorilla/websocket"
)

// VideoHandler 处理 WebSocket 请求
func VideoHandler(conn *websocket.Conn, user models.User) {
	defer conn.Close()

	fmt.Println("WebSocket connected!")

	err := conn.WriteMessage(websocket.TextMessage, []byte("hello "+user.Username))
	if err != nil {
		return
	}

	for {
		// 监听并接收来自前端的消息
		_, msg, err := conn.ReadMessage()
		if err != nil {
			fmt.Println("Error reading message:", err)
			return
		}
		if utils.IsImage(msg) {
			fmt.Println("received image from client!")
		}
		if utils.IsAudio(msg) {
			fmt.Println("received audio from client!")
		}
	}
}
