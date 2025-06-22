from loguru import logger
import os
import sys


os.makedirs("logs", exist_ok=True)
logger.remove()

logger.add(sys.stdout, level="INFO")

logger.add(
    "logs/site_log.log",
    rotation="5 MB",
    retention="7 days",
    compression="zip",
    format="""{time: DD-MM-YYYY at HH:mm}
        | {level}
        | {message}""",
    level="DEBUG",
)
