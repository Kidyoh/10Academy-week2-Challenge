"""User experience analysis module."""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import logging

logger = logging.getLogger('tellco_analysis')

class ExperienceAnalyzer:
    """Class for analyzing user experience metrics."""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.experience_metrics = None
        
    def aggregate_user_experience(self) -> pd.DataFrame:
        """Aggregate experience metrics per customer."""
        # Handle missing values
        metrics_columns = {
            'TCP DL Retrans. Vol (Bytes)': 'tcp_dl_retrans',
            'TCP UL Retrans. Vol (Bytes)': 'tcp_ul_retrans',
            'Avg RTT DL (ms)': 'rtt_dl',
            'Avg RTT UL (ms)': 'rtt_ul',
            'Avg Bearer TP DL (kbps)': 'throughput_dl',
            'Avg Bearer TP UL (kbps)': 'throughput_ul'
        }
        
        # Fill missing values with mean
        for col in metrics_columns.keys():
            self.data[col] = self.data[col].fillna(self.data[col].mean())
        
        # Aggregate metrics per user
        metrics = self.data.groupby('MSISDN/Number').agg({
            'TCP DL Retrans. Vol (Bytes)': 'mean',
            'TCP UL Retrans. Vol (Bytes)': 'mean',
            'Avg RTT DL (ms)': 'mean',
            'Avg RTT UL (ms)': 'mean',
            'Avg Bearer TP DL (kbps)': 'mean',
            'Avg Bearer TP UL (kbps)': 'mean',
            'Handset Type': lambda x: x.mode()[0] if not x.mode().empty else 'Unknown'
        }).reset_index()
        
        # Rename columns
        metrics.columns = ['msisdn'] + list(metrics_columns.values()) + ['handset_type']
        
        # Calculate averages
        metrics['avg_tcp_retrans'] = (metrics['tcp_dl_retrans'] + metrics['tcp_ul_retrans']) / 2
        metrics['avg_rtt'] = (metrics['rtt_dl'] + metrics['rtt_ul']) / 2
        metrics['avg_throughput'] = (metrics['throughput_dl'] + metrics['throughput_ul']) / 2
        
        # Remove outliers (using IQR method)
        for col in ['avg_tcp_retrans', 'avg_rtt', 'avg_throughput']:
            Q1 = metrics[col].quantile(0.25)
            Q3 = metrics[col].quantile(0.75)
            IQR = Q3 - Q1
            metrics[col] = metrics[col].clip(lower=Q1 - 1.5*IQR, upper=Q3 + 1.5*IQR)
        
        self.experience_metrics = metrics
        return metrics
    
    def get_metric_distributions(self) -> dict:
        """Get top, bottom, and most frequent values for metrics."""
        if self.experience_metrics is None:
            self.aggregate_user_experience()
        
        metrics = ['avg_tcp_retrans', 'avg_rtt', 'avg_throughput']
        distributions = {}
        
        for metric in metrics:
            distributions[metric] = {
                'top_10': self.experience_metrics.nlargest(10, metric)[['msisdn', metric, 'handset_type']],
                'bottom_10': self.experience_metrics.nsmallest(10, metric)[['msisdn', metric, 'handset_type']],
                'most_frequent': self.experience_metrics[metric].value_counts().head(10)
            }
        
        return distributions
    
    def analyze_throughput_by_handset(self) -> pd.DataFrame:
        """Analyze throughput distribution per handset type."""
        if self.experience_metrics is None:
            self.aggregate_user_experience()
            
        analysis = self.experience_metrics.groupby('handset_type').agg({
            'avg_throughput': ['mean', 'std', 'count', 'min', 'max']
        }).round(2)
        
        # Add interpretation
        analysis['interpretation'] = analysis.apply(
            lambda x: f"Average throughput: {x['avg_throughput']['mean']:.2f} kbps, "
                     f"Standard deviation: {x['avg_throughput']['std']:.2f} kbps, "
                     f"Sample size: {x['avg_throughput']['count']} users", axis=1)
        
        return analysis
    
    def analyze_tcp_by_handset(self) -> pd.DataFrame:
        """Analyze TCP retransmission per handset type."""
        if self.experience_metrics is None:
            self.aggregate_user_experience()
            
        analysis = self.experience_metrics.groupby('handset_type').agg({
            'avg_tcp_retrans': ['mean', 'std', 'count', 'min', 'max']
        }).round(2)
        
        # Add interpretation
        analysis['interpretation'] = analysis.apply(
            lambda x: f"Average TCP retrans: {x['avg_tcp_retrans']['mean']:.2f} bytes, "
                     f"Standard deviation: {x['avg_tcp_retrans']['std']:.2f} bytes, "
                     f"Sample size: {x['avg_tcp_retrans']['count']} users", axis=1)
        
        return analysis
    
    def cluster_users(self, k: int = 3) -> tuple:
        """Cluster users based on experience metrics."""
        if self.experience_metrics is None:
            self.aggregate_user_experience()
        
        # Select features for clustering
        features = ['avg_tcp_retrans', 'avg_rtt', 'avg_throughput']
        X = self.experience_metrics[features].copy()
        
        # Normalize features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Perform clustering
        kmeans = KMeans(n_clusters=k, random_state=42)
        self.experience_metrics['cluster'] = kmeans.fit_predict(X_scaled)
        
        # Calculate cluster characteristics
        cluster_stats = self.experience_metrics.groupby('cluster').agg({
            'avg_tcp_retrans': ['mean', 'min', 'max'],
            'avg_rtt': ['mean', 'min', 'max'],
            'avg_throughput': ['mean', 'min', 'max'],
            'msisdn': 'count'
        }).round(2)
        
        # Add cluster descriptions
        descriptions = {
            0: "Good Experience: Low TCP retrans, Low RTT, High throughput",
            1: "Average Experience: Moderate values across metrics",
            2: "Poor Experience: High TCP retrans, High RTT, Low throughput"
        }
        
        cluster_stats['description'] = cluster_stats.index.map(descriptions)
        
        return self.experience_metrics, cluster_stats