"""Tests for analysis modules."""
import pytest
import pandas as pd
import numpy as np
from src.analysis.user_overview import UserOverviewAnalyzer
from src.analysis.engagement import EngagementAnalyzer
from src.analysis.experience import ExperienceAnalyzer

@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    return pd.DataFrame({
        'user_id': range(1, 101),
        'total_data': np.random.uniform(0, 1000, 100),
        'session_duration': np.random.uniform(0, 3600, 100),
        'tcp_retransmission': np.random.uniform(0, 1, 100),
        'throughput': np.random.uniform(0, 100, 100),
        'latency': np.random.uniform(0, 1000, 100),
        'packet_loss': np.random.uniform(0, 1, 100)
    })

def test_user_overview_analyzer(sample_data):
    """Test UserOverviewAnalyzer functionality."""
    analyzer = UserOverviewAnalyzer(sample_data)
    stats = analyzer.get_user_statistics()
    
    assert isinstance(stats, dict)
    assert 'total_users' in stats
    assert 'active_users' in stats
    assert stats['total_users'] == 100

def test_experience_analyzer(sample_data):
    """Test ExperienceAnalyzer functionality."""
    analyzer = ExperienceAnalyzer(sample_data)
    metrics = analyzer.calculate_experience_metrics()
    
    assert isinstance(metrics, pd.DataFrame)
    assert 'experience_score' in metrics.columns
    assert len(metrics) == len(sample_data['user_id'].unique()) 