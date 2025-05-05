from sanic import Sanic
from sanic.blueprints import Blueprint
from ujson import loads, dumps
from .exceptions import AuthError
from .auth import AuthManager
import base64
import os
import time

# Create frames directory if it doesn't exist
os.makedirs("frames", exist_ok=True)

bp = Blueprint("ws", url_prefix="/ai/ws")
bp.ctx.auth = AuthManager.from_env()

@bp.websocket("/stream")
async def ws(request, ws):
    """
    Handles a single WebSocket Video & Audio streaming connection.
    Lifecycle:
     - accepts and waits for auth msg
     - check auth data and verifies it
     - returns auth_ok msg
     - starts recieving video & audio chunks
    Frontend -> backend auth msg:
    {
        "type": "auth",
        "token": "1234567890"
    }
    Backend -> frontend auth_ok msg:
    {
        "type": "auth_response",
        "status": "success",
        "user_id": "1234567890"
    }
    Stream data:
    {
        "packet_id": 123,
        "time": 1234567890, # unix timestamp
        "video": "base64_encoded_video_data",
        "audio": "base64_encoded_audio_data"
    }
    """
    print("WebSocket connection established")
    try:
        # Wait for authentication message
        print("Waiting for auth message...")
        auth_message = await ws.recv()
        auth_data = loads(auth_message)
        if auth_data.get("type") != "auth" or not auth_data.get("token"):
            print("Invalid auth data format")
            raise AuthError("Invalid message type")
        
        # Verify auth token
        token = auth_data.get("token")
        print(f"Verifying token: {token[:10]}...")
        if not bp.ctx.auth.verify_token(token):
            print("Token verification failed")
            raise AuthError("Invalid token")

        print("Auth successful, sending success response")
        await ws.send(dumps({
            "type": "auth_response",
            "status": "success",
            "user_id": "1234567890"
            }))
        
        # Create a unique session folder using timestamp
        session_id = int(time.time())
        session_dir = f"frames/session_{session_id}"
        os.makedirs(session_dir, exist_ok=True)
        print(f"Created session directory: {session_dir}")
        
        # Start receiving video & audio chunks
        print("Starting to receive video/audio data")
        while True:
            chunk = await ws.recv()
            try:
                chunk_data = loads(chunk)
                
                # Process video frames
                if chunk_data.get("video") is not None:
                    packet_id = chunk_data.get('packet_id')
                    print(f"Received video packet #{packet_id} at time {chunk_data.get('time')}")
                    
                    # Decode base64 data and save as image file
                    try:
                        # Get the base64 encoded frame
                        base64_data = chunk_data.get("video")
                        
                        # Decode the base64 data
                        image_data = base64.b64decode(base64_data)
                        
                        # Save to file
                        file_path = f"{session_dir}/frame_{packet_id}.jpg"
                        with open(file_path, "wb") as f:
                            f.write(image_data)
                        
                        print(f"Saved frame #{packet_id} to {file_path}")
                    except Exception as e:
                        print(f"Error saving frame #{packet_id}: {e}")
                    
                    # Send acknowledgment if needed
                    await ws.send(dumps({
                        "type": "ack",
                        "packet_id": packet_id,
                        "message": f"Frame {packet_id} received and saved"
                    }))
                
                # Process audio frames
                if chunk_data.get("audio") is not None:
                    packet_id = chunk_data.get('packet_id')
                    print(f"Received audio packet #{packet_id} at time {chunk_data.get('time')}")
                    
                    # Here you can process the base64-encoded audio data
                    # For example, saving audio to a file:
                    """
                    try:
                        base64_data = chunk_data.get("audio").split(",")[1] if "," in chunk_data.get("audio") else chunk_data.get("audio")
                        audio_data = base64.b64decode(base64_data)
                        file_path = f"{session_dir}/audio_{packet_id}.wav"
                        with open(file_path, "wb") as f:
                            f.write(audio_data)
                    except Exception as e:
                        print(f"Error saving audio #{packet_id}: {e}")
                    """
                
            except Exception as e:
                print(f"Error processing message: {e}")
                print(f"Message content (first 100 chars): {str(chunk)[:100]}")
            
    except AuthError as e:
        print(f"Authentication error: {e}")
        await ws.send(dumps({
            "type": "auth_response",
            "status": "error",
            "message": str(e)
        }))
    except Exception as e:
        print(f"WebSocket error: {e}")
        raise
    finally:
        # Ensure connection is closed
        print("WebSocket connection closed")
        await ws.close()