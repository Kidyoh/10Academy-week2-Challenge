"""User engagement dashboard page."""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def render_engagement_page(data):
    st.title("User Engagement Analysis")
    
    try:
        engagement_metrics = data['engagement_metrics']
        
        # KPI Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Users",
                f"{len(engagement_metrics):,}"
            )
        with col2:
            st.metric(
                "Avg Session Duration",
                f"{engagement_metrics['session_duration'].mean()/60:.1f} hrs"
            )
        with col3:
            st.metric(
                "Avg Data Usage",
                f"{engagement_metrics['total_traffic'].mean()/1e9:.1f} GB"
            )
        with col4:
            active_users = len(engagement_metrics[engagement_metrics['total_traffic'] > 0])
            st.metric(
                "Active Users",
                f"{active_users:,}"
            )
        
        # Add filters
        st.sidebar.header("Filters")
        min_traffic = st.sidebar.slider(
            "Minimum Data Usage (GB)",
            0.0,
            engagement_metrics['total_traffic'].max()/1e9,
            0.0
        )
        
        filtered_data = engagement_metrics[
            engagement_metrics['total_traffic'] >= min_traffic * 1e9
        ]
        
        # Session Analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Session Duration Distribution")
            fig_sessions = px.histogram(
                filtered_data,
                x='session_duration',
                nbins=50,
                title="Distribution of Session Durations (mins)"
            )
            st.plotly_chart(fig_sessions, use_container_width=True)
        
        with col2:
            st.subheader("Data Usage Distribution")
            fig_data = px.histogram(
                filtered_data,
                x='total_traffic',
                nbins=50,
                title="Distribution of Data Usage (bytes)"
            )
            st.plotly_chart(fig_data, use_container_width=True)
        
        # User Segmentation
        st.subheader("User Segmentation Analysis")
        
        # Perform clustering
        from sklearn.preprocessing import StandardScaler
        from sklearn.cluster import KMeans
        
        # Prepare features for clustering
        features = ['session_duration', 'total_traffic']
        X = filtered_data[features].copy()
        
        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Perform clustering
        n_clusters = st.slider("Number of Clusters", 2, 5, 3)
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        filtered_data['Cluster'] = kmeans.fit_predict(X_scaled)
        
        # Plot clusters
        fig_clusters = px.scatter(
            filtered_data,
            x='session_duration',
            y='total_traffic',
            color='Cluster',
            title="User Segments by Session Duration and Data Usage",
            labels={
                'session_duration': 'Session Duration (mins)',
                'total_traffic': 'Data Usage (bytes)'
            }
        )
        st.plotly_chart(fig_clusters, use_container_width=True)
        
        # Cluster Statistics
        st.subheader("Cluster Statistics")
        cluster_stats = filtered_data.groupby('Cluster').agg({
            'session_duration': ['mean', 'count'],
            'total_traffic': 'mean'
        }).round(2)
        
        cluster_stats.columns = ['Avg Session Duration', 'User Count', 'Avg Data Usage']
        st.dataframe(cluster_stats)
        
    except Exception as e:
        st.error(f"Error in engagement analysis: {str(e)}")
        st.exception(e) 