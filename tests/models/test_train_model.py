"""
Test cases for train_model.py
"""
from unittest.mock import patch
from spreadsheetz.models.train_model import main


def test_main(self):
    with patch('spreadsheetz.models.train_model.logger.info') as mock_logger_info:
        main()
        mock_logger_info.assert_any_call("Training model...")
        mock_logger_info.assert_any_call("Model trained successfully.")
