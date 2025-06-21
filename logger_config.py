from loguru import logger
import os
import sys
import pytz
import datetime

os.makedirs("logs", exist_ok=True)


def custom_time(record):
    tz = pytz.timezone("Europe/Kiev")
    dt = datetime.datetime.fromtimestamp(record["time"].timestamp(), tz)
    return dt.strftime("%d-%m-%Y at %H:%M")


logger.remove()
kiev_time = pytz.timezone("Europe/Kiev")
logger.add(sys.stdout, level="DEBUG")
logger.add(
    "logs/site_log.log",
    rotation="5 MB",
    retention="7 days",
    compression="zip",
    format="{time: DD-MM-YYYY at HH:mm} | {level} | {message}",
    level="DEBUG",
)
