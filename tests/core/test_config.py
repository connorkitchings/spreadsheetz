"""
Test cases for the core configuration.
"""
from spreadsheetz.core.config import settings

def test_project_name():
    assert settings.PROJECT_NAME == "Vibe Coding Data Science Template"
