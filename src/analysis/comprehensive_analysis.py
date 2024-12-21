"""Comprehensive analysis module combining all analysis features."""
import pandas as pd
import numpy as np
from scipy import stats
from .handset_analysis import HandsetAnalyzer
from .user_behavior import UserBehaviorAnalyzer

class ComprehensiveAnalyzer:
    """Class for comprehensive analysis combining all features."""
    
    def __init__(self, data):
        self.data = data
        self.handset_analyzer = HandsetAnalyzer(data)
        self.behavior_analyzer = UserBehaviorAnalyzer(data)
    
    def get_basic_statistics(self):
        """Calculate basic statistics for all numeric columns."""
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        stats_df = pd.DataFrame({
            'mean': self.data[numeric_cols].mean(),
            'median': self.data[numeric_cols].median(),
            'std': self.data[numeric_cols].std(),
            'skew': self.data[numeric_cols].skew(),
            'kurtosis': self.data[numeric_cols].kurtosis()
        })
        return stats_df
    
    def identify_outliers(self, column, method='zscore', threshold=3):
        """Identify outliers in specified column."""
        if method == 'zscore':
            z_scores = np.abs(stats.zscore(self.data[column]))
            outliers = self.data[z_scores > threshold]
        elif method == 'iqr':
            Q1 = self.data[column].quantile(0.25)
            Q3 = self.data[column].quantile(0.75)
            IQR = Q3 - Q1
            outliers = self.data[(self.data[column] < (Q1 - 1.5 * IQR)) | 
                                (self.data[column] > (Q3 + 1.5 * IQR))]
        return outliers
    
    def perform_full_analysis(self):
        """Perform complete analysis and return all results."""
        results = {
            'basic_stats': self.get_basic_statistics(),
            'top_handsets': self.handset_analyzer.get_top_handsets(),
            'top_manufacturers': self.handset_analyzer.get_top_manufacturers(),
            'user_metrics': self.behavior_analyzer.aggregate_user_metrics(),
            'correlation_matrix': self.behavior_analyzer.compute_correlation_matrix(self.data),
            'pca_results': self.behavior_analyzer.perform_pca(self.data)
        }
        return results 