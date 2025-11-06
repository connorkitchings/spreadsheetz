"""
Test cases for prediction_pipeline.py
"""
from unittest.mock import patch
from spreadsheetz.pipelines.prediction_pipeline import main


def test_main(self):
    with patch('spreadsheetz.pipelines.prediction_pipeline.logger.info') as mock_logger_info:
        main()
        mock_logger_info.assert_any_call("Running prediction pipeline...")
        mock_logger_info.assert_any_call("Prediction pipeline completed successfully.")
