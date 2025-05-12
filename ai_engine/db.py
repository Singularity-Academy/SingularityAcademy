from tortoise import fields, models
from tortoise.contrib.sanic import register_tortoise
import yaml
from datetime import datetime
import os

class User(models.Model):
    id = fields.BigIntField(pk=True)  # Using BigInt for uint64
    username = fields.CharField(max_length=255, null=False)
    email = fields.CharField(max_length=255, unique=True, null=False)
    password = fields.CharField(max_length=255, null=False)
    is_verified = fields.BooleanField(default=False)
    verification_token = fields.CharField(max_length=10, null=True)
    register_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "users"

def load_db_config():
    """Load database configuration from config.yml"""
    # Get the project root directory (where run.py is located)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(project_root, "backend", "config", "config.yml")
    
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
        return config["database"]

def init_db(app):
    """Initialize database connection for Sanic app"""
    db_config = load_db_config()
    
    # Construct database URL
    db_url = f"mysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['name']}"
    
    # Register Tortoise ORM with Sanic
    register_tortoise(
        app,
        db_url=db_url,
        modules={"models": ["ai_engine.db"]},
        generate_schemas=True,  # Auto-generate schemas
    )
