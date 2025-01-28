package handlers

import (
	"log"
	"net/http"

	"github.com/gorilla/websocket"
)

var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		return true // In production, implement proper origin checking
	},
}

func HandleVideoStream(w http.ResponseWriter, r *http.Request) {
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Printf("Error upgrading to websocket: %v", err)
		return
	}
	defer conn.Close()

	for {
		messageType, p, err := conn.ReadMessage()
		if err != nil {
			if websocket.IsUnexpectedCloseError(err, websocket.CloseGoingAway, websocket.CloseAbnormalClosure) {
				log.Printf("Error reading message: %v", err)
			}
			break
		}

		// Here you can:
		// 1. Save the video chunks to disk
		// 2. Process the video stream
		// 3. Forward to other clients
		// 4. Send to AI processing service
		// etc.

		// Echo back for testing
		if err := conn.WriteMessage(messageType, p); err != nil {
			log.Printf("Error writing message: %v", err)
			break
		}
	}
}
