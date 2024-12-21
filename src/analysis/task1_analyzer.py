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
        
        # Log the column names for debugging
        logger.info(f"Handset info columns: {self.handset_info.columns.tolist()}")
    
    def analyze_handsets(self) -> Dict[str, pd.DataFrame]:
        """Analyze handset information as per Task 1 requirements."""
        # Remove any missing values
        handset_data = self.handset_info.dropna(subset=['handset', 'Handset Manufacturer'])
        
        # Print column names for debugging
        logger.info(f"Handset data columns: {handset_data.columns.tolist()}")
        
        # Top 10 handsets
        top_handsets = (handset_data['handset']
                       .value_counts()
                       .head(10)
                       .reset_index())
        
        # Keep original column names
        top_handsets.columns = ['handset', 'count']
        logger.info(f"Top handsets shape: {top_handsets.shape}")
        logger.info(f"Top handsets columns: {top_handsets.columns.tolist()}")
        
        # Top 3 manufacturers
        top_manufacturers = (handset_data['Handset Manufacturer']
                           .value_counts()
                           .head(3)
                           .reset_index())
        top_manufacturers.columns = ['manufacturer', 'count']
        
        return {
            'top_handsets': top_handsets,
            'top_manufacturers': top_manufacturers,
            'handset_data': handset_data
        }
    
    def analyze_user_behavior(self) -> Dict[str, pd.DataFrame]:
        """Analyze user behavior on applications."""
        # Calculate total data per user
        user_metrics = self.app_usage.copy()
        
        # Log column names for debugging
        logger.info(f"User metrics columns: {user_metrics.columns.tolist()}")
        
        # Convert duration from milliseconds to seconds for better readability
        user_metrics['session_duration'] = user_metrics['session_duration'] / 1000
        
        # Calculate total bytes for each application
        app_metrics = {
            'social_media': ['Social Media DL (Bytes)', 'Social Media UL (Bytes)'],
            'google': ['Google DL (Bytes)', 'Google UL (Bytes)'],
            'email': ['Email DL (Bytes)', 'Email UL (Bytes)'],
            'youtube': ['Youtube DL (Bytes)', 'Youtube UL (Bytes)'],
            'netflix': ['Netflix DL (Bytes)', 'Netflix UL (Bytes)'],
            'gaming': ['Gaming DL (Bytes)', 'Gaming UL (Bytes)']
        }
        
        # Calculate total bytes for each application
        for app, columns in app_metrics.items():
            user_metrics[f'{app}_total_bytes'] = user_metrics[columns[0]] + user_metrics[columns[1]]
        
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
            'gaming_total_bytes': 'sum'
        }).round(2)
        
        # Log analysis completion
        logger.info("User behavior analysis completed")
        logger.info(f"Analyzed {len(user_metrics)} users across {len(decile_stats)} deciles")
        
        return {
            'user_metrics': user_metrics,
            'decile_stats': decile_stats,
            'app_metrics': app_metrics  # Include the mapping for reference
        } 