"""Data preparation utilities for dashboard."""
import pandas as pd
import numpy as np
from typing import Dict

def prepare_engagement_metrics(data: pd.DataFrame) -> pd.DataFrame:
    """Prepare engagement metrics from raw data."""
    try:
        # Calculate session duration in minutes
        engagement_data = pd.DataFrame()
        engagement_data['msisdn'] = data['MSISDN/Number']
        engagement_data['session_duration'] = data['Dur. (ms)'] / (1000 * 60)  # Convert to minutes
        
        # Calculate total data traffic (DL + UL)
        engagement_data['total_dl'] = data['Total DL (Bytes)'].fillna(0)
        engagement_data['total_ul'] = data['Total UL (Bytes)'].fillna(0)
        engagement_data['total_traffic'] = engagement_data['total_dl'] + engagement_data['total_ul']
        
        # Calculate app usage - first verify column names
        app_mapping = {
            'Social Media': ['Social Media DL (Bytes)', 'Social Media UL (Bytes)'],
            'Google': ['Google DL (Bytes)', 'Google UL (Bytes)'],
            'Email': ['Email DL (Bytes)', 'Email UL (Bytes)'],
            'Youtube': ['Youtube DL (Bytes)', 'Youtube UL (Bytes)'],
            'Netflix': ['Netflix DL (Bytes)', 'Netflix UL (Bytes)'],
            'Gaming': ['Gaming DL (Bytes)', 'Gaming UL (Bytes)'],
            'Other': ['Other DL (Bytes)', 'Other UL (Bytes)']
        }
        
        for app, cols in app_mapping.items():
            col_name = f"{app.lower().replace(' ', '_')}_usage"
            engagement_data[col_name] = data[cols[0]].fillna(0) + data[cols[1]].fillna(0)
        
        # Aggregate by user
        metrics_to_sum = ['session_duration', 'total_traffic', 
                         'social_media_usage', 'google_usage', 'email_usage',
                         'youtube_usage', 'netflix_usage', 'gaming_usage', 'other_usage']
        
        # Verify columns exist before aggregating
        available_metrics = [col for col in metrics_to_sum if col in engagement_data.columns]
        
        agg_dict = {metric: 'sum' for metric in available_metrics}
        user_metrics = engagement_data.groupby('msisdn').agg(agg_dict).reset_index()
        
        return user_metrics
        
    except Exception as e:
        print(f"Error preparing engagement metrics: {str(e)}")
        print("Available columns:", engagement_data.columns.tolist())
        raise

def prepare_experience_metrics(data: pd.DataFrame) -> pd.DataFrame:
    """Prepare experience metrics from raw data."""
    try:
        experience_data = pd.DataFrame()
        experience_data['msisdn'] = data['MSISDN/Number']
        
        # TCP retransmission
        experience_data['tcp_retrans_dl'] = data['TCP DL Retrans. Vol (Bytes)'].fillna(0)
        experience_data['tcp_retrans_ul'] = data['TCP UL Retrans. Vol (Bytes)'].fillna(0)
        
        # RTT
        experience_data['rtt_dl'] = data['Avg RTT DL (ms)'].fillna(data['Avg RTT DL (ms)'].mean())
        experience_data['rtt_ul'] = data['Avg RTT UL (ms)'].fillna(data['Avg RTT UL (ms)'].mean())
        
        # Throughput
        experience_data['throughput_dl'] = data['Avg Bearer TP DL (kbps)'].fillna(0)
        experience_data['throughput_ul'] = data['Avg Bearer TP UL (kbps)'].fillna(0)
        
        # Handset info
        experience_data['handset_type'] = data['Handset Type']
        experience_data['handset_manufacturer'] = data['Handset Manufacturer']
        
        # Aggregate by user
        user_metrics = experience_data.groupby('msisdn').agg({
            'tcp_retrans_dl': 'mean',
            'tcp_retrans_ul': 'mean',
            'rtt_dl': 'mean',
            'rtt_ul': 'mean',
            'throughput_dl': 'mean',
            'throughput_ul': 'mean',
            'handset_type': 'first',
            'handset_manufacturer': 'first'
        }).reset_index()
        
        # Calculate averages
        user_metrics['avg_tcp_retrans'] = (user_metrics['tcp_retrans_dl'] + user_metrics['tcp_retrans_ul']) / 2
        user_metrics['avg_rtt'] = (user_metrics['rtt_dl'] + user_metrics['rtt_ul']) / 2
        user_metrics['avg_throughput'] = (user_metrics['throughput_dl'] + user_metrics['throughput_ul']) / 2
        
        return user_metrics
        
    except Exception as e:
        print(f"Error preparing experience metrics: {str(e)}")
        raise

def prepare_handset_metrics(data: pd.DataFrame) -> pd.DataFrame:
    """Prepare handset-specific metrics."""
    try:
        handset_metrics = data.groupby('Handset Type').agg({
            'Avg Bearer TP DL (kbps)': 'mean',
            'Avg Bearer TP UL (kbps)': 'mean',
            'TCP DL Retrans. Vol (Bytes)': 'mean',
            'TCP UL Retrans. Vol (Bytes)': 'mean',
            'MSISDN/Number': 'count'
        }).reset_index()
        
        handset_metrics.columns = [
            'handset_type', 'avg_tp_dl', 'avg_tp_ul', 
            'avg_tcp_retrans_dl', 'avg_tcp_retrans_ul', 'user_count'
        ]
        
        # Calculate combined metrics
        handset_metrics['avg_throughput'] = (handset_metrics['avg_tp_dl'] + handset_metrics['avg_tp_ul']) / 2
        handset_metrics['avg_tcp_retrans'] = (handset_metrics['avg_tcp_retrans_dl'] + handset_metrics['avg_tcp_retrans_ul']) / 2
        
        return handset_metrics
        
    except Exception as e:
        print(f"Error preparing handset metrics: {str(e)}")
        raise

def prepare_dashboard_data(raw_data: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """Prepare all metrics for dashboard."""
    return {
        'engagement_metrics': prepare_engagement_metrics(raw_data),
        'experience_metrics': prepare_experience_metrics(raw_data),
        'handset_metrics': prepare_handset_metrics(raw_data),
        'raw_data': raw_data
    } 