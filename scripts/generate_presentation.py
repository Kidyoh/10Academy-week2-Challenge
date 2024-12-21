"""Script to generate interim presentation."""
import pandas as pd
import traceback
from src.data.task1_loader import Task1DataLoader
from src.analysis.task1_analyzer import Task1Analyzer
from src.analysis.engagement_analyzer import EngagementAnalyzer
from src.utils.presentation_generator import PresentationGenerator
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        logger.info("Starting data loading process...")
        # Load and analyze data
        loader = Task1DataLoader()
        data = loader.prepare_task1_data()
        
        logger.info("Starting Task 1 Analysis...")
        # Task 1 Analysis
        task1_analyzer = Task1Analyzer(data)
        handset_results = task1_analyzer.analyze_handsets()
        logger.info("Task 1 Analysis completed")
        
        logger.info("Starting Task 2 Analysis...")
        # Task 2 Analysis
        engagement_analyzer = EngagementAnalyzer(data['raw_data'])
        engagement_metrics = engagement_analyzer.calculate_engagement_metrics()
        top_users = engagement_analyzer.get_top_users()
        clustered_data, cluster_stats = engagement_analyzer.cluster_users()
        app_engagement = engagement_analyzer.analyze_app_engagement()
        logger.info("Task 2 Analysis completed")
        
        logger.info("Generating presentation...")
        # Generate presentation
        presentation = PresentationGenerator()
        presentation.generate_presentation(
            {'top_handsets': handset_results['top_handsets'],
             'top_manufacturers': handset_results['top_manufacturers']},
            {'engagement_metrics': engagement_metrics,
             'top_users': top_users,
             'cluster_stats': cluster_stats,
             'app_engagement': app_engagement}
        )
        logger.info("Presentation generation completed successfully")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        logger.error(traceback.format_exc())
        raise

if __name__ == "__main__":
    main() 