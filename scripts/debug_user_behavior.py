"""Debug script for user behavior analysis."""
import pandas as pd
from src.data.task1_loader import Task1DataLoader
from src.analysis.task1_analyzer import Task1Analyzer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Load data
    loader = Task1DataLoader()
    data = loader.prepare_task1_data()
    
    # Check app_usage data
    logger.info("App Usage Data:")
    logger.info(f"Columns: {data['app_usage'].columns.tolist()}")
    logger.info(f"Sample data:\n{data['app_usage'].head()}")
    
    # Initialize analyzer
    analyzer = Task1Analyzer(data)
    
    # Get behavior analysis results
    results = analyzer.analyze_user_behavior()
    
    # Check results
    logger.info("\nUser Metrics Results:")
    logger.info(f"Columns: {results['user_metrics'].columns.tolist()}")
    logger.info("\nDecile Stats Results:")
    logger.info(f"Data:\n{results['decile_stats']}")
    
    # Save intermediate results for verification
    results['user_metrics'].to_csv('debug_user_metrics.csv', index=False)
    results['decile_stats'].to_csv('debug_decile_stats.csv')

if __name__ == "__main__":
    main() 