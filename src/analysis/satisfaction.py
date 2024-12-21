"""User satisfaction analysis module."""
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

class SatisfactionAnalyzer:
    """Class for analyzing user satisfaction."""
    
    def __init__(self, data):
        self.data = data
    
    def segment_users(self, n_clusters=3):
        """Segment users based on their behavior and experience."""
        features = ['total_data', 'session_duration', 'experience_score']
        
        # Prepare features for clustering
        X = self.data[features].copy()
        for feature in features:
            X[feature] = (X[feature] - X[feature].mean()) / X[feature].std()
        
        # Perform clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        self.data['satisfaction_cluster'] = kmeans.fit_predict(X)
        
        return self.data
    
    def get_satisfaction_metrics(self):
        """Calculate satisfaction metrics per segment."""
        if 'satisfaction_cluster' not in self.data.columns:
            self.segment_users()
            
        metrics = self.data.groupby('satisfaction_cluster').agg({
            'total_data': 'mean',
            'session_duration': 'mean',
            'experience_score': 'mean',
            'user_id': 'count'
        }).reset_index()
        
        metrics = metrics.rename(columns={'user_id': 'user_count'})
        return metrics 