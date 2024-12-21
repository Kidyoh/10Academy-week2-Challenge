"""Tests for Task 1 analysis modules."""
import pytest
import pandas as pd
import numpy as np
from src.analysis.handset_analysis import HandsetAnalyzer
from src.analysis.user_behavior import UserBehaviorAnalyzer

@pytest.fixture
def sample_handset_data():
    """Create sample handset data."""
    return pd.DataFrame({
        'handset': ['Model1', 'Model2', 'Model1', 'Model3'] * 25,
        'manufacturer': ['Brand1', 'Brand2', 'Brand1', 'Brand3'] * 25
    })

@pytest.fixture
def sample_user_data():
    """Create sample user behavior data."""
    return pd.DataFrame({
        'user_id': range(100),
        'session_id': range(100),
        'session_duration': np.random.uniform(0, 3600, 100),
        'download_data': np.random.uniform(0, 1000, 100),
        'upload_data': np.random.uniform(0, 1000, 100),
        'Social_Media': np.random.uniform(0, 100, 100),
        'Google': np.random.uniform(0, 100, 100),
        'Email': np.random.uniform(0, 100, 100),
        'YouTube': np.random.uniform(0, 100, 100),
        'Netflix': np.random.uniform(0, 100, 100),
        'Gaming': np.random.uniform(0, 100, 100),
        'Other': np.random.uniform(0, 100, 100)
    })

def test_handset_analyzer(sample_handset_data):
    """Test HandsetAnalyzer functionality."""
    analyzer = HandsetAnalyzer(sample_handset_data)
    
    top_handsets = analyzer.get_top_handsets(n=2)
    assert len(top_handsets) == 2
    assert 'Model1' in top_handsets['handset'].values
    
    top_manufacturers = analyzer.get_top_manufacturers(n=2)
    assert len(top_manufacturers) == 2
    assert 'Brand1' in top_manufacturers['manufacturer'].values

def test_user_behavior_analyzer(sample_user_data):
    """Test UserBehaviorAnalyzer functionality."""
    analyzer = UserBehaviorAnalyzer(sample_user_data)
    
    aggregated_data = analyzer.aggregate_user_metrics()
    assert len(aggregated_data) == len(sample_user_data['user_id'].unique())
    
    correlation_matrix = analyzer.compute_correlation_matrix(sample_user_data)
    assert correlation_matrix.shape == (7, 7)  # 7 application columns
    
    pca_results = analyzer.perform_pca(sample_user_data)
    assert len(pca_results['explained_variance']) == 7 