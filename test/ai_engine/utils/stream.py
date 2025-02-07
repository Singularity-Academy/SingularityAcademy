import cv2
import numpy as np
from typing import Literal
import io

class StreamProcessor:
    def detect_type(self, data: bytes) -> Literal["image", "audio", "unknown"]:
        # Check for image signatures
        if data[:2] == b'\xFF\xD8':  # JPEG
            return "image"
        if data[:8] == b'\x89PNG\r\n\x1a\n':  # PNG
            return "image"
            
        # Check for audio signatures
        if data[:4] == b'RIFF' and data[8:12] == b'WAVE':  # WAV
            return "audio"
        if data[:3] == b'ID3' or data[:2] == b'\xFF\xFB':  # MP3
            return "audio"
            
        return "unknown"
        
    def preprocess_image(self, image_data: bytes):
        # Convert bytes to numpy array
        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 