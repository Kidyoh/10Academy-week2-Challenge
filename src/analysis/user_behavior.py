"""User behavior analysis module."""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

class UserBehaviorAnalyzer:
    """Class for analyzing user behavior."""
    
    def __init__(self, data):
        """Initialize with data and define metrics."""
        self.data = data
        
        # Basic metrics
        self.basic_metrics = {
            'Bearer Id': 'count',
            'Dur. (ms)': 'sum',
            'Avg Bearer TP DL (kbps)': 'mean',
            'Avg Bearer TP UL (kbps)': 'mean',
            'TCP DL Retrans. Vol (Bytes)': 'sum',
            'TCP UL Retrans. Vol (Bytes)': 'sum'
        }
        
        # Performance metrics
        self.perf_metrics = [
            'DL TP < 50 Kbps (%)',
            '50 Kbps < DL TP < 250 Kbps (%)',
            '250 Kbps < DL TP < 1 Mbps (%)',
            'DL TP > 1 Mbps (%)',
            'UL TP < 10 Kbps (%)',
            '10 Kbps < UL TP < 50 Kbps (%)',
            '50 Kbps < UL TP < 300 Kbps (%)',
            'UL TP > 300 Kbps (%)'
        ]
    
    def aggregate_user_metrics(self):
        """Aggregate metrics per user."""
        try:
            # Create aggregation dictionary
            agg_dict = {
                **self.basic_metrics,
                **{metric: 'mean' for metric in self.perf_metrics}
            }
            
            # Group by MSISDN/Number and aggregate metrics
            metrics = self.data.groupby('MSISDN/Number').agg(agg_dict).reset_index()
            
            # Rename columns for consistency
            metrics = metrics.rename(columns={
                'MSISDN/Number': 'msisdn',
                'Bearer Id': 'total_sessions',
                'Dur. (ms)': 'session_duration',
                'Avg Bearer TP DL (kbps)': 'avg_throughput_dl',
                'Avg Bearer TP UL (kbps)': 'avg_throughput_ul',
                'TCP DL Retrans. Vol (Bytes)': 'tcp_retrans_dl',
                'TCP UL Retrans. Vol (Bytes)': 'tcp_retrans_ul'
            })
            
            # Calculate derived metrics
            metrics['total_throughput'] = metrics['avg_throughput_dl'] + metrics['avg_throughput_ul']
            metrics['total_retrans'] = metrics['tcp_retrans_dl'] + metrics['tcp_retrans_ul']
            
            return metrics
            
        except Exception as e:
            print(f"Error in aggregate_user_metrics: {str(e)}")
            print("Available columns:", self.data.columns.tolist())
            raise
    
    def create_duration_deciles(self, user_data):
        """Segment users into deciles based on session duration."""
        user_data['duration_decile'] = pd.qcut(
            user_data['session_duration'], 
            q=10, 
            labels=False
        ) + 1
        return user_data
    
    def compute_correlation_matrix(self, user_data):
        """Compute correlation matrix for performance metrics."""
        perf_cols = [col for col in user_data.columns if 'TP' in col]
        return user_data[perf_cols].corr()
    
    def perform_pca(self, user_data):
        """Perform PCA on performance metrics."""
        # Get performance metrics columns
        perf_cols = [col for col in user_data.columns if 'TP' in col]
        
        # Prepare data for PCA
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(user_data[perf_cols])
        
        # Perform PCA
        pca = PCA()
        pca_result = pca.fit_transform(scaled_data)
        
        # Calculate explained variance ratio
        explained_variance = pca.explained_variance_ratio_
        
        return {
            'pca_result': pca_result,
            'explained_variance': explained_variance,
            'components': pca.components_,
            'feature_names': perf_cols
        } 