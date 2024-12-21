"""Visualization utilities."""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_distribution_plot(data, column, title=None, bins=30):
    """Create a distribution plot using plotly."""
    fig = px.histogram(data, x=column, nbins=bins)
    if title:
        fig.update_layout(title=title)
    return fig

def create_scatter_plot(data, x, y, color=None, title=None):
    """Create a scatter plot using plotly."""
    fig = px.scatter(data, x=x, y=y, color=color)
    if title:
        fig.update_layout(title=title)
    return fig

def create_metric_summary(data, metric_columns, title=None):
    """Create a summary box plot for multiple metrics."""
    fig = go.Figure()
    for col in metric_columns:
        fig.add_trace(go.Box(y=data[col], name=col))
    if title:
        fig.update_layout(title=title)
    return fig 