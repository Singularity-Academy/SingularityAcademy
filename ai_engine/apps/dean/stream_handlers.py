import base64
import json
import os
import logging
from datetime import datetime
import av.video
import numpy as np
import av
import asyncio
from dataclasses import dataclass
from typing import Optional
from ai_engine.logging import logger, log_exception

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class StreamState:
    video_writer: Optional[av.VideoStream] = None
    audio_writer: Optional[av.AudioStream] = None
    output_dir: str = ""
    is_recording: bool = False

class StreamHandler:
    """Handler for managing a single user's audio/video stream recording."""
    
    def __init__(self, user_id: str):
        """Initialize a stream handler for a specific user.
        
        Args:
            user_id: Unique identifier for the user
        """
        self.user_id = user_id
        self.output_dir = "recordings"
        self.state = StreamState()
        os.makedirs(self.output_dir, exist_ok=True)
        logger.info(f"Initialized StreamHandler for user {user_id}")

    def start_recording(self) -> None:
        """Start recording the user's stream."""
        try:
            # Create directory with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = os.path.join(self.output_dir, f"{self.user_id}_{timestamp}")
            os.makedirs(output_dir, exist_ok=True)
            
            # Create video writer
            video_container = av.open(os.path.join(output_dir, "video.mp4"), 'w', format='mp4')
            video_stream = video_container.add_stream('h264', rate=5)
            video_stream.width = 320
            video_stream.height = 240
            
            # Create audio writer - using WAV format with PCM encoding
            audio_container = av.open(os.path.join(output_dir, "audio.wav"), 'w', format='wav')
            audio_stream = audio_container.add_stream('pcm_s16le', rate=44100)
            #audio_stream.channels = 1
            
            # Update state
            self.state = StreamState(
                video_writer=video_container,
                audio_writer=audio_container,
                output_dir=output_dir,
                is_recording=True
            )
            logger.info(f"Started recording for user {self.user_id} in {output_dir}")
            
        except Exception as e:
            log_exception(e, f"Failed to start recording for user {self.user_id}")

    async def save_video_frame(self, frame_data: str) -> None:
        """Save a video frame from the user's stream.
        
        Args:
            frame_data: Base64 encoded video frame data
        """
        try:
            if not self.state.is_recording:
                logger.warning(f"No active recording for user {self.user_id}")
                return
                
            if not self.state.video_writer:
                logger.error(f"No video writer for user {self.user_id}")
                return

            data = base64.b64decode(frame_data)
            frame = np.frombuffer(data, dtype=np.uint8).reshape((240, 320, 3))
            frame = av.VideoFrame.from_ndarray(frame, format='rgb24')
            
            for packet in self.state.video_writer.streams.video[0].encode(frame):
                self.state.video_writer.mux(packet)
                
        except Exception as e:
            log_exception(e, f"Error saving video frame for user {self.user_id}")

    async def save_audio_frame(self, frame_data: str) -> None:
        """Save an audio frame from the user's stream.
        
        Args:
            frame_data: Base64 encoded audio frame data
        """
        try:
            if not self.state.is_recording:
                logger.warning(f"No active recording for user {self.user_id}")
                return
                
            if not self.state.audio_writer:
                logger.error(f"No audio writer for user {self.user_id}")
                return

            data = base64.b64decode(frame_data)
            # Reshape the audio data to (1, samples) for mono audio
            audio_data = np.frombuffer(data, dtype=np.int16)
            audio_data = audio_data.reshape(1, -1)  # Reshape to (1, samples)
            frame = av.AudioFrame.from_ndarray(
                audio_data,
                format='s16',
                layout='mono'
            )
            
            for packet in self.state.audio_writer.streams.audio[0].encode(frame):
                self.state.audio_writer.mux(packet)
                
        except Exception as e:
            log_exception(e, f"Error saving audio frame for user {self.user_id}")

    def stop_recording(self) -> None:
        """Stop recording the user's stream and clean up resources."""
        try:
            if not self.state.is_recording:
                logger.warning(f"No active recording to stop for user {self.user_id}")
                return
                
            if self.state.video_writer:
                self.state.video_writer.close()
            if self.state.audio_writer:
                self.state.audio_writer.close()
                
            self.state.is_recording = False
            logger.info(f"Stopped recording for user {self.user_id}")
            
        except Exception as e:
            log_exception(e, f"Error stopping recording for user {self.user_id}")

# Example usage:
"""
@bp.websocket('/stream')
async def handle_stream(request, ws: WebSocket):
    user_id = request.ctx.user_id
    handler = StreamHandler(user_id)
    
    try:
        handler.start_recording()
        
        async for message in ws:
            data = json.loads(message)
            if data.get('video'):
                await handler.save_video_frame(data['video'])
            elif data.get('audio'):
                await handler.save_audio_frame(data['audio'])
                
    except Exception as e:
        logger.error(f"Stream handling error for user {user_id}: {str(e)}")
    finally:
        handler.stop_recording()
"""
