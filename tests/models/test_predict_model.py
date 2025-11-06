"""
Test cases for predict_model.py
"""
from unittest.mock import patch
from spreadsheetz.models.predict_model import main


def test_main(self):
    with patch('spreadsheetz.models.predict_model.logger.info') as mock_logger_info:
        main()
        mock_logger_info.assert_any_call("Making predictions...")
        mock_logger_info.assert_any_call("Predictions made successfully.")
