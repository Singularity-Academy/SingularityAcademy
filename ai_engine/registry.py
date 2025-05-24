"""
Registry module for AI Engine.

This module handles registration of various components including database models,
applications, and their configurations.
"""

import os
import importlib
import pkgutil
from typing import List, Dict, Any, Set, Optional
from pathlib import Path
from loguru import logger
from sanic import Blueprint, Sanic
from tortoise.contrib.sanic import register_tortoise
from .config import load_db_config, construct_db_url
from ai_engine.logging import log_exception

def get_modules() -> Dict[str, List[str]]:
    """
    Discover and return all modules under the apps/ directory.
    
    This function:
    1. Scans the apps/ directory for Python packages
    2. Finds all .py files in each package (both modules and subpackages)
    3. Returns a dictionary mapping package names to their module lists
    
    Returns:
        Dict[str, List[str]]: A dictionary where:
            - Keys are package names (e.g., "principal")
            - Values are lists of fully qualified module names (e.g., ["apps.principal.models"])
            
    Example:
        {
            "principal": [
                "apps.principal.models",
                "apps.principal.routes",
                "apps.principal.services"
            ]
        }
    """
    apps_dir = Path(__file__).parent / "apps"
    if not apps_dir.exists():
        logger.warning(f"Apps directory not found at {apps_dir}")
        return {}
        
    modules: Dict[str, List[str]] = {}
    
    try:
        # Import the apps package
        apps_package = importlib.import_module("ai_engine.apps")
        
        # Walk through all packages in apps/
        for _, package_name, is_pkg in pkgutil.iter_modules([str(apps_dir)]):
            if not is_pkg:
                continue
                
            # Skip __pycache__ and other special directories
            if package_name.startswith('_'):
                continue
                
            # Get the full package path
            package_path = apps_dir / package_name
            
            # Initialize the package's module list
            modules[package_name] = []
            
            # Find all .py files in the package directory
            for py_file in package_path.glob("*.py"):
                # Skip __init__.py and other special files
                if py_file.stem.startswith('_'):
                    continue
                    
                # Add the fully qualified module name
                full_module_name = f"ai_engine.apps.{package_name}.{py_file.stem}"
                modules[package_name].append(full_module_name)
                
        logger.info(f"Discovered {len(modules)} modules")
        return modules
        
    except Exception as e:
        log_exception(e, "Error discovering modules")
        raise

_MODULES = get_modules()

def register_modules(app: Sanic, url_prefix: str = "/ai") -> None:
    """
    Register all module blueprints to the Sanic app.
    
    This function:
    1. Finds all modules ending with 'routes'
    2. Imports the 'bp' blueprint from each routes module
    3. Creates a Blueprint group with the specified URL prefix
    4. Registers all route blueprints to the group
    5. Registers the group to the Sanic app
    
    Args:
        app (Sanic): The Sanic application instance
        url_prefix (str): The URL prefix for all routes (default: "/ai")
        
    Raises:
        ImportError: If a routes module doesn't have a 'bp' blueprint
        ValueError: If no route modules are found
    """
    try:
        # Find all route modules using list comprehension
        route_modules = [
            module_name 
            for modules in _MODULES.values() 
            for module_name in modules 
            if module_name.endswith('.routes')
        ]
        
        if not route_modules:
            logger.warning("No route modules found to register")
            return
            
        # Import and collect blueprints
        route_blueprints = []
        for module_name in route_modules:
            try:
                module = importlib.import_module(module_name)
                if not hasattr(module, 'bp'):
                    logger.error(f"Module {module_name} has no 'bp' blueprint")
                    continue
                    
                bp = getattr(module, 'bp')
                if not isinstance(bp, Blueprint):
                    continue
                    
                # Add package name as prefix to blueprint name for uniqueness
                package_name = module_name.split('.')[-2]  # Get package name from module path
                bp.name = f"{package_name}.{bp.name}"
                route_blueprints.append(bp)
                
            except ImportError as e:
                logger.error(f"Failed to import module {module_name}: {e}")
                raise
                continue
                
        if not route_blueprints:
            logger.warning("No valid blueprints found to register")
            return
            
        # Create a blueprint group with the URL prefix
        app_bp = Blueprint.group(*route_blueprints, url_prefix=url_prefix)
        
        # Register the group to the app
        app.blueprint(app_bp)
        logger.info(f"Registered {len(route_blueprints)} blueprints under {url_prefix}: {', '.join([bp.name for bp in route_blueprints])}")
        
    except Exception as e:
        log_exception(e, "Error registering modules")
        raise

def init_db(app: Sanic) -> None:
    """
    Initialize database connection and register Tortoise ORM with Sanic.
    
    This function:
    1. Loads database configuration
    2. Constructs database URL
    3. Discovers all model modules
    4. Registers Tortoise ORM with the app
    
    Args:
        app (Sanic): The Sanic application instance
        
    Raises:
        ValueError: If database configuration is invalid
        ImportError: If model modules cannot be imported
    """
    try:
        # Load and validate database configuration
        db_config = load_db_config()
        db_url = construct_db_url(db_config)
        
        # Find all model modules using list comprehension
        model_modules = [
            module_name 
            for modules in _MODULES.values() 
            for module_name in modules 
            if module_name.endswith('.models')
        ]
        
        if not model_modules:
            logger.warning("No model modules found")
            raise ValueError("No model modules found")
            
        # Register Tortoise ORM
        register_tortoise(
            app,
            db_url=db_url,
            modules={"models": model_modules},
            generate_schemas=True,  # Auto-generate schemas
        )
        
        logger.info(f"Database initialized with URL: {db_url}")
        logger.info(f"Registered model modules: {model_modules}")
        
    except Exception as e:
        log_exception(e, "Failed to initialize database")
        raise

