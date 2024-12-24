"""Task 3: User Experience Analysis Module."""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from typing import Dict, List, Optional

class ExperienceAnalyzer:
    """Analyzer for user experience metrics."""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self._preprocess_data()
    
    def _preprocess_data(self):
        """Preprocess the data for analysis."""
        # Handle missing values
        self.data['TCP DL Retrans. Vol (Bytes)'] = self.data['TCP DL Retrans. Vol (Bytes)'].fillna(0)
        self.data['TCP UL Retrans. Vol (Bytes)'] = self.data['TCP UL Retrans. Vol (Bytes)'].fillna(0)
        self.data['Avg RTT DL (ms)'] = self.data['Avg RTT DL (ms)'].fillna(self.data['Avg RTT DL (ms)'].mean())
        self.data['Avg RTT UL (ms)'] = self.data['Avg RTT UL (ms)'].fillna(self.data['Avg RTT UL (ms)'].mean())
    
    def calculate_experience_metrics(self) -> Dict[str, float]:
        """Calculate average experience metrics."""
        return {
            'avg_tcp_retrans': (
                self.data['TCP DL Retrans. Vol (Bytes)'].mean() +
                self.data['TCP UL Retrans. Vol (Bytes)'].mean()
            ) / 2,
            'avg_rtt': (
                self.data['Avg RTT DL (ms)'].mean() +
                self.data['Avg RTT UL (ms)'].mean()
            ) / 2,
            'avg_throughput': (
                self.data['Avg Bearer TP DL (kbps)'].mean() +
                self.data['Avg Bearer TP UL (kbps)'].mean()
            ) / 2
        }
    
    def analyze_tcp_retransmission(self, handset_types: Optional[List[str]] = None) -> pd.DataFrame:
        """Analyze TCP retransmission by handset type."""
        df = self.data.copy()
        if handset_types:
            df = df[df['Handset Type'].isin(handset_types)]
            
        df['TCP Retransmission Volume'] = (
            df['TCP DL Retrans. Vol (Bytes)'] + 
            df['TCP UL Retrans. Vol (Bytes)']
        )
        
        return df[['Handset Type', 'TCP Retransmission Volume']]
    
    def analyze_throughput(self, direction: str = 'DL', handset_types: Optional[List[str]] = None) -> pd.DataFrame:
        """Analyze throughput by direction and handset type."""
        df = self.data.copy()
        if handset_types:
            df = df[df['Handset Type'].isin(handset_types)]
            
        df['Throughput'] = df[f'Avg Bearer TP {direction} (kbps)']
        return df[['Handset Type', 'Throughput']]
    
    def analyze_rtt(self, handset_types: Optional[List[str]] = None) -> pd.DataFrame:
        """Analyze RTT vs throughput."""
        df = self.data.copy()
        if handset_types:
            df = df[df['Handset Type'].isin(handset_types)]
            
        df['RTT'] = (df['Avg RTT DL (ms)'] + df['Avg RTT UL (ms)']) / 2
        df['Throughput'] = (df['Avg Bearer TP DL (kbps)'] + df['Avg Bearer TP UL (kbps)']) / 2
        
        return df[['Handset Type', 'RTT', 'Throughput']]
    
    def calculate_experience_scores(self) -> pd.DataFrame:
        """Calculate experience scores for each user."""
        # Prepare features
        features = [
            'TCP DL Retrans. Vol (Bytes)',
            'TCP UL Retrans. Vol (Bytes)',
            'Avg RTT DL (ms)',
            'Avg RTT UL (ms)',
            'Avg Bearer TP DL (kbps)',
            'Avg Bearer TP UL (kbps)'
        ]
        
        X = self.data[features].copy()
        
        # Normalize features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Calculate experience score (higher is better)
        experience_scores = pd.DataFrame()
        experience_scores['msisdn'] = self.data['MSISDN/Number']
        experience_scores['experience_score'] = (
            (X_scaled[:, 4] + X_scaled[:, 5]) -  # Throughput (positive impact)
            (X_scaled[:, 0] + X_scaled[:, 1] + X_scaled[:, 2] + X_scaled[:, 3])  # Negative impacts
        ) / 6  # Average across all components
        
        return experience_scores
    
    def get_detailed_statistics(self) -> pd.DataFrame:
        """Get detailed statistics for experience metrics."""
        metrics = [
            'TCP DL Retrans. Vol (Bytes)',
            'TCP UL Retrans. Vol (Bytes)',
            'Avg RTT DL (ms)',
            'Avg RTT UL (ms)',
            'Avg Bearer TP DL (kbps)',
            'Avg Bearer TP UL (kbps)'
        ]
        
        return self.data[metrics].describe() 