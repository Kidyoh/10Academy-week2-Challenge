"""Task 1 specific analysis module."""
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger('tellco_analysis')

class Task1Analyzer:
    """Analyzer specifically for Task 1 requirements."""
    
    def __init__(self, data: Dict[str, pd.DataFrame]):
        self.app_usage = data['app_usage']
        self.handset_info = data['handset_info']
        self.raw_data = data['raw_data']
    
    def analyze_handsets(self) -> Dict[str, pd.DataFrame]:
        """Analyze handset information as per Task 1 requirements."""
        # Remove any missing values
        handset_data = self.handset_info.dropna(subset=['handset', 'manufacturer'])
        
        # Top 10 handsets
        top_handsets = (handset_data['handset']
                       .value_counts()
                       .head(10)
                       .reset_index()
                       .rename(columns={'index': 'handset', 'handset': 'count'}))
        
        # Top 3 manufacturers
        top_manufacturers = (handset_data['manufacturer']
                           .value_counts()
                           .head(3)
                           .reset_index()
                           .rename(columns={'index': 'manufacturer', 'manufacturer': 'count'}))
        
        # Top 5 handsets per top 3 manufacturer
        top_handsets_per_manufacturer = {}
        for manufacturer in top_manufacturers['manufacturer']:
            manufacturer_data = handset_data[
                handset_data['manufacturer'] == manufacturer
            ]
            top_handsets_per_manufacturer[manufacturer] = (
                manufacturer_data['handset']
                .value_counts()
                .head(5)
                .reset_index()
                .rename(columns={'index': 'handset', 'handset': 'count'})
            )
        
        return {
            'top_handsets': top_handsets,
            'top_manufacturers': top_manufacturers,
            'top_handsets_per_manufacturer': top_handsets_per_manufacturer
        }
    
    def analyze_user_behavior(self) -> Dict[str, pd.DataFrame]:
        """Analyze user behavior on applications."""
        # Calculate total data per user
        user_metrics = self.app_usage.copy()
        
        # Convert duration from milliseconds to seconds for better readability
        user_metrics['session_duration'] = user_metrics['session_duration'] / 1000
        
        # Create duration deciles
        user_metrics['duration_decile'] = pd.qcut(
            user_metrics['session_duration'],
            q=10,
            labels=False
        ) + 1
        
        # Calculate statistics per decile
        decile_stats = user_metrics.groupby('duration_decile').agg({
            'session_duration': ['mean', 'median', 'count'],
            'social_media_total_bytes': 'sum',
            'google_total_bytes': 'sum',
            'email_total_bytes': 'sum',
            'youtube_total_bytes': 'sum',
            'netflix_total_bytes': 'sum',
            'gaming_total_bytes': 'sum',
            'other_total_bytes': 'sum'
        }).round(2)
        
        return {
            'user_metrics': user_metrics,
            'decile_stats': decile_stats
        } 