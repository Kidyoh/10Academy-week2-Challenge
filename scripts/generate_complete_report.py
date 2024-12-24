"""Script to generate complete analysis report."""
import pandas as pd
from src.dashboard.task1_loader import Task1DataLoader
from src.analysis.task1_analyzer import Task1Analyzer
from src.utils.report_generator import ReportGenerator
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Load data
    loader = Task1DataLoader()
    data = loader.prepare_task1_data()
    
    # Initialize analyzer and report generator
    analyzer = Task1Analyzer(data)
    report_generator = ReportGenerator(analyzer)
    
    try:
        # Generate reports
        handset_report = report_generator.generate_handset_report()
        behavior_report = report_generator.generate_user_behavior_report()
        
        logger.info(f"Reports generated successfully:")
        logger.info(f"Handset analysis: {handset_report}")
        logger.info(f"User behavior analysis: {behavior_report}")
        
    except Exception as e:
        logger.error(f"Error generating reports: {str(e)}")
        raise

if __name__ == "__main__":
    main() 