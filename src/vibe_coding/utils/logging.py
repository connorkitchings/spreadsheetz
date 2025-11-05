"""
Logging configuration.
"""
import logging
from vibe_coding.core.config import settings

# Create a logger
logger = logging.getLogger(settings.PROJECT_NAME)

# Set the logging level
logger.setLevel(logging.INFO)

# Create a console handler
handler = logging.StreamHandler()

# Create a formatter and add it to the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)
