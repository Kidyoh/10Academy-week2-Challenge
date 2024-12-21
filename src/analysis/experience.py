"""User experience analysis module."""
import pandas as pd
import numpy as np

class ExperienceAnalyzer:
    """Class for analyzing user experience metrics."""
    
    def __init__(self, data):
        self.data = data
    
    def calculate_experience_metrics(self):
        """Calculate experience metrics per user."""
        metrics = self.data.groupby('user_id').agg({
            'tcp_retransmission': 'mean',
            'throughput': 'mean',
            'latency': 'mean',
            'packet_loss': 'mean'
        }).reset_index()
        
        # Calculate experience score
        metrics['experience_score'] = self._calculate_experience_score(metrics)
        return metrics
    
    def _calculate_experience_score(self, metrics):
        """Calculate overall experience score based on metrics."""
        # Normalize metrics between 0 and 1
        normalized_metrics = metrics.copy()
        for column in ['tcp_retransmission', 'latency', 'packet_loss']:
            normalized_metrics[column] = 1 - (metrics[column] - metrics[column].min()) / \
                                          (metrics[column].max() - metrics[column].min())
        
        normalized_metrics['throughput'] = (metrics['throughput'] - metrics['throughput'].min()) / \
                                         (metrics['throughput'].max() - metrics['throughput'].min())
        
        # Calculate weighted average
        weights = {
            'tcp_retransmission': 0.25,
            'throughput': 0.3,
            'latency': 0.25,
            'packet_loss': 0.2
        }
        
        score = sum(normalized_metrics[metric] * weight 
                   for metric, weight in weights.items())
        return score 