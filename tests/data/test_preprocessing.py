"""Tests for data preprocessing module."""
import pytest
from src.data.preprocessing import DataPreprocessor
import pandas as pd

def test_data_preprocessor_initialization():
    """Test DataPreprocessor initialization."""
    preprocessor = DataPreprocessor()
    assert preprocessor.data is None

def test_clean_data_without_loading():
    """Test clean_data raises error when data not loaded."""
    preprocessor = DataPreprocessor()
    with pytest.raises(ValueError):
        preprocessor.clean_data() 