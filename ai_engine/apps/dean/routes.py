import uuid
from sanic import Blueprint, response
from sanic.exceptions import WebsocketClosed, InvalidUsage
import ujson as json
from pathlib import Path
import asyncio
from typing import Dict, Any, Optional, Set
from datetime import datetime
import shutil

from ai_engine.apps.auth.utils import handle_ws_login
from ai_engine.logging import logger, log_exception
from .stream_handlers import StreamHandler
from .ai_video_generator import AIVideoGenerator

bp = Blueprint("dean", url_prefix="/dean")

# Initialize video generator
video_generator = None
try:
    video_generator = AIVideoGenerator()
    logger.info("✅ AI Video Generator initialized successfully")
except Exception as e:
    logger.error(f"❌ Failed to initialize AI Video Generator: {e}")
    video_generator = None

# Video storage configuration
VIDEO_STORAGE = {
    "base_dir": Path("videos"),  # Base directory for video storage
    "temp_dir": Path("videos/temp"),  # Temporary directory for processing
    "max_age_days": 7,  # Maximum age of videos in days
}

# Active video generation sessions
active_generations: Dict[str, Dict[str, Any]] = {}  # video_uuid -> {ws, info, task}

# Ensure directories exist
VIDEO_STORAGE["base_dir"].mkdir(parents=True, exist_ok=True)
VIDEO_STORAGE["temp_dir"].mkdir(parents=True, exist_ok=True)

def get_video_path(video_uuid: str) -> Optional[Path]:
    """Get the path to a video file by UUID"""
    # First check in base directory
    video_path = VIDEO_STORAGE["base_dir"] / f"{video_uuid}.mp4"
    if video_path.exists():
        return video_path
    
    # Then check in temp directory
    video_path = VIDEO_STORAGE["temp_dir"] / f"{video_uuid}.mp4"
    if video_path.exists():
        return video_path
    
    return None

