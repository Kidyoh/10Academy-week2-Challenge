"""Script to analyze user satisfaction."""
import pandas as pd
from src.dashboard.task1_loader import Task1DataLoader
from src.analysis.engagement_analyzer import EngagementAnalyzer
from src.analysis.experience_analyzer import ExperienceAnalyzer
from src.analysis.satisfaction_analyzer import SatisfactionAnalyzer
import logging
from dotenv import load_dotenv
import os

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    try:
        # Load environment variables
        load_dotenv()
        
        # Load data
        logger.info("Loading data...")
        loader = Task1DataLoader()
        data = loader.prepare_task1_data()
        
        # Calculate metrics
        logger.info("Calculating engagement metrics...")
        engagement_analyzer = EngagementAnalyzer(data['raw_data'])
        engagement_metrics = engagement_analyzer.calculate_engagement_metrics()
        
        logger.info("Calculating experience metrics...")
        experience_analyzer = ExperienceAnalyzer(data['raw_data'])
        experience_metrics = experience_analyzer.aggregate_user_experience()
        
        # Initialize satisfaction analyzer
        satisfaction_analyzer = SatisfactionAnalyzer(
            engagement_metrics,
            experience_metrics
        )
        
        # Calculate satisfaction scores
        logger.info("Analyzing customer satisfaction...")
        satisfaction_scores = satisfaction_analyzer.calculate_satisfaction_scores()
        
        # Get top satisfied customers
        top_satisfied = satisfaction_analyzer.get_top_satisfied_customers()
        print("\nTop 10 Satisfied Customers:")
        print(top_satisfied)
        
        # Save results
        logger.info("Saving analysis results...")
        file_paths = satisfaction_analyzer.save_results()
        
        # Try database export if configured
        connection_string = os.getenv('MYSQL_CONNECTION_STRING')
        if connection_string:
            logger.info("Attempting database export...")
            satisfaction_analyzer.export_to_database(connection_string)
        else:
            logger.info("No database connection configured. Results saved to CSV only.")
        
        logger.info("Analysis completed successfully")
        
    except Exception as e:
        logger.error(f"Error in satisfaction analysis: {str(e)}")
        raise

if __name__ == "__main__":
    main() 