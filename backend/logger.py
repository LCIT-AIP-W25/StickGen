import logging
import os
import sys

# Create logs directory if not exist
if not os.path.exists("logs"):
    os.makedirs("logs")

# Force UTF-8 for console on Windows
if os.name == 'nt':
    sys.stdout.reconfigure(encoding='utf-8')

# Configure Logger
logger = logging.getLogger("backend_logger")
logger.setLevel(logging.DEBUG)

# File handler
file_handler = logging.FileHandler("logs/backend.log", encoding='utf-8')  # ensure utf-8 for file too
file_handler.setLevel(logging.DEBUG)

# Console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers (prevent duplicate handlers)
if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
