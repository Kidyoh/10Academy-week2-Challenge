"""Task 1 specific dashboard components."""
import streamlit as st
import plotly.express as px
from src.utils.task1_visualization import (
    plot_top_handsets,
    plot_app_usage_distribution,
    plot_correlation_heatmap,
    plot_pca_explained_variance
)

class Task1Dashboard:
    """Dashboard class for Task 1 visualizations."""
    
    def __init__(self, analyzer):
        self.analyzer = analyzer
    
    def render_handset_section(self):
        """Render handset analysis section."""
        st.header("Handset Analysis")
        
        # Top handsets
        top_handsets = self.analyzer.handset_analyzer.get_top_handsets()
        st.plotly_chart(plot_top_handsets(top_handsets))
        
        # Top manufacturers
        top_manufacturers = self.analyzer.handset_analyzer.get_top_manufacturers()
        st.plotly_chart(plot_top_handsets(
            top_manufacturers, 
            title="Top Handset Manufacturers"
        ))
        
        # Top handsets per manufacturer
        selected_manufacturer = st.selectbox(
            "Select Manufacturer",
            top_manufacturers['manufacturer'].tolist()
        )
        if selected_manufacturer:
            top_models = self.analyzer.handset_analyzer.get_top_handsets_per_manufacturer(
                selected_manufacturer
            )
            st.plotly_chart(plot_top_handsets(
                top_models,
                title=f"Top Handsets for {selected_manufacturer}"
            ))
    
    def render_behavior_section(self):
        """Render user behavior analysis section."""
        st.header("User Behavior Analysis")
        
        # Basic statistics
        st.subheader("Basic Statistics")
        stats = self.analyzer.get_basic_statistics()
        st.dataframe(stats)
        
        # Application usage distribution
        st.subheader("Application Usage Distribution")
        user_metrics = self.analyzer.behavior_analyzer.aggregate_user_metrics()
        st.plotly_chart(plot_app_usage_distribution(
            user_metrics,
            self.analyzer.behavior_analyzer.app_columns
        ))
        
        # Correlation matrix
        st.subheader("Application Usage Correlation")
        correlation = self.analyzer.behavior_analyzer.compute_correlation_matrix(user_metrics)
        st.plotly_chart(plot_correlation_heatmap(correlation))
        
        # PCA results
        st.subheader("Principal Component Analysis")
        pca_results = self.analyzer.behavior_analyzer.perform_pca(user_metrics)
        st.plotly_chart(plot_pca_explained_variance(pca_results['explained_variance'])) 