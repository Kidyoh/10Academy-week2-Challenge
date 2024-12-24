"""User Experience Analysis Dashboard Page."""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from src.analysis.task3_experience import ExperienceAnalyzer
from src.dashboard.data_loader import load_telco_data

def render_experience_page():
    st.title("User Experience Analysis")
    
    try:
        # Load data
        with st.spinner("Loading data..."):
            loader = load_telco_data()
            data = loader.load_data()
            analyzer = ExperienceAnalyzer(data)
            
        # Sidebar filters
        st.sidebar.header("Filters")
        handset_type = st.sidebar.multiselect(
            "Select Handset Types",
            options=data['Handset Type'].unique(),
            default=data['Handset Type'].unique()[:5]
        )
        
        # KPI Metrics Row
        col1, col2, col3 = st.columns(3)
        
        metrics = analyzer.calculate_experience_metrics()
        with col1:
            st.metric(
                "Average TCP Retransmission",
                f"{metrics['avg_tcp_retrans']:.2f} bytes",
                help="Average TCP retransmission volume"
            )
        with col2:
            st.metric(
                "Average RTT",
                f"{metrics['avg_rtt']:.2f} ms",
                help="Average Round Trip Time"
            )
        with col3:
            st.metric(
                "Average Throughput",
                f"{metrics['avg_throughput']:.2f} kbps",
                help="Average Bearer Throughput"
            )
        
        # TCP Retransmission Analysis
        st.subheader("TCP Retransmission Analysis")
        tcp_analysis = analyzer.analyze_tcp_retransmission(handset_types=handset_type)
        
        fig_tcp = px.box(
            tcp_analysis,
            x='Handset Type',
            y='TCP Retransmission Volume',
            title="TCP Retransmission Distribution by Handset"
        )
        st.plotly_chart(fig_tcp, use_container_width=True)
        
        # Throughput Analysis
        st.subheader("Throughput Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            throughput_dl = analyzer.analyze_throughput(
                direction='DL',
                handset_types=handset_type
            )
            fig_dl = px.box(
                throughput_dl,
                x='Handset Type',
                y='Throughput',
                title="Download Throughput by Handset"
            )
            st.plotly_chart(fig_dl, use_container_width=True)
            
        with col2:
            throughput_ul = analyzer.analyze_throughput(
                direction='UL',
                handset_types=handset_type
            )
            fig_ul = px.box(
                throughput_ul,
                x='Handset Type',
                y='Throughput',
                title="Upload Throughput by Handset"
            )
            st.plotly_chart(fig_ul, use_container_width=True)
        
        # RTT Analysis
        st.subheader("Round Trip Time (RTT) Analysis")
        rtt_analysis = analyzer.analyze_rtt(handset_types=handset_type)
        
        fig_rtt = px.scatter(
            rtt_analysis,
            x='Throughput',
            y='RTT',
            color='Handset Type',
            title="RTT vs Throughput by Handset Type"
        )
        st.plotly_chart(fig_rtt, use_container_width=True)
        
        # Experience Score Distribution
        st.subheader("Experience Score Distribution")
        experience_scores = analyzer.calculate_experience_scores()
        
        fig_scores = px.histogram(
            experience_scores,
            x='experience_score',
            nbins=50,
            title="Distribution of Experience Scores"
        )
        st.plotly_chart(fig_scores, use_container_width=True)
        
        # Show detailed statistics
        if st.checkbox("Show Detailed Statistics"):
            st.dataframe(analyzer.get_detailed_statistics())
        
    except Exception as e:
        st.error(f"Error in experience analysis: {str(e)}")
        st.exception(e)

if __name__ == "__main__":
    render_experience_page() 