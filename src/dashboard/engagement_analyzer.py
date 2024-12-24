"""User engagement analysis module."""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from typing import Dict, Tuple
import logging

logger = logging.getLogger('tellco_analysis')

class EngagementAnalyzer:
    """Class for analyzing user engagement metrics."""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.engagement_metrics = None
        
    def calculate_engagement_metrics(self) -> pd.DataFrame:
        """Calculate basic engagement metrics per user."""
        metrics = self.data.groupby('MSISDN/Number').agg({
            'Bearer Id': 'count',  # Session frequency
            'Dur. (ms)': 'sum',    # Total duration
            'Total DL (Bytes)': 'sum',  # Total download
            'Total UL (Bytes)': 'sum'   # Total upload
        }).reset_index()
        
        # Rename columns
        metrics.columns = ['msisdn', 'session_count', 'total_duration', 'total_dl', 'total_ul']
        
        # Add total traffic
        metrics['total_traffic'] = metrics['total_dl'] + metrics['total_ul']
        
        self.engagement_metrics = metrics
        return metrics
    
    def get_top_users(self, n: int = 10) -> Dict[str, pd.DataFrame]:
        """Get top n users per engagement metric."""
        if self.engagement_metrics is None:
            self.calculate_engagement_metrics()
        
        metrics = ['session_count', 'total_duration', 'total_traffic']
        top_users = {}
        
        for metric in metrics:
            top_users[metric] = (
                self.engagement_metrics
                .nlargest(n, metric)
                [['msisdn', metric]]
                .reset_index(drop=True)
            )
        
        return top_users
    
    def cluster_users(self, k: int = 3) -> Tuple[pd.DataFrame, Dict]:
        """Cluster users based on engagement metrics."""
        if self.engagement_metrics is None:
            self.calculate_engagement_metrics()
        
        # Select features for clustering
        features = ['session_count', 'total_duration', 'total_traffic']
        X = self.engagement_metrics[features].copy()
        
        # Normalize features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Perform clustering
        kmeans = KMeans(n_clusters=k, random_state=42)
        clusters = kmeans.fit_predict(X_scaled)
        
        # Add cluster labels to metrics
        self.engagement_metrics['cluster'] = clusters
        
        # Calculate cluster statistics
        cluster_stats = {}
        for i in range(k):
            cluster_data = self.engagement_metrics[self.engagement_metrics['cluster'] == i]
            cluster_stats[f'cluster_{i}'] = {
                'size': len(cluster_data),
                'metrics': {
                    feature: {
                        'min': cluster_data[feature].min(),
                        'max': cluster_data[feature].max(),
                        'mean': cluster_data[feature].mean(),
                        'total': cluster_data[feature].sum()
                    }
                    for feature in features
                }
            }
        
        return self.engagement_metrics, cluster_stats
    
    def analyze_app_engagement(self) -> Dict[str, pd.DataFrame]:
        """Analyze engagement per application."""
        # Calculate total traffic per app per user
        apps = {
            'Social Media': ['Social Media DL (Bytes)', 'Social Media UL (Bytes)'],
            'Google': ['Google DL (Bytes)', 'Google UL (Bytes)'],
            'Email': ['Email DL (Bytes)', 'Email UL (Bytes)'],
            'Youtube': ['Youtube DL (Bytes)', 'Youtube UL (Bytes)'],
            'Netflix': ['Netflix DL (Bytes)', 'Netflix UL (Bytes)'],
            'Gaming': ['Gaming DL (Bytes)', 'Gaming UL (Bytes)']
        }
        
        app_engagement = {}
        for app, columns in apps.items():
            app_traffic = (
                self.data.groupby('MSISDN/Number')
                [columns].sum()
                .sum(axis=1)
                .sort_values(ascending=False)
                .head(10)
                .reset_index()
            )
            app_traffic.columns = ['msisdn', 'total_traffic']
            app_engagement[app] = app_traffic
        
        # Calculate total traffic per app
        app_totals = {
            app: self.data[columns].sum().sum()
            for app, columns in apps.items()
        }
        
        return {
            'top_users': app_engagement,
            'app_totals': app_totals
        }
    
    def find_optimal_k(self, max_k: int = 10) -> Dict:
        """Find optimal number of clusters using elbow method."""
        if self.engagement_metrics is None:
            self.calculate_engagement_metrics()
        
        features = ['session_count', 'total_duration', 'total_traffic']
        X = self.engagement_metrics[features].copy()
        
        # Normalize features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Calculate inertia for different k values
        inertias = []
        for k in range(1, max_k + 1):
            kmeans = KMeans(n_clusters=k, random_state=42)
            kmeans.fit(X_scaled)
            inertias.append(kmeans.inertia_)
        
        return {
            'k_values': list(range(1, max_k + 1)),
            'inertias': inertias
        } 