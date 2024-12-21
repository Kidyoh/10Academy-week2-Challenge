"""User behavior analysis module."""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

class UserBehaviorAnalyzer:
    """Class for analyzing user behavior."""
    
    def __init__(self, data):
        self.data = data
        self.app_columns = ['Social_Media', 'Google', 'Email', 'YouTube', 
                           'Netflix', 'Gaming', 'Other']
    
    def aggregate_user_metrics(self):
        """Aggregate metrics per user."""
        return self.data.groupby('user_id').agg({
            'session_id': 'count',
            'session_duration': 'sum',
            'download_data': 'sum',
            'upload_data': 'sum',
            **{app: 'sum' for app in self.app_columns}
        }).reset_index().rename(columns={
            'session_id': 'total_sessions',
            'download_data': 'total_dl',
            'upload_data': 'total_ul'
        })
    
    def create_duration_deciles(self, user_data):
        """Segment users into deciles based on session duration."""
        user_data['duration_decile'] = pd.qcut(user_data['session_duration'], 
                                             q=10, labels=False) + 1
        return user_data
    
    def compute_correlation_matrix(self, user_data):
        """Compute correlation matrix for application data."""
        return user_data[self.app_columns].corr()
    
    def perform_pca(self, user_data):
        """Perform PCA on application data."""
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(user_data[self.app_columns])
        
        pca = PCA()
        pca_result = pca.fit_transform(scaled_data)
        
        # Calculate explained variance ratio
        explained_variance = pca.explained_variance_ratio_
        
        return {
            'pca_result': pca_result,
            'explained_variance': explained_variance,
            'components': pca.components_,
            'feature_names': self.app_columns
        } 