def get_video_info(video_uuid: str) -> Optional[Dict[str, Any]]:
    """Get video information from JSON file"""
    info_path = VIDEO_STORAGE["base_dir"] / f"{video_uuid}_info.json"
    if not info_path.exists():
        info_path = VIDEO_STORAGE["temp_dir"] / f"{video_uuid}_info.json"
    
    if info_path.exists():
        try:
            with open(info_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return None

@bp.websocket("/ws/<course_id>")
async def stream(request, ws, course_id):
    session_id = str(uuid.uuid4())[:8]
    stream_handler = None
    remote = request.remote_addr or request.ip
    logger.info(f"New WebSocket connection from {remote} (session: {session_id})")
    try:
        user = await handle_ws_login(request, ws, session_id)
        if not user:
            logger.info(f"WebSocket authentication unsuccessful (session: {session_id})")
            return

        # Initialize stream handler
        stream_handler = StreamHandler(user_id=user.id)
        stream_handler.start_recording()
        logger.info(f"Started recording for user {user.id}")

        while True:
            data = await ws.recv()
            data = json.loads(data)

            if data.get('video'):
                await stream_handler.save_video_frame(data['video'])
            if data.get('audio'):
                await stream_handler.save_audio_frame(data['audio'])

            logger.trace(f"Received data frames: {'audio' if data.get('audio') else ''} {'video' if data.get('video') else ''}")

    except WebsocketClosed:
        logger.info(f"WebSocket closed (session: {session_id})")
        return
    except Exception as e:
        log_exception(e, f"Error handling WebSocket connection")
        await ws.close(code=1008)
        return
    finally:
        if stream_handler:
            await stream_handler.stop_recording()

@bp.websocket("/video-generator")
async def video_generator_ws(request, ws):
    """
    WebSocket endpoint for video generation with real-time status updates.
    
    Messages from client:
    1. Authentication:
    {
        "type": "auth",
        "token": "your_auth_token"
    }
    
    2. Start generation:
    {
        "type": "generate",
        "text": "Your educational content description",
        "title": "Optional video title",
        "model": "Optional model name"
    }
    
    3. Cancel generation:
    {
        "type": "cancel",
        "video_uuid": "uuid_of_video_to_cancel"
    }
    
    Messages to client:
    1. Authentication response:
    {
        "type": "auth_response",
        "status": "success" | "error",
        "message": "Optional message"
    }
    
    2. Generation status:
    {
        "type": "status",
        "video_uuid": "uuid",
        "status": "processing" | "completed" | "failed",
        "progress": 0-100,
        "message": "Optional status message",
        "error": "Error message if failed",
        "download_url": "URL if completed"
    }
    """
    session_id = str(uuid.uuid4())[:8]
    user = None
    remote = request.remote_addr or request.ip
    logger.info(f"🎥 New video generator WebSocket connection from {remote} (session: {session_id})")
    
    try:
        # Wait for authentication
        logger.info(f"🔐 Waiting for authentication (session: {session_id})")
        # Authenticate user
        user = await handle_ws_login(request, ws, session_id)
        if not user:
            logger.warning(f"❌ Authentication failed (session: {session_id})")
            await ws.send(json.dumps({
                "type": "auth_response",
                "status": "error",
                "message": "Authentication failed"
            }))
            return
        
        logger.info(f"✅ Video generator WebSocket authenticated for user {user.id} (session: {session_id})")
        await ws.send(json.dumps({
            "type": "auth_response",
            "status": "success",
            "message": "Authentication successful"
        }))
        
        # Main message loop
        while True:
            message = await ws.recv()
            data = json.loads(message)
            logger.debug(f"📨 Received message type: {data.get('type')} (session: {session_id})")
            
            if data.get("type") == "generate":
                # Start new video generation
                if not video_generator:
                    logger.error(f"❌ Video generator not available (session: {session_id})")
                    await ws.send(json.dumps({
                        "type": "status",
                        "status": "failed",
                        "error": "Video generator is not available"
                    }))
                    continue
                
                text = data.get("text", "").strip()
                title = data.get("title", "").strip()
                model = data.get("model", "").strip()
                
                logger.info(f"🎬 Starting video generation (session: {session_id})")
                logger.debug(f"📝 Generation parameters: text_length={len(text)}, title='{title}', model='{model}'")
                
                if not text:
                    logger.warning(f"❌ Empty text content (session: {session_id})")
                    await ws.send(json.dumps({
                        "type": "status",
                        "status": "failed",
                        "error": "Text content cannot be empty"
                    }))
                    continue
                
                if len(text) > 300:
                    logger.warning(f"❌ Content too long: {len(text)} chars (session: {session_id})")
                    await ws.send(json.dumps({
                        "type": "status",
                        "status": "failed",
                        "error": "Content too long, maximum 300 characters allowed"
                    }))
                    continue
                
                # Generate UUID for video
                video_uuid = str(uuid.uuid4())
                logger.info(f"🆔 Generated video UUID: {video_uuid} (session: {session_id})")
                
                # Switch model if specified
                if model:
                    logger.info(f"🔄 Switching to model: {model} (session: {session_id})")
                    video_generator.switch_model(model)
                
                # Create initial info
                info = {
                    "video_uuid": video_uuid,
                    "input_text": text,
                    "title": title or "AI Generated Video",
                    "model_used": "gpt-4",
                    "created_at": datetime.now().isoformat(),
                    "status": "processing",
                    "progress": 0,
                    "user_id": user.id
                }
                
                # Save initial info
                info_path = VIDEO_STORAGE["temp_dir"] / f"{video_uuid}_info.json"
                with open(info_path, 'w', encoding='utf-8') as f:
                    json.dump(info, f, ensure_ascii=False, indent=2)
                logger.info(f"💾 Saved initial video info to {info_path} (session: {session_id})")
                
                async def generate_and_notify():
                    try:
                        # Notify start
                        logger.info(f"🚀 Starting video generation process (video: {video_uuid}, session: {session_id})")
                        await ws.send(json.dumps({
                            "type": "status",
                            "video_uuid": video_uuid,
                            "status": "processing",
                            "progress": 0,
                            "message": "Starting video generation"
                        }))
                        
                        # Run generation
                        logger.info(f"⚙️ Running video generation (video: {video_uuid}, session: {session_id})")
                        loop = asyncio.get_event_loop()
                        result = await loop.run_in_executor(
                            None, 
                            lambda: video_generator.generate_video(text)
                        )
                        
                        if result.get('video_path') and Path(result['video_path']).exists():
                            # Move video to final location
                            source_path = Path(result['video_path'])
                            target_path = VIDEO_STORAGE["base_dir"] / f"{video_uuid}.mp4"
                            logger.info(f"📦 Moving video from {source_path} to {target_path} (video: {video_uuid})")
                            shutil.move(str(source_path), str(target_path))
                            
                            # Update info
                            info.update({
                                "status": "completed",
                                "progress": 100,
                                "completed_at": datetime.now().isoformat(),
                                "file_size": target_path.stat().st_size,
                                "scene_name": result.get('scene_name', 'Unknown')
                            })
                            
                            # Save final info
                            final_info_path = VIDEO_STORAGE["base_dir"] / f"{video_uuid}_info.json"
                            with open(final_info_path, 'w', encoding='utf-8') as f:
                                json.dump(info, f, ensure_ascii=False, indent=2)
                            logger.info(f"✅ Video generation completed successfully (video: {video_uuid}, size: {info['file_size']} bytes)")
                            
                            # Clean up temp files
                            if info_path.exists():
                                info_path.unlink()
                                logger.debug(f"🧹 Cleaned up temp info file: {info_path}")
                            
                            # Notify completion
                            await ws.send(json.dumps({
                                "type": "status",
                                "video_uuid": video_uuid,
                                "status": "completed",
                                "progress": 100,
                                "message": "Video generation completed",
                                "download_url": f"/dean/videos/{video_uuid}/download"
                            }))
                        else:
                            logger.error(f"❌ Video generation failed - no output file (video: {video_uuid})")
                            info.update({
                                "status": "failed",
                                "error": "Video generation failed",
                                "completed_at": datetime.now().isoformat()
                            })
                            with open(info_path, 'w', encoding='utf-8') as f:
                                json.dump(info, f, ensure_ascii=False, indent=2)
                            
                            await ws.send(json.dumps({
                                "type": "status",
                                "video_uuid": video_uuid,
                                "status": "failed",
                                "error": "Video generation failed"
                            }))
                            
                    except Exception as e:
                        logger.error(f"❌ Video generation failed: {str(e)} (video: {video_uuid}, session: {session_id})")
                        log_exception(e, f"Video generation error (video: {video_uuid})")
                        info.update({
                            "status": "failed",
                            "error": str(e),
                            "completed_at": datetime.now().isoformat()
                        })
                        with open(info_path, 'w', encoding='utf-8') as f:
                            json.dump(info, f, ensure_ascii=False, indent=2)
                        
                        await ws.send(json.dumps({
                            "type": "status",
                            "video_uuid": video_uuid,
                            "status": "failed",
                            "error": str(e)
                        }))
                    finally:
                        # Clean up active generation
                        if video_uuid in active_generations:
                            logger.debug(f"🧹 Cleaning up active generation (video: {video_uuid})")
                            del active_generations[video_uuid]
                
                # Start generation task
                task = asyncio.create_task(generate_and_notify())
                active_generations[video_uuid] = {
                    "ws": ws,
                    "info": info,
                    "task": task
                }
                logger.info(f"📋 Added to active generations (video: {video_uuid}, total active: {len(active_generations)})")
                
            elif data.get("type") == "cancel":
                # Cancel video generation
                video_uuid = data.get("video_uuid")
                logger.info(f"🛑 Cancellation requested for video: {video_uuid} (session: {session_id})")
                
                if video_uuid in active_generations:
                    generation = active_generations[video_uuid]
                    if generation["info"]["user_id"] == user.id:  # Verify ownership
                        logger.info(f"✅ Cancelling video generation (video: {video_uuid})")
                        generation["task"].cancel()
                        del active_generations[video_uuid]
                        
                        # Update info
                        info_path = VIDEO_STORAGE["temp_dir"] / f"{video_uuid}_info.json"
                        if info_path.exists():
                            with open(info_path, 'r', encoding='utf-8') as f:
                                info = json.load(f)
                            info.update({
                                "status": "cancelled",
                                "completed_at": datetime.now().isoformat()
                            })
                            with open(info_path, 'w', encoding='utf-8') as f:
                                json.dump(info, f, ensure_ascii=False, indent=2)
                            logger.info(f"💾 Updated video info for cancelled generation (video: {video_uuid})")
                        
                        await ws.send(json.dumps({
                            "type": "status",
                            "video_uuid": video_uuid,
                            "status": "cancelled",
                            "message": "Video generation cancelled"
                        }))
                    else:
                        logger.warning(f"❌ Unauthorized cancellation attempt (video: {video_uuid}, user: {user.id})")
                        await ws.send(json.dumps({
                            "type": "status",
                            "video_uuid": video_uuid,
                            "status": "error",
                            "error": "Not authorized to cancel this video"
                        }))
                else:
                    logger.warning(f"❌ Video generation not found for cancellation (video: {video_uuid})")
                    await ws.send(json.dumps({
                        "type": "status",
                        "video_uuid": video_uuid,
                        "status": "error",
                        "error": "Video generation not found"
                    }))
            
            else:
                logger.warning(f"❌ Unknown message type: {data.get('type')} (session: {session_id})")
                await ws.send(json.dumps({
                    "type": "error",
                    "error": "Unknown message type"
                }))
                
    except WebsocketClosed:
        logger.info(f"🔌 Video generator WebSocket closed (session: {session_id})")
        # Clean up any active generations for this user
        for video_uuid, generation in list(active_generations.items()):
            if generation["info"]["user_id"] == user.id:
                logger.info(f"🧹 Cleaning up active generation on disconnect (video: {video_uuid})")
                generation["task"].cancel()
                del active_generations[video_uuid]
        return
    except Exception as e:
        logger.error(f"❌ Error in video generator WebSocket: {str(e)} (session: {session_id})")
        log_exception(e, "Video generator WebSocket error")
        try:
            await ws.send(json.dumps({
                "type": "error",
                "error": "Internal server error"
            }))
        except:
            pass
        await ws.close(code=1008)
        return

@bp.get("/videos/<video_uuid>")
async def get_video_status(request, video_uuid: str):
    """
    Get the status and information about a video.
    
    Response:
    {
        "video_uuid": str,
        "status": str,  # "processing", "completed", "failed"
        "progress": int,  # 0-100
        "title": str,
        "created_at": str,
        "completed_at": str (if completed),
        "error": str (if failed),
        "download_url": str (if completed)
    }
    """
    try:
        info = get_video_info(video_uuid)
        if not info:
            return response.json({
                "error": "Video not found"
            }, status=404)
        
        response_data = {
            "video_uuid": video_uuid,
            "status": info.get("status", "unknown"),
            "progress": info.get("progress", 0),
            "title": info.get("title", "AI Generated Video"),
            "created_at": info.get("created_at"),
            "model_used": info.get("model_used", "unknown")
        }
        
        if info.get("status") == "completed":
            response_data.update({
                "completed_at": info.get("completed_at"),
                "file_size": info.get("file_size"),
                "download_url": f"/dean/videos/{video_uuid}/download"
            })
        elif info.get("status") == "failed":
            response_data.update({
                "completed_at": info.get("completed_at"),
                "error": info.get("error", "Unknown error")
            })
        
        return response.json(response_data)
        
    except Exception as e:
        log_exception(e, "Error getting video status")
        return response.json({
            "error": "Internal server error"
        }, status=500)

@bp.get("/videos/<video_uuid>/download")
async def download_video(request, video_uuid: str):
    """Download a generated video"""
    try:
        video_path = get_video_path(video_uuid)
        if not video_path or not video_path.exists():
            return response.json({
                "error": "Video not found or not ready for download"
            }, status=404)
        
        info = get_video_info(video_uuid)
        if not info or info.get("status") != "completed":
            return response.json({
                "error": "Video is not ready for download"
            }, status=400)
        
        # Get video name from info
        title = info.get('title', 'AI Generated Video')
        clean_title = "".join(c for c in title if c.isalnum() or c in " _-")[:20]
        video_name = f"{clean_title}_{video_uuid}.mp4"
        
        return await response.file(
            video_path,
            filename=video_name,
            mime_type='video/mp4'
        )
        
    except Exception as e:
        log_exception(e, "Error downloading video")
        return response.json({
            "error": f"Download failed: {str(e)}"
        }, status=500)
