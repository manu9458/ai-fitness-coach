import logging
import os
from logging.handlers import RotatingFileHandler

# Create log directory
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "app.log")

# RotatingFileHandler: max 5 MB per file, keep 3 backups
rotating_handler = RotatingFileHandler(
    LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    handlers=[
        rotating_handler,
        logging.StreamHandler()  # Optional: show logs in console
    ]
)

logger = logging.getLogger("health_coach_logger")

# Test log to confirm
logger.info("🟢 Logging initialized with rotation!")
