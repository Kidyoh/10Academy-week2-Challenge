"""Visualization utilities for Task 1."""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def plot_top_handsets(data, title="Top Handsets"):
    """Create bar plot for top handsets."""
    fig = px.bar(data, 
                 x='handset', 
                 y='count',
                 title=title)
    fig.update_layout(xaxis_tickangle=-45)
    return fig

def plot_app_usage_distribution(data, app_columns):
    """Create box plots for application usage distribution."""
    fig = go.Figure()
    for col in app_columns:
        fig.add_trace(go.Box(y=data[col], name=col))
    fig.update_layout(title="Application Usage Distribution",
                     yaxis_title="Data Volume (Bytes)",
                     showlegend=False)
    return fig

def plot_correlation_heatmap(correlation_matrix):
    """Create correlation heatmap."""
    fig = px.imshow(correlation_matrix,
                    labels=dict(color="Correlation"),
                    color_continuous_scale="RdBu")
    fig.update_layout(title="Application Usage Correlation Matrix")
    return fig

def plot_pca_explained_variance(explained_variance):
    """Create scree plot for PCA."""
    fig = px.line(x=range(1, len(explained_variance) + 1),
                  y=explained_variance,
                  markers=True,
                  title="PCA Explained Variance Ratio",
                  labels={'x': 'Principal Component', 
                         'y': 'Explained Variance Ratio'})
    return fig 