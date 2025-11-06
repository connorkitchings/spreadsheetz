"""
Test cases for evaluate_model.py
"""
from unittest.mock import patch
from spreadsheetz.models.evaluate_model import main


def test_main(self):
    with patch('spreadsheetz.models.evaluate_model.logger.info') as mock_logger_info:
        main()
        mock_logger_info.assert_any_call("Evaluating model...")
        mock_logger_info.assert_any_call("Model evaluated successfully.")
