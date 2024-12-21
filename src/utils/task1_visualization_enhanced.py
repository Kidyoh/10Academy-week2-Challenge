"""Enhanced visualization utilities for Task 1."""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def plot_top_handsets(handset_data: pd.DataFrame) -> go.Figure:
    """Create visualization for top handsets."""
    fig = go.Figure(data=[
        go.Bar(
            x=handset_data['handset'],
            y=handset_data['count'],
            text=handset_data['count'],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title='Top 10 Handsets by Usage',
        xaxis_title="Handset Model",
        yaxis_title="Number of Users",
        xaxis_tickangle=-45,
        height=600,
        showlegend=False
    )
    
    return fig

def plot_manufacturer_distribution(manufacturer_data: pd.DataFrame) -> go.Figure:
    """Create visualization for manufacturer distribution."""
    # Calculate market share percentage
    total_users = manufacturer_data['count'].sum()
    manufacturer_data['market_share'] = (manufacturer_data['count'] / total_users * 100).round(2)
    
    fig = go.Figure(data=[
        go.Pie(
            labels=manufacturer_data['manufacturer'],
            values=manufacturer_data['count'],
            hovertemplate="<b>%{label}</b><br>" +
                         "Users: %{value}<br>" +
                         "Market Share: %{text}%",
            text=manufacturer_data['market_share'].apply(lambda x: f"{x:.1f}%")
        )
    ])
    
    fig.update_layout(
        title='Manufacturer Market Share Distribution',
        height=500
    )
    
    return fig

def plot_user_behavior(handset_data: pd.DataFrame) -> go.Figure:
    """Create visualization for user behavior patterns."""
    # Create a subplot with 2 rows
    fig = go.Figure()
    
    # Add manufacturer adoption trend
    manufacturer_trend = (
        handset_data.groupby('Handset Manufacturer')
        .size()
        .sort_values(ascending=True)
    )
    
    fig.add_trace(go.Bar(
        x=manufacturer_trend.values,
        y=manufacturer_trend.index,
        orientation='h',
        name='Users per Manufacturer'
    ))
    
    fig.update_layout(
        title='Manufacturer Adoption Pattern',
        xaxis_title="Number of Users",
        yaxis_title="Manufacturer",
        height=600,
        showlegend=False
    )
    
    return fig

def create_task1_visualizations(handset_results: dict) -> dict:
    """Create all visualizations for Task 1."""
    return {
        'handset_viz': plot_top_handsets(handset_results['top_handsets']),
        'manufacturer_viz': plot_manufacturer_distribution(handset_results['top_manufacturers']),
        'behavior_viz': plot_user_behavior(handset_results['handset_data'])
    } 