"""User satisfaction dashboard page."""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def calculate_satisfaction_scores(engagement_metrics, experience_metrics):
    """Calculate satisfaction scores from engagement and experience metrics."""
    # Normalize engagement metrics
    engagement_features = ['session_duration', 'total_traffic']
    engagement_scaler = StandardScaler()
    engagement_scores = engagement_scaler.fit_transform(engagement_metrics[engagement_features])
    engagement_scores = pd.DataFrame(engagement_scores, columns=['session_score', 'traffic_score'])
    
    # Normalize experience metrics
    experience_features = ['avg_throughput', 'avg_tcp_retrans', 'avg_rtt']
    experience_scaler = StandardScaler()
    experience_scores = experience_scaler.fit_transform(experience_metrics[experience_features])
    experience_scores = pd.DataFrame(experience_scores, columns=['throughput_score', 'tcp_score', 'rtt_score'])
    
    # Calculate final scores
    satisfaction_scores = pd.DataFrame()
    satisfaction_scores['msisdn'] = engagement_metrics['msisdn']
    satisfaction_scores['engagement_score'] = engagement_scores.mean(axis=1)
    satisfaction_scores['experience_score'] = experience_scores.mean(axis=1)
    satisfaction_scores['satisfaction_score'] = (
        satisfaction_scores['engagement_score'] + satisfaction_scores['experience_score']
    ) / 2
    
    return satisfaction_scores

def render_satisfaction_page(data):
    st.title("User Satisfaction Analysis")
    
    try:
        # Calculate satisfaction scores
        satisfaction_scores = calculate_satisfaction_scores(
            data['engagement_metrics'],
            data['experience_metrics']
        )
        
        # KPI Metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Average Satisfaction Score",
                f"{satisfaction_scores['satisfaction_score'].mean():.2f}"
            )
        with col2:
            st.metric(
                "Highly Satisfied Users",
                f"{len(satisfaction_scores[satisfaction_scores['satisfaction_score'] > 0.8]):,}"
            )
        with col3:
            st.metric(
                "Satisfaction Rate",
                f"{(satisfaction_scores['satisfaction_score'] > 0).mean()*100:.1f}%"
            )
        
        # Satisfaction Distribution
        st.subheader("Satisfaction Score Distribution")
        fig_dist = px.histogram(
            satisfaction_scores,
            x='satisfaction_score',
            nbins=50,
            title="Distribution of Satisfaction Scores"
        )
        st.plotly_chart(fig_dist, use_container_width=True)
        
        # Engagement vs Experience
        st.subheader("Engagement vs Experience Analysis")
        fig_scatter = px.scatter(
            satisfaction_scores,
            x='engagement_score',
            y='experience_score',
            color='satisfaction_score',
            title="Engagement vs Experience Scores",
            labels={
                'engagement_score': 'Engagement Score',
                'experience_score': 'Experience Score',
                'satisfaction_score': 'Satisfaction Score'
            }
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        # User Segments
        st.subheader("User Satisfaction Segments")
        
        # Perform clustering
        n_clusters = st.slider("Number of Satisfaction Clusters", 2, 5, 3)
        
        X = satisfaction_scores[['engagement_score', 'experience_score']]
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        satisfaction_scores['cluster'] = kmeans.fit_predict(X)
        
        # Show cluster statistics
        cluster_stats = satisfaction_scores.groupby('cluster').agg({
            'satisfaction_score': ['mean', 'count'],
            'engagement_score': 'mean',
            'experience_score': 'mean'
        }).round(3)
        
        st.write("Cluster Statistics:")
        st.dataframe(cluster_stats)
        
    except Exception as e:
        st.error(f"Error in satisfaction analysis: {str(e)}")
        st.exception(e) 