"""Script to run engagement analysis."""
import pandas as pd
from src.dashboard.task1_loader import Task1DataLoader
from src.analysis.engagement_analyzer import EngagementAnalyzer
from src.utils.engagement_visualization import (
    plot_top_users,
    plot_cluster_analysis,
    plot_app_usage,
    plot_elbow_curve
)
import streamlit as st

def main():
    # Load data
    loader = Task1DataLoader()
    data = loader.prepare_task1_data()
    
    # Initialize analyzer
    analyzer = EngagementAnalyzer(data['raw_data'])
    
    # Calculate engagement metrics
    metrics = analyzer.calculate_engagement_metrics()
    
    # Get top users
    top_users = analyzer.get_top_users()
    
    # Perform clustering
    clustered_data, cluster_stats = analyzer.cluster_users()
    
    # Analyze app engagement
    app_engagement = analyzer.analyze_app_engagement()
    
    # Find optimal k
    elbow_data = analyzer.find_optimal_k()
    
    # Create visualizations
    st.title("User Engagement Analysis")
    
    # Top Users Section
    st.header("Top Users Analysis")
    for metric, fig in plot_top_users(top_users).items():
        st.plotly_chart(fig)
    
    # Clustering Analysis
    st.header("User Clustering Analysis")
    st.plotly_chart(plot_cluster_analysis(cluster_stats))
    
    # Application Usage
    st.header("Application Usage Analysis")
    st.plotly_chart(plot_app_usage(app_engagement['app_totals']))
    
    # Elbow Analysis
    st.header("Optimal Cluster Analysis")
    st.plotly_chart(plot_elbow_curve(elbow_data['k_values'], elbow_data['inertias']))

if __name__ == "__main__":
    main() 