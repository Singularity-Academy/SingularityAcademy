package ws

import (
	"backend/models"
	"backend/utils"
	"fmt"
	"github.com/gorilla/websocket"
	"net/url"
)

// VideoHandler 处理 WebSocket 请求
func VideoHandler(conn *websocket.Conn, user models.User) {
	// Connect to Python AI engine
	u := url.URL{Scheme: "ws", Host: "localhost:8765", Path: "/"}
	aiConn, _, err := websocket.DefaultDialer.Dial(u.String(), nil)
	if err != nil {
		fmt.Println("Failed to connect to AI engine:", err)
		return
	}
	defer aiConn.Close()

	// Handle client connection closure
	defer func(conn *websocket.Conn) {
		err := conn.Close()
		if err != nil {
			fmt.Println("WebSocket failed to disconnected:" + err.Error())
		}
	}(conn)

	fmt.Println("WebSocket connected!")

	// Send welcome message
	err = conn.WriteMessage(websocket.TextMessage, []byte("hello "+user.Username))
	if err != nil {
		return
	}

	// Start goroutine to handle AI engine responses
	go func() {
		for {
			_, msg, err := aiConn.ReadMessage()
			if err != nil {
				fmt.Println("Error reading from AI engine:", err)
				return
			}
			// Forward AI response to client
			err = conn.WriteMessage(websocket.TextMessage, msg)
			if err != nil {
				fmt.Println("Error writing to client:", err)
				return
			}
		}
	}()

	// Main loop to handle client messages
	for {
		// Listen for messages from client
		_, msg, err := conn.ReadMessage()
		if err != nil {
			fmt.Println("Error reading message:", err)
			return
		}

		// Forward video/audio data to AI engine
		if utils.IsImage(msg) || utils.IsAudio(msg) {
			err = aiConn.WriteMessage(websocket.BinaryMessage, msg)
			if err != nil {
				fmt.Println("Error forwarding to AI engine:", err)
				return
			}
		}
		if utils.IsImage(msg) {
			fmt.Println("收到视频数据")
			err = aiConn.WriteMessage(websocket.BinaryMessage, msg)
			if err != nil {
				fmt.Println("Error forwarding to AI engine:", err)
				return
			}
		} else if utils.IsAudio(msg) {
			fmt.Println("收到音频数据")
			err = aiConn.WriteMessage(websocket.BinaryMessage, msg)
			if err != nil {
				fmt.Println("Error forwarding to AI engine:", err)
				return
			}
		}
	}
}
