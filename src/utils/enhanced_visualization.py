"""Enhanced visualization utilities."""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def create_handset_treemap(handset_data):
    """Create treemap visualization of handset distribution."""
    fig = px.treemap(
        handset_data,
        path=['manufacturer', 'handset'],
        values='count',
        title='Handset Distribution by Manufacturer'
    )
    return fig

def create_usage_patterns_heatmap(user_metrics):
    """Create heatmap of application usage patterns."""
    # Normalize the data for better visualization
    apps = ['social_media', 'google', 'email', 'youtube', 'netflix', 'gaming']
    usage_data = user_metrics[[f'{app}_total_bytes' for app in apps]].copy()
    
    # Log transform for better visualization
    usage_data = np.log1p(usage_data)
    
    # Create correlation matrix
    corr_matrix = usage_data.corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix,
        x=apps,
        y=apps,
        colorscale='RdBu',
        zmin=-1,
        zmax=1
    ))
    
    fig.update_layout(
        title='Application Usage Correlation Heatmap',
        xaxis_title='Application',
        yaxis_title='Application'
    )
    
    return fig

def create_usage_time_distribution(user_metrics):
    """Create distribution plot of usage time."""
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=user_metrics['session_duration'],
        nbinsx=50,
        name='Session Duration'
    ))
    
    fig.update_layout(
        title='Distribution of Session Durations',
        xaxis_title='Duration (seconds)',
        yaxis_title='Count',
        showlegend=True
    )
    
    return fig 