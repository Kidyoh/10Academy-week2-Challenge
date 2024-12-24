"""Debug script for handset analysis."""
import pandas as pd
from src.dashboard.task1_loader import Task1DataLoader
from src.analysis.task1_analyzer import Task1Analyzer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Load data
    loader = Task1DataLoader()
    data = loader.prepare_task1_data()
    
    # Check handset_info data
    logger.info("Handset Info Data:")
    logger.info(f"Columns: {data['handset_info'].columns.tolist()}")
    logger.info(f"Sample data:\n{data['handset_info'].head()}")
    
    # Initialize analyzer
    analyzer = Task1Analyzer(data)
    
    # Get handset analysis results
    results = analyzer.analyze_handsets()
    
    # Check results
    logger.info("\nTop Handsets Results:")
    logger.info(f"Columns: {results['top_handsets'].columns.tolist()}")
    logger.info(f"Data:\n{results['top_handsets']}")
    
    # Save intermediate results for verification
    results['top_handsets'].to_csv('debug_top_handsets.csv', index=False)
    results['handset_data'].to_csv('debug_handset_data.csv', index=False)

if __name__ == "__main__":
    main() 