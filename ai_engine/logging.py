import logging
import logging.handlers
import os
from datetime import datetime
from pathlib import Path

def setup_logging(
    log_level: str = "INFO",
    log_dir: str = "logs",
    app_name: str = "ai_online_school",
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5,
) -> logging.Logger:
    """
    Set up application logging with both file and console handlers.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: Directory to store log files
        app_name: Name of the application (used in log file names)
        max_bytes: Maximum size of each log file before rotation
        backup_count: Number of backup files to keep
    
    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logs directory if it doesn't exist
    log_dir_path = Path(log_dir)
    log_dir_path.mkdir(parents=True, exist_ok=True)
    
    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Remove any existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        fmt='%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_formatter = logging.Formatter(
        fmt='%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # Set up rotating file handler for all logs
    main_log_file = log_dir_path / f"{app_name}.log"
    file_handler = logging.handlers.RotatingFileHandler(
        filename=main_log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    file_handler.setFormatter(detailed_formatter)
    logger.addHandler(file_handler)
    
    # Set up rotating file handler for errors
    error_log_file = log_dir_path / f"{app_name}_error.log"
    error_file_handler = logging.handlers.RotatingFileHandler(
        filename=error_log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(detailed_formatter)
    logger.addHandler(error_file_handler)
    
    # Set up console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # Log initial message
    logger.info(f"Logging initialized at level {log_level}")
    
    return logger

# Example usage
if __name__ == "__main__":
    logger = setup_logging(log_level="DEBUG")
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
