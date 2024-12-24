"""User experience dashboard page."""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from src.analysis.experience_analyzer import ExperienceAnalyzer
from src.dashboard.data_preparation import prepare_experience_metrics, prepare_handset_metrics

def render_experience_page(data):
    st.title("User Experience Analysis")
    
    try:
        # Get metrics
        experience_metrics = prepare_experience_metrics(data['raw_data'])
        handset_metrics = prepare_handset_metrics(data['raw_data'])
        
        # KPI Metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Average TCP Retransmission",
                f"{experience_metrics['avg_tcp_retrans'].mean():.2f} bytes"
            )
        with col2:
            st.metric(
                "Average RTT",
                f"{experience_metrics['avg_rtt'].mean():.2f} ms"
            )
        with col3:
            st.metric(
                "Average Throughput",
                f"{experience_metrics['avg_throughput'].mean():.2f} kbps"
            )
        
        # Throughput Analysis
        st.subheader("Throughput Analysis by Handset")
        
        fig_throughput = px.bar(
            handset_metrics,
            x='handset_type',
            y='avg_throughput',
            title="Average Throughput by Handset Type",
            labels={
                'handset_type': 'Handset Type',
                'avg_throughput': 'Average Throughput (kbps)'
            }
        )
        st.plotly_chart(fig_throughput, use_container_width=True)
        
        # TCP Retransmission Analysis
        st.subheader("TCP Retransmission Analysis")
        
        fig_tcp = px.bar(
            handset_metrics,
            x='handset_type',
            y='avg_tcp_retrans',
            title="TCP Retransmission by Handset Type",
            labels={
                'handset_type': 'Handset Type',
                'avg_tcp_retrans': 'Average TCP Retransmission (bytes)'
            }
        )
        st.plotly_chart(fig_tcp, use_container_width=True)
        
        # Add more visualizations and analysis as needed
        
    except Exception as e:
        st.error(f"Error in experience analysis: {str(e)}")
        st.exception(e)