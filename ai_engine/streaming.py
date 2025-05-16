"""
Module for handling streaming LLM responses with buffering.
"""

import asyncio
from typing import AsyncGenerator, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import uuid
from loguru import logger

@dataclass
class StreamChunk:
    """Represents a chunk of streamed data."""
    content: str
    message_id: str
    timestamp: datetime
    is_final: bool = False
    error: Optional[str] = None

async def stream_with_buffer(
    stream: AsyncGenerator[str, None],
    message_id: Optional[str] = None,
    buffer_size: int = 30,
    websocket: Optional[Any] = None
) -> AsyncGenerator[StreamChunk, None]:
    """
    Stream content with buffering.
    
    Args:
        stream: Async generator yielding content chunks
        message_id: Optional message ID for tracking
        buffer_size: Number of characters to buffer before sending
        websocket: Optional websocket to send chunks to directly
        
    Yields:
        StreamChunk objects containing buffered content
    """
    message_id = message_id or str(uuid.uuid4())
    buffer = ""
    last_send_time = datetime.now()
    
    try:
        async for token in stream:
            buffer += token
            
            # Send chunk if buffer is full or enough time has passed
            current_time = datetime.now()
            if len(buffer) >= buffer_size or (current_time - last_send_time).total_seconds() >= 0.1:
                chunk = StreamChunk(
                    content=buffer,
                    message_id=message_id,
                    timestamp=current_time
                )
                
                # Send to websocket if provided
                if websocket:
                    try:
                        await websocket.send(chunk.__dict__)
                    except Exception as e:
                        logger.error(f"Error sending to websocket: {e}")
                
                yield chunk
                buffer = ""
                last_send_time = current_time
        
        # Send any remaining content
        if buffer:
            chunk = StreamChunk(
                content=buffer,
                message_id=message_id,
                timestamp=datetime.now(),
                is_final=True
            )
            
            if websocket:
                try:
                    await websocket.send(chunk.__dict__)
                except Exception as e:
                    logger.error(f"Error sending final chunk to websocket: {e}")
            
            yield chunk
            
    except Exception as e:
        logger.error(f"Error in stream processing: {e}")
        error_chunk = StreamChunk(
            content="",
            message_id=message_id,
            timestamp=datetime.now(),
            is_final=True,
            error=str(e)
        )
        
        if websocket:
            try:
                await websocket.send(error_chunk.__dict__)
            except Exception as ws_error:
                logger.error(f"Error sending error chunk to websocket: {ws_error}")
        
        yield error_chunk 