"""User Engagement Analysis Dashboard Page."""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from src.analysis.engagement_analyzer import EngagementAnalyzer
from src.dashboard.data_loader import load_telco_data

def render_engagement_page():
    st.title("User Engagement Analysis")
    
    try:
        # Load data
        with st.spinner("Loading data..."):
            loader = load_telco_data()
            data = loader.load_data()
            analyzer = EngagementAnalyzer(data)
            
        # Calculate metrics
        engagement_metrics = analyzer.calculate_engagement_metrics()
        
        # Sidebar filters
        st.sidebar.header("Filters")
        metric_options = {
            'Session Count': 'session_count',
            'Total Duration': 'total_duration',
            'Total Traffic': 'total_traffic'
        }
        selected_metric = st.sidebar.selectbox(
            "Select Metric for Analysis",
            options=list(metric_options.keys())
        )
        metric_col = metric_options[selected_metric]
        
        # KPI Metrics Row
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Average Sessions per User",
                f"{engagement_metrics['session_count'].mean():.0f}",
                help="Average number of sessions per user"
            )
        with col2:
            st.metric(
                "Average Duration",
                f"{(engagement_metrics['total_duration'] / 1000 / 60).mean():.0f} min",
                help="Average session duration in minutes"
            )
        with col3:
            st.metric(
                "Average Traffic",
                f"{(engagement_metrics['total_traffic'] / 1e6).mean():.1f} MB",
                help="Average total traffic per user"
            )
        
        # Distribution Analysis
        st.subheader(f"{selected_metric} Distribution")
        fig_dist = px.histogram(
            engagement_metrics,
            x=metric_col,
            nbins=50,
            title=f"Distribution of {selected_metric}"
        )
        st.plotly_chart(fig_dist, use_container_width=True)
        
        # Top Users Analysis
        st.subheader("Top Users Analysis")
        top_users = analyzer.get_top_users()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_top_sessions = px.bar(
                top_users['session_count'],
                x='msisdn',
                y='session_count',
                title="Top Users by Session Count"
            )
            st.plotly_chart(fig_top_sessions, use_container_width=True)
            
        with col2:
            fig_top_traffic = px.bar(
                top_users['total_traffic'],
                x='msisdn',
                y='total_traffic',
                title="Top Users by Total Traffic"
            )
            st.plotly_chart(fig_top_traffic, use_container_width=True)
        
        # Correlation Analysis
        st.subheader("Metric Correlations")
        correlation_matrix = engagement_metrics[['session_count', 'total_duration', 'total_traffic']].corr()
        
        fig_corr = go.Figure(data=go.Heatmap(
            z=correlation_matrix,
            x=correlation_matrix.columns,
            y=correlation_matrix.columns,
            colorscale='RdBu',
            zmin=-1,
            zmax=1
        ))
        fig_corr.update_layout(title="Correlation Matrix of Engagement Metrics")
        st.plotly_chart(fig_corr, use_container_width=True)
        
        # Show detailed statistics
        if st.checkbox("Show Detailed Statistics"):
            st.dataframe(engagement_metrics.describe())
        
    except Exception as e:
        st.error(f"Error in engagement analysis: {str(e)}")
        st.exception(e)

if __name__ == "__main__":
    render_engagement_page() 