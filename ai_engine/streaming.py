"""
Module for handling streaming LLM responses with buffering.
"""

import asyncio
import json
import inspect
from typing import AsyncGenerator, Dict, Any, Optional, Type
from datetime import datetime
import uuid
from loguru import logger

async def stream_with_buffer(
    stream: AsyncGenerator[str, None],
    message_id: Optional[str] = None,
    buffer_size: int = 30,
    websocket: Optional[Any] = None
):
    """
    Stream content with buffering directly to a websocket.
    
    Args:
        stream: Async generator yielding content chunks
        message_id: Optional message ID for tracking
        buffer_size: Number of characters to buffer before sending
        websocket: Websocket to send chunks to directly
    """
    if not websocket:
        logger.warning("No websocket provided to stream_with_buffer, no data will be sent")
        return
        
    message_id = message_id or str(uuid.uuid4())
    buffer = []
    last_send_time = datetime.now()
    
    try:
        async for token in stream:
            # Convert Pydantic models to dictionaries
            if hasattr(token, 'model_dump'):
                token = token.model_dump()
            
            # Handle different chunk types
            if isinstance(token, dict):
                buffer.append(token)
                if len(buffer) >= buffer_size:
                    await websocket.send(json.dumps({
                        "message_id": message_id,
                        "content": buffer,
                        "timestamp": datetime.now().isoformat()
                    }))
                    buffer = []
            
            # Send chunk if buffer is full or enough time has passed
            current_time = datetime.now()
            if len(buffer) >= buffer_size or (current_time - last_send_time).total_seconds() >= 0.1:
                await websocket.send(json.dumps({
                    "message_id": message_id,
                    "content": buffer,
                    "timestamp": current_time.isoformat(),
                    "is_final": False
                }))
                
                buffer = []
                last_send_time = current_time
        
        # Send any remaining content
        if buffer:
            await websocket.send(json.dumps({
                "message_id": message_id,
                "content": buffer,
                "timestamp": datetime.now().isoformat(),
                "is_final": True
            }))
            
    except Exception as e:
        logger.error(f"Error in stream processing: {e}")
        import traceback
        traceback.print_exc()
        
        try:
            await websocket.send(json.dumps({
                "message_id": message_id,
                "content": "",
                "timestamp": datetime.now().isoformat(),
                "is_final": True,
                "error": str(e)
            }))
        except Exception as ws_error:
            logger.error(f"Error sending error message to websocket: {ws_error}") 