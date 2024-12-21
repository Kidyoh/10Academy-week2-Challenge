"""Visualization components for Task 1."""
import streamlit as st
import plotly.express as px
from src.utils.enhanced_visualization import (
    create_handset_treemap,
    create_manufacturer_bar,
    create_usage_patterns_heatmap,
    create_usage_time_distribution,
    create_decile_analysis_plot
)

def render_handset_analysis(analyzer):
    """Render handset analysis section."""
    st.header("Handset Analysis")
    
    # Get analysis results
    handset_results = analyzer.analyze_handsets()
    
    try:
        # Display top 10 handsets
        st.subheader("Top 10 Handsets")
        fig_handsets = create_handset_treemap(handset_results['top_handsets'])
        st.plotly_chart(fig_handsets, use_container_width=True)
        
        # Display top manufacturers
        st.subheader("Top 3 Manufacturers")
        fig_manufacturers = create_manufacturer_bar(handset_results['top_manufacturers'])
        st.plotly_chart(fig_manufacturers, use_container_width=True)
        
        # Display data tables
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Top Handsets Data")
            st.dataframe(handset_results['top_handsets'])
        with col2:
            st.subheader("Top Manufacturers Data")
            st.dataframe(handset_results['top_manufacturers'])
            
    except Exception as e:
        st.error(f"Error rendering handset analysis: {str(e)}")
        st.exception(e)

def render_user_behavior_analysis(analyzer):
    """Render user behavior analysis section."""
    st.header("User Behavior Analysis")
    
    try:
        # Get analysis results
        behavior_results = analyzer.analyze_user_behavior()
        
        # Display usage patterns
        st.subheader("Application Usage Patterns")
        fig_usage = create_usage_patterns_heatmap(behavior_results['user_metrics'])
        st.plotly_chart(fig_usage, use_container_width=True)
        
        # Display session duration distribution
        st.subheader("Session Duration Distribution")
        fig_duration = create_usage_time_distribution(behavior_results['user_metrics'])
        st.plotly_chart(fig_duration, use_container_width=True)
        
        # Display decile analysis
        st.subheader("Usage Analysis by Duration Deciles")
        fig_deciles = create_decile_analysis_plot(behavior_results['decile_stats'])
        st.plotly_chart(fig_deciles, use_container_width=True)
        
        # Display raw data
        if st.checkbox("Show Raw Data"):
            st.dataframe(behavior_results['decile_stats'])
            
    except Exception as e:
        st.error(f"Error rendering user behavior analysis: {str(e)}")
        st.exception(e)