"""Visualization components for Task 1."""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from src.utils.task1_visualization import (
    plot_top_handsets,
    plot_app_usage_distribution,
    plot_correlation_heatmap
)

def render_handset_analysis(analyzer):
    """Render handset analysis section."""
    st.header("Handset Analysis")
    
    # Get analysis results
    handset_results = analyzer.analyze_handsets()
    
    # Display top 10 handsets
    st.subheader("Top 10 Handsets")
    fig_handsets = plot_top_handsets(handset_results['top_handsets'])
    st.plotly_chart(fig_handsets)
    
    # Display top manufacturers
    st.subheader("Top 3 Manufacturers")
    fig_manufacturers = plot_top_handsets(
        handset_results['top_manufacturers'],
        title="Top Handset Manufacturers"
    )
    st.plotly_chart(fig_manufacturers)
    
    # Display top handsets per manufacturer
    st.subheader("Top Handsets by Manufacturer")
    selected_manufacturer = st.selectbox(
        "Select Manufacturer",
        options=handset_results['top_manufacturers']['manufacturer'].tolist()
    )
    
    if selected_manufacturer:
        fig_manufacturer_handsets = plot_top_handsets(
            handset_results['top_handsets_per_manufacturer'][selected_manufacturer],
            title=f"Top 5 Handsets for {selected_manufacturer}"
        )
        st.plotly_chart(fig_manufacturer_handsets)

def render_user_behavior_analysis(analyzer):
    """Render user behavior analysis section."""
    st.header("User Behavior Analysis")
    
    # Get analysis results
    behavior_results = analyzer.analyze_user_behavior()
    
    # Display application usage distribution
    st.subheader("Application Usage Distribution")
    fig_usage = plot_app_usage_distribution(
        behavior_results['user_metrics'],
        ['social_media_total_bytes', 'google_total_bytes', 'email_total_bytes',
         'youtube_total_bytes', 'netflix_total_bytes', 'gaming_total_bytes']
    )
    st.plotly_chart(fig_usage)
    
    # Display decile analysis
    st.subheader("Usage Analysis by Duration Deciles")
    st.dataframe(behavior_results['decile_stats']) 