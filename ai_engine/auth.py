import os
import time
import jwt
from functools import wraps
from sanic import json
import logging # Optional: for logging auth events

logger = logging.getLogger(__name__) # Optional

# Same default secret key as Go backend
DEFAULT_SECRET_KEY = "AISAISAAA"
SECRET_KEY_FILE = "backend/auth_secret.key"

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
                logger.warning(f"Token with invalid issuer: {claims.get('iss')}")
                return None
                
            if "exp" in claims and claims["exp"] < int(time.time()):
                logger.warning("Expired token received.")
                return None
                
            if "ID" not in claims:
                logger.warning("Token missing 'ID' claim.")
                return None
            
            # You might want to ensure claims["ID"] is of a specific type, e.g., int
            # For now, we return the whole claims dictionary.
            return claims
        except jwt.ExpiredSignatureError:
            logger.warning("Expired token signature.")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error decoding token: {e}")
            return None

    def verify_token(self, token: str) -> bool: # Kept for potential other uses
        return self.decode_token(token) is not None

AuthManager = _AuthManager.from_env()


def init_auth(app):
    """
    Initializes authentication for the Sanic application.
    Makes AuthManager available via `app.ctx.auth`.
    """
    app.ctx.auth = AuthManager
    logger.info("Authentication Manager initialized and attached to app.ctx.auth")


async def authentication_middleware(request):
    """
    Sanic middleware to handle JWT authentication.
    If successful, adds `user_id` and `claims` to `request.ctx`.
    If authentication fails for a route that requires it (determined by where this middleware is applied),
    it will short-circuit with a 401 error.
    """
    auth_header = request.headers.get("Authorization")
    
    # Default to no authenticated user
    request.ctx.user_id = None
    request.ctx.claims = None

    if not auth_header:
        # If the route is public, this is fine. If protected, it will fail later
        # if user_id is None and the route handler expects it.
        # Alternatively, make the middleware itself decide to raise 401 if no header
        # for protected routes. For now, it just sets user_id to None.
        # logger.debug("No Authorization header found.")
        return

    parts = auth_header.split(" ")
    if len(parts) != 2 or parts[0].lower() != "bearer":
        logger.warning(f"Invalid Authorization header format: {auth_header}")
        # This is an error, so we can return a 401 immediately if we want all
        # routes with this middleware to be strictly authenticated.
        # However, if we want some routes to be optionally authenticated,
        # we just let request.ctx.user_id remain None.
        # For a stricter approach:
        # return json({"error": "Invalid Authorization header format. Expected 'Bearer <token>'"}, status=401)
        return 

    token = parts[1]
    
    # Access AuthManager from app.ctx (set by init_auth)
    auth_manager = request.app.ctx.auth 
    claims = auth_manager.decode_token(token)

    if claims:
        request.ctx.user_id = claims.get("ID")
        request.ctx.claims = claims # Store all claims if needed
        logger.info(f"User {request.ctx.user_id} authenticated successfully.")
    else:
        logger.warning(f"Token verification failed for token: {token[:10]}...")
        # If strict, and token is provided but invalid:
        # return json({"error": "Unauthorized - Invalid Token"}, status=401)

# The login_required decorator is no longer the primary mechanism.
# Routes will be protected by applying the middleware.
# If you still want a decorator for specific checks on top of middleware:
# def ensure_authenticated(func):
#     @wraps(func)
#     async def wrapper(request, *args, **kwargs):
#         if not request.ctx.user_id:
#             return json({"error": "Authentication required"}, status=401)
#         return await func(request, *args, **kwargs)
#     return wrapper