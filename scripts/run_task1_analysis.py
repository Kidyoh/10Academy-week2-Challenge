"""Script to run Task 1 analysis."""
import streamlit as st
from src.data.task1_loader import Task1DataLoader
from src.analysis.task1_analyzer import Task1Analyzer
from src.utils.task1_validation import Task1Validator
from src.dashboard.components.task1_visuals import (
    render_handset_analysis,
    render_user_behavior_analysis
)
from src.utils.logging_config import setup_logging

def main():

    logger = setup_logging()
    
    # Load and prepare data
    loader = Task1DataLoader()
    data = loader.prepare_task1_data()
    
    # Validate data
    validator = Task1Validator(data['raw_data'])
    validation_results = validator.validate_task1_requirements()
    
    # Initialize analyzer
    analyzer = Task1Analyzer(data)
    
    # Streamlit dashboard
    st.title("TellCo User Analysis - Task 1")
    
    analysis_type = st.sidebar.radio(
        "Select Analysis",
        ["Handset Analysis", "User Behavior Analysis"]
    )
    
    if analysis_type == "Handset Analysis":
        render_handset_analysis(analyzer)
    else:
        render_user_behavior_analysis(analyzer)

if __name__ == "__main__":
    main() 