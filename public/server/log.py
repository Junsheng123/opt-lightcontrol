from loguru import logger
import sys

logger.add(sys.stderr, format="{time} - {level} - {message}")
logger.add(r"systemlog/{time:YYYY-MM-DD}/file_{time:YYYY-MM-DD}.log", rotation="10 MB")
logger.propagate = False