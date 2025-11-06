"""
Test cases for make_dataset.py
"""
from unittest.mock import patch
from spreadsheetz.data.make_dataset import main


def test_main(self):
    with patch('spreadsheetz.data.make_dataset.logger.info') as mock_logger_info:
        main()
        mock_logger_info.assert_any_call("Generating dataset...")
        mock_logger_info.assert_any_call("Dataset generated successfully.")
