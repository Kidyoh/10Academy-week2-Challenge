"""Script to run complete analysis with all components."""
import streamlit as st
from src.data.task1_loader import Task1DataLoader
from src.analysis.task1_analyzer import Task1Analyzer
from src.utils.task1_validation import Task1Validator
from src.utils.report_generator import ReportGenerator
from src.utils.data_export import DataExporter
from src.utils.enhanced_visualization import (
    create_handset_treemap,
    create_usage_patterns_heatmap,
    create_usage_time_distribution
)
from src.utils.logging_config import setup_logging

def main():
    # Setup logging
    logger = setup_logging()
    
    # Initialize Streamlit interface
    st.title("TellCo Telecom Analysis - Complete Analysis")
    
    # Load and validate data
    with st.spinner("Loading and validating data..."):
        loader = Task1DataLoader()
        data = loader.prepare_task1_data()
        validator = Task1Validator(data['raw_data'])
        validation_results = validator.validate_task1_requirements()
    
    # Initialize analyzers and utilities
    analyzer = Task1Analyzer(data)
    report_generator = ReportGenerator(analyzer)
    data_exporter = DataExporter()
    
    # Sidebar for navigation
    analysis_type = st.sidebar.selectbox(
        "Select Analysis Type",
        ["Handset Analysis", "User Behavior", "Complete Report"]
    )
    
    if analysis_type == "Handset Analysis":
        st.header("Handset Analysis")
        
        # Get and display handset analysis
        handset_results = analyzer.analyze_handsets()
        
        # Display treemap
        st.plotly_chart(create_handset_treemap(handset_results['top_handsets']))
        
        # Export option
        if st.button("Export Handset Analysis"):
            export_paths = data_exporter.export_analysis_results(
                handset_results,
                "handset_analysis"
            )
            st.success(f"Analysis exported to {export_paths['csv_path']}")
    
    elif analysis_type == "User Behavior":
        st.header("User Behavior Analysis")
        
        # Get and display behavior analysis
        behavior_results = analyzer.analyze_user_behavior()
        
        # Display usage patterns
        st.plotly_chart(create_usage_patterns_heatmap(behavior_results['user_metrics']))
        st.plotly_chart(create_usage_time_distribution(behavior_results['user_metrics']))
        
        # Export option
        if st.button("Export Behavior Analysis"):
            export_paths = data_exporter.export_analysis_results(
                behavior_results,
                "user_behavior"
            )
            st.success(f"Analysis exported to {export_paths['csv_path']}")
    
    else:  # Complete Report
        st.header("Complete Analysis Report")
        
        # Generate complete report
        if st.button("Generate Complete Report"):
            with st.spinner("Generating report..."):
                handset_report = report_generator.generate_handset_report()
                behavior_report = report_generator.generate_user_behavior_report()
                st.success(f"Reports generated:\n{handset_report}\n{behavior_report}")

if __name__ == "__main__":
    main() 