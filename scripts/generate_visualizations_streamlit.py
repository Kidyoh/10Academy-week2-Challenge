"""Generate visualizations using Streamlit."""
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from src.dashboard.data_loader import Task1DataLoader
from src.analysis.task1_analyzer import Task1Analyzer
from src.analysis.engagement_analyzer import EngagementAnalyzer

def main():
    st.set_page_config(layout="wide")
    
    # Load data
    loader = Task1DataLoader()
    data = loader.prepare_task1_data()
    
    # Initialize analyzers
    task1_analyzer = Task1Analyzer(data)
    engagement_analyzer = EngagementAnalyzer(data['raw_data'])
    
    # Get analysis results
    handset_results = task1_analyzer.analyze_handsets()
    engagement_metrics = engagement_analyzer.calculate_engagement_metrics()
    app_engagement = engagement_analyzer.analyze_app_engagement()
    
    # Title
    st.title("TellCo Telecom Analysis - Visualizations")
    
    # 1. Handset Distribution
    st.header("Top 10 Handsets Distribution")
    fig_handsets = px.bar(
        handset_results['top_handsets'],
        x='handset',
        y='count',
        title='Top 10 Handsets by Usage'
    )
    fig_handsets.update_layout(height=500)
    st.plotly_chart(fig_handsets, use_container_width=True)
    
    # 2. Manufacturer Market Share
    st.header("Manufacturer Market Share")
    fig_manufacturers = px.pie(
        handset_results['top_manufacturers'],
        values='count',
        names='manufacturer',
        title='Market Share Distribution'
    )
    fig_manufacturers.update_layout(height=500)
    st.plotly_chart(fig_manufacturers, use_container_width=True)
    
    # 3. User Engagement Distribution
    st.header("User Engagement Patterns")
    fig_engagement = px.scatter(
        engagement_metrics,
        x='session_count',
        y='total_traffic',
        title='User Engagement Distribution'
    )
    fig_engagement.update_layout(height=500)
    st.plotly_chart(fig_engagement, use_container_width=True)
    
    # 4. Application Usage
    st.header("Application Usage Distribution")
    app_data = pd.DataFrame({
        'Application': app_engagement['app_totals'].keys(),
        'Traffic': app_engagement['app_totals'].values()
    })
    fig_apps = px.pie(
        app_data,
        values='Traffic',
        names='Application',
        title='Traffic Distribution by Application'
    )
    fig_apps.update_layout(height=500)
    st.plotly_chart(fig_apps, use_container_width=True)

if __name__ == "__main__":
    main() 