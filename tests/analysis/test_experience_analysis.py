"""Tests for experience analysis module."""
import pytest
import pandas as pd
import numpy as np
from src.analysis.experience_analyzer import ExperienceAnalyzer

@pytest.fixture
def sample_experience_data():
    """Create sample data for testing."""
    return pd.DataFrame({
        'MSISDN/Number': range(100),
        'TCP DL Retrans. Vol (Bytes)': np.random.uniform(0, 1000, 100),
        'TCP UL Retrans. Vol (Bytes)': np.random.uniform(0, 1000, 100),
        'Avg Bearer TP DL (kbps)': np.random.uniform(0, 100, 100),
        'Avg Bearer TP UL (kbps)': np.random.uniform(0, 100, 100)
    })

def test_tcp_retransmission_analysis(sample_experience_data):
    analyzer = ExperienceAnalyzer(sample_experience_data)
    results = analyzer.analyze_tcp_retransmission()
    assert isinstance(results, pd.DataFrame)
    assert not results.empty 