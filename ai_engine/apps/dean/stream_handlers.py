import base64
import json
import os
from datetime import datetime
import av.video
import numpy as np
import av
import asyncio
from dataclasses import dataclass
from typing import Optional

@dataclass
class StreamState:
    video_writer: Optional[av.VideoStream] = None
    audio_writer: Optional[av.AudioStream] = None
    output_dir: str = ""
    is_recording: bool = False

class SimpleStreamHandler:
    def __init__(self):
        self.output_dir = "recordings"
        os.makedirs(self.output_dir, exist_ok=True)
        self.writers = {}  # user_id -> (video_writer, audio_writer)
    
    def start_recording(self, user_id: str):
        # Create directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = os.path.join(self.output_dir, f"{user_id}_{timestamp}")
        os.makedirs(output_dir, exist_ok=True)
        
        # Create writers
        video_writer = av.open(os.path.join(output_dir, "video.mp4"), 'w', format='mp4')
        video_stream = video_writer.add_stream('h264', rate=5)
        video_stream.width = 320
        video_stream.height = 240
        
        audio_writer = av.open(os.path.join(output_dir, "audio.mp3"), 'w', format='mp3')
        audio_stream = audio_writer.add_stream('aac', rate=44100)
        audio_stream.channels = 1
        
        self.writers[user_id] = (video_writer, audio_writer)

    async def save_frame(self, user_id: str, frame_data: str, is_video: bool = True):
        if user_id not in self.writers:
            return
            
        video_writer, audio_writer = self.writers[user_id]
        data = base64.b64decode(frame_data)
        
        if is_video:
            # Save video frame
            frame = np.frombuffer(data, dtype=np.uint8).reshape((240, 320, 3))
            frame = av.VideoFrame.from_ndarray(frame, format='rgb24')
            for packet in video_writer.streams.video[0].encode(frame):
                video_writer.mux(packet)
        else:
            # Save audio frame
            frame = av.AudioFrame.from_ndarray(
                np.frombuffer(data, dtype=np.int16).reshape(-1, 1),
                format='s16',
                layout='mono'
            )
            for packet in audio_writer.streams.audio[0].encode(frame):
                audio_writer.mux(packet)

    def stop_recording(self, user_id: str):
        if user_id not in self.writers:
            return
            
        video_writer, audio_writer = self.writers[user_id]
        video_writer.close()
        audio_writer.close()
        del self.writers[user_id]

# Example usage:
"""
@bp.websocket('/stream')
async def handle_stream(request, ws: WebSocket):
    user_id = request.ctx.user_id
    handler = SimpleStreamHandler()
    handler.start_recording(user_id)
    
    async for message in ws:
        data = json.loads(message)
        if data.get('video'):
            await handler.save_frame(user_id, data['video'], is_video=True)
        elif data.get('audio'):
            await handler.save_frame(user_id, data['audio'], is_video=False)
    
    handler.stop_recording(user_id)
"""
