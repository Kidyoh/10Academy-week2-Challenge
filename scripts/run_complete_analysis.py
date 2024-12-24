"""Script to run complete analysis with all components."""
import streamlit as st
import pandas as pd
from src.dashboard.task1_loader import Task1DataLoader
from src.analysis.task1_analyzer import Task1Analyzer
from src.utils.task1_validation import Task1Validator
from src.utils.report_generator import ReportGenerator
from src.utils.data_export import DataExporter
from src.dashboard.components.task1_visuals import (
    render_handset_analysis,
    render_user_behavior_analysis
)
from src.utils.logging_config import setup_logging
import traceback

def main():
    try:
        # Setup logging
        logger = setup_logging()
        
        # Initialize Streamlit interface
        st.title("TellCo Telecom Analysis - Complete Analysis")
        
        # Load and validate data
        with st.spinner("Loading and validating data..."):
            try:
                loader = Task1DataLoader()
                data = loader.prepare_task1_data()
                validator = Task1Validator(data['raw_data'])
                validation_results = validator.validate_task1_requirements()
                
                if not all(all(results.values()) for results in validation_results.values()):
                    st.warning("Some data validation checks failed. Results may be incomplete.")
                    
            except Exception as e:
                st.error("Error loading data. Please check the data files and try again.")
                st.exception(e)
                return
        
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
            render_handset_analysis(analyzer)
        
        elif analysis_type == "User Behavior":
            render_user_behavior_analysis(analyzer)
        
        else:  # Complete Report
            st.header("Complete Analysis Report")
            
            if st.button("Generate Complete Report"):
                with st.spinner("Generating report..."):
                    try:
                        handset_report = report_generator.generate_handset_report()
                        behavior_report = report_generator.generate_user_behavior_report()
                        st.success(f"Reports generated:\n{handset_report}\n{behavior_report}")
                    except Exception as e:
                        st.error("Error generating reports.")
                        st.exception(e)
        
    except Exception as e:
        st.error("An unexpected error occurred.")
        st.exception(e)
        logger.error(f"Unexpected error: {str(e)}")
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    main() 