"""
Test cases for the logging utility.
"""
from spreadsheetz.utils.logging import logger

def test_logger_name():
    assert logger.name == "Vibe Coding Data Science Template"

def test_logger_level():
    assert logger.level == 20 # INFO level
