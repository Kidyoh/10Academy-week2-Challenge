"""User Satisfaction Analysis Dashboard Page."""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from satisfaction_analyzer import SatisfactionAnalyzer
from engagement_analyzer import EngagementAnalyzer
from task3_experience import ExperienceAnalyzer
from data_loader import load_telco_data

def render_satisfaction_page():
    st.title("User Satisfaction Analysis")
    
    try:
        # Load data
        with st.spinner("Loading data..."):
            loader = load_telco_data()
            data = loader.load_data()
            
            # Initialize analyzers
            engagement_analyzer = EngagementAnalyzer(data)
            experience_analyzer = ExperienceAnalyzer(data)
            
            # Get metrics
            engagement_metrics = engagement_analyzer.calculate_engagement_metrics()
            
            # Get experience metrics and transform to DataFrame
            experience_scores = experience_analyzer.calculate_experience_scores()
            experience_metrics = pd.DataFrame({
                'msisdn': data['MSISDN/Number'],
                'avg_tcp_retrans': (
                    data['TCP DL Retrans. Vol (Bytes)'] + 
                    data['TCP UL Retrans. Vol (Bytes)']
                ) / 2,
                'avg_rtt': (
                    data['Avg RTT DL (ms)'] + 
                    data['Avg RTT UL (ms)']
                ) / 2,
                'avg_throughput': (
                    data['Avg Bearer TP DL (kbps)'] + 
                    data['Avg Bearer TP UL (kbps)']
                ) / 2
            }).groupby('msisdn').mean().reset_index()
            
            # Initialize satisfaction analyzer
            satisfaction_analyzer = SatisfactionAnalyzer(engagement_metrics, experience_metrics)
            satisfaction_scores = satisfaction_analyzer.calculate_satisfaction_scores()
        
        # Sidebar filters
        st.sidebar.header("Filters")
        score_type = st.sidebar.selectbox(
            "Select Score Type",
            options=['Satisfaction Score', 'Engagement Score', 'Experience Score']
        )
        score_col = score_type.lower().replace(' ', '_')
        
        # KPI Metrics Row
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Average Satisfaction Score",
                f"{satisfaction_scores['satisfaction_score'].mean():.2f}",
                help="Overall satisfaction score (0-1)"
            )
        with col2:
            st.metric(
                "Average Engagement Score",
                f"{satisfaction_scores['engagement_score'].mean():.2f}",
                help="User engagement score (0-1)"
            )
        with col3:
            st.metric(
                "Average Experience Score",
                f"{satisfaction_scores['experience_score'].mean():.2f}",
                help="User experience score (0-1)"
            )
        
        # Score Distribution
        st.subheader(f"{score_type} Distribution")
        fig_dist = px.histogram(
            satisfaction_scores,
            x=score_col,
            nbins=50,
            title=f"Distribution of {score_type}"
        )
        st.plotly_chart(fig_dist, use_container_width=True)
        
        # Score Correlations
        st.subheader("Score Correlations")
        col1, col2 = st.columns(2)
        
        with col1:
            # Try to create scatter plot with trendline if statsmodels is available
            try:
                import statsmodels.api as sm
                trendline = "ols"
            except ImportError:
                trendline = None
                
            fig_eng_exp = px.scatter(
                satisfaction_scores,
                x='engagement_score',
                y='experience_score',
                title="Engagement vs Experience Scores",
                trendline=trendline
            )
            st.plotly_chart(fig_eng_exp, use_container_width=True)
        
        with col2:
            correlation_matrix = satisfaction_scores[['satisfaction_score', 'engagement_score', 'experience_score']].corr()
            fig_corr = go.Figure(data=go.Heatmap(
                z=correlation_matrix,
                x=correlation_matrix.columns,
                y=correlation_matrix.columns,
                colorscale='RdBu',
                zmin=-1,
                zmax=1
            ))
            fig_corr.update_layout(title="Correlation Matrix of Scores")
            st.plotly_chart(fig_corr, use_container_width=True)
        
        # User Segments
        st.subheader("User Segments")
        satisfaction_scores['engagement_level'] = pd.qcut(
            satisfaction_scores['engagement_score'],
            q=3,
            labels=['Low', 'Medium', 'High']
        )
        satisfaction_scores['experience_level'] = pd.qcut(
            satisfaction_scores['experience_score'],
            q=3,
            labels=['Low', 'Medium', 'High']
        )
        
        segment_matrix = pd.crosstab(
            satisfaction_scores['engagement_level'],
            satisfaction_scores['experience_level']
        )
        
        fig_segments = px.imshow(
            segment_matrix,
            title="User Segments Matrix",
            labels=dict(x="Experience Level", y="Engagement Level", color="Count")
        )
        st.plotly_chart(fig_segments, use_container_width=True)
        
        # Show detailed statistics
        if st.checkbox("Show Detailed Statistics"):
            st.dataframe(satisfaction_scores.describe())
        
    except Exception as e:
        st.error(f"Error in satisfaction analysis: {str(e)}")
        st.exception(e)

if __name__ == "__main__":
    render_satisfaction_page() 