"""Enhanced visualization utilities."""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def create_handset_treemap(handset_data):
    """Create treemap visualization of handset distribution."""
    # Print data for debugging
    print("Handset data columns:", handset_data.columns)
    print("First few rows:", handset_data.head())
    
    # Prepare data for treemap
    df = handset_data.copy()
    
    # Ensure we have the required columns
    if not {'handset', 'count'}.issubset(df.columns):
        print("Available columns:", df.columns.tolist())
        raise KeyError(f"Required columns 'handset' and 'count' not found. Available columns: {df.columns.tolist()}")
    
    # Create treemap
    fig = go.Figure(go.Treemap(
        labels=df['handset'],
        parents=['All'] * len(df),
        values=df['count'],
        textinfo="label+value"
    ))
    
    fig.update_layout(
        title='Top 10 Handsets Distribution',
        width=800,
        height=600
    )
    return fig

def create_manufacturer_bar(manufacturer_data):
    """Create bar chart for manufacturer distribution."""
    fig = px.bar(
        manufacturer_data,
        x='manufacturer',
        y='count',
        title='Top Manufacturers Distribution'
    )
    fig.update_layout(
        xaxis_title="Manufacturer",
        yaxis_title="Count",
        showlegend=False
    )
    return fig

def create_usage_patterns_heatmap(user_metrics):
    """Create heatmap of application usage patterns."""
    # Get the total bytes columns
    total_bytes_cols = [col for col in user_metrics.columns if col.endswith('_total_bytes')]
    
    if not total_bytes_cols:
        raise ValueError("No total bytes columns found in the data")
    
    # Normalize the data for better visualization
    usage_data = user_metrics[total_bytes_cols].copy()
    
    # Handle zeros and log transform
    usage_data = usage_data.replace(0, 1)  # Replace zeros with 1 before log transform
    usage_data = np.log1p(usage_data)
    
    # Create correlation matrix
    corr_matrix = usage_data.corr()
    
    # Clean up labels
    labels = [col.replace('_total_bytes', '').replace('_', ' ').title() 
             for col in total_bytes_cols]
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix,
        x=labels,
        y=labels,
        colorscale='RdBu',
        zmin=-1,
        zmax=1
    ))
    
    fig.update_layout(
        title='Application Usage Correlation Heatmap',
        xaxis_title="Application",
        yaxis_title="Application",
        width=800,
        height=600
    )
    
    return fig

def create_usage_time_distribution(user_metrics):
    """Create distribution plot of usage time."""
    fig = go.Figure()
    
    # Remove outliers for better visualization
    Q1 = user_metrics['session_duration'].quantile(0.25)
    Q3 = user_metrics['session_duration'].quantile(0.75)
    IQR = Q3 - Q1
    filtered_duration = user_metrics[
        (user_metrics['session_duration'] >= Q1 - 1.5 * IQR) &
        (user_metrics['session_duration'] <= Q3 + 1.5 * IQR)
    ]['session_duration']
    
    fig.add_trace(go.Histogram(
        x=filtered_duration,
        nbinsx=50,
        name='Session Duration'
    ))
    
    fig.update_layout(
        title='Distribution of Session Durations (Excluding Outliers)',
        xaxis_title="Duration (seconds)",
        yaxis_title="Count",
        showlegend=True,
        width=800,
        height=500
    )
    
    return fig

def create_decile_analysis_plot(decile_stats):
    """Create visualization for decile analysis."""
    # Prepare data
    df = decile_stats.copy()
    df.columns = [f"{col[0]}_{col[1]}" if isinstance(col, tuple) else col 
                 for col in df.columns]
    df = df.reset_index()
    
    fig = go.Figure()
    
    # Add session duration mean
    fig.add_trace(go.Bar(
        x=df['duration_decile'],
        y=df['session_duration_mean'],
        name='Mean Duration'
    ))
    
    fig.update_layout(
        title='Session Duration by Decile',
        xaxis_title="Decile",
        yaxis_title="Mean Duration (seconds)",
        showlegend=True,
        width=800,
        height=500
    )
    
    return fig 