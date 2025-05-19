"""
Main application module for AI Engine.
"""

from sanic import Sanic
from .logging import logger
from .config import load_app_config
from .registry import register_modules
from .registry import init_db
from .apps.auth import init_auth

logger.info("Creating AI Engine application")

app = Sanic("ai_engine_rewrite")

# Load app config
load_app_config(app)

# Register modules
register_modules(app)

# Register DB
init_db(app)

# Register auth
init_auth(app)


