"""Visualization utilities for engagement analysis."""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from typing import Dict, Tuple, List

def plot_top_users(top_users_dict: Dict[str, pd.DataFrame]) -> Dict[str, go.Figure]:
    """Create visualizations for top users per metric."""
    figs = {}
    
    for metric, df in top_users_dict.items():
        fig = px.bar(
            df,
            x='msisdn',
            y=metric,
            title=f'Top 10 Users by {metric.replace("_", " ").title()}'
        )
        fig.update_layout(
            xaxis_title="User ID",
            yaxis_title=metric.replace("_", " ").title(),
            showlegend=False
        )
        figs[metric] = fig
    
    return figs

def plot_cluster_analysis(cluster_stats: Dict) -> go.Figure:
    """Create visualization for cluster analysis."""
    metrics = ['session_count', 'total_duration', 'total_traffic']
    clusters = list(cluster_stats.keys())
    
    fig = go.Figure()
    
    for metric in metrics:
        y_values = [stats['metrics'][metric]['mean'] for stats in cluster_stats.values()]
        fig.add_trace(go.Bar(
            name=metric.replace("_", " ").title(),
            x=clusters,
            y=y_values
        ))
    
    fig.update_layout(
        title="Cluster Characteristics",
        barmode='group',
        xaxis_title="Cluster",
        yaxis_title="Average Value"
    )
    
    return fig

def plot_app_usage(app_totals: Dict[str, float]) -> go.Figure:
    """Create visualization for application usage."""
    apps = list(app_totals.keys())
    values = list(app_totals.values())
    
    # Convert to GB for better readability
    values_gb = [v/1e9 for v in values]
    
    fig = px.pie(
        values=values_gb,
        names=apps,
        title='Total Traffic by Application (GB)'
    )
    
    return fig

def plot_elbow_curve(k_values: List[int], inertias: List[float]) -> go.Figure:
    """Create elbow curve visualization."""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=k_values,
        y=inertias,
        mode='lines+markers'
    ))
    
    fig.update_layout(
        title='Elbow Method for Optimal k',
        xaxis_title='Number of Clusters (k)',
        yaxis_title='Inertia'
    )
    
    return fig 