"""
Authentication module for AI Engine.
"""

import os
import time
import jwt
from functools import wraps
from sanic import json
from loguru import logger
from typing import Optional, Dict, Any
from sanic import Sanic, Request

# Same default secret key as Go backend
DEFAULT_SECRET_KEY = "AISAISAAA"
SECRET_KEY_FILE = "backend/auth_secret.key"

class AuthError(Exception):
    """Base exception for authentication errors."""
    pass

class _AuthManager():
    def __init__(self, secret_key: str):
        self.secret_key = secret_key

    @classmethod
    def from_env(cls):
        secret_key = None
        try:
            if os.path.exists(SECRET_KEY_FILE):
                with open(SECRET_KEY_FILE, 'rb') as f:
                    secret_key = f.read().decode('utf-8').strip() # Ensure it's a string
                logger.info(f"Secret key loaded from {SECRET_KEY_FILE}")
        except Exception as e:
            logger.error(f"Error reading secret key file: {e}")
        
        if not secret_key:
            secret_key = os.getenv("AUTH_SECRET_KEY")
            if secret_key:
                logger.info("Secret key loaded from AUTH_SECRET_KEY environment variable.")
            
        if not secret_key:
            logger.warning("Could not load secret key from file or environment, using default key.")
            secret_key = DEFAULT_SECRET_KEY
            
        return cls(secret_key)

    def decode_token(self, token_string: str) -> dict | None:
        """
        Decodes the JWT token and returns claims if valid, otherwise None.
        Validates issuer, expiry, and presence of 'ID' claim.
        """
        try:
            claims = jwt.decode(token_string, self.secret_key, algorithms=["HS256"])
            
            if claims.get("iss") != "aiLearn":
                logger.warning(f"Token validation failed: Invalid issuer '{claims.get('iss')}', expected 'aiLearn'")
                return None
                
            if "exp" in claims and claims["exp"] < int(time.time()):
                logger.warning(f"Token validation failed: Expired at {time.ctime(claims['exp'])}, current time {time.ctime()}")
                return None
                
            if "ID" not in claims:
                logger.warning("Token validation failed: Missing required 'ID' claim")
                return None
            
            return claims
        except jwt.ExpiredSignatureError:
            logger.warning("Token validation failed: Signature has expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Token validation failed: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during token validation: {str(e)}")
            return None

AuthManager = _AuthManager.from_env()

def init_auth(app):
    """
    Initializes authentication for the Sanic application.
    Makes AuthManager available via `app.ctx.auth` and registers global auth middleware.
    """
    app.ctx.auth = AuthManager
    # Register authentication middleware globally
    app.middleware("request")(authentication_middleware)
    logger.info("Authentication Manager initialized and attached to app.ctx.auth")
    logger.info("Global authentication middleware registered")

async def authentication_middleware(request):
    """
    Sanic middleware to extract and store the raw auth token.
    This middleware only extracts the token and stores it in request.ctx.raw_token.
    Actual token verification is done by the login_required decorator when needed.
    """
    auth_header = request.headers.get("Authorization")
    
    # Initialize raw_auth_token as None
    request.ctx.raw_auth_token = None

    if not auth_header:
        return

    parts = auth_header.split(" ")
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return

    # Store the raw token for later verification
    request.ctx.raw_auth_token = parts[1]

def login_required(func):
    """
    Decorator to verify authentication token and set user context.
    This is where actual token verification happens, only when the decorator is used.
    """
    @wraps(func)
    async def wrapper(request, *args, **kwargs):
        if not request.ctx.raw_auth_token:
            return json({"error": "Authentication required", "error_code": "AUTH_REQUIRED"}, status=401)
        
        # Get auth manager from app context
        auth_manager = request.app.ctx.auth
        
        # Verify the token
        claims = auth_manager.decode_token(request.ctx.raw_auth_token)
        if not claims:
            return json({"error": "Invalid or expired token", "error_code": "INVALID_TOKEN"}, status=401)
        
        # Set user context
        request.ctx.user_id = claims.get("ID")
        request.ctx.claims = claims
        
        logger.info(f"Authorized: User {request.ctx.user_id}")
        return await func(request, *args, **kwargs)
    
    return wrapper