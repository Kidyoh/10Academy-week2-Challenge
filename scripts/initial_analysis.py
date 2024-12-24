"""Script to run initial data analysis."""
import pandas as pd
from src.dashboard.data_loader import Task1DataLoader
from src.analysis.task1_analyzer import Task1Analyzer

def main():
    # Load data
    loader = Task1DataLoader()
    data = loader.prepare_task1_data()
    
    # Basic info about the dataset
    print("\nDataset Information:")
    print(data['raw_data'].info())
    
    # Check missing values
    print("\nMissing Values:")
    print(data['raw_data'].isnull().sum())
    
    # Initialize analyzer
    analyzer = Task1Analyzer(data)
    
    # Get handset analysis
    handset_results = analyzer.analyze_handsets()
    
    # Print top handsets and manufacturers
    print("\nTop 10 Handsets:")
    print(handset_results['top_handsets'])
    
    print("\nTop 3 Manufacturers:")
    print(handset_results['top_manufacturers'])

if __name__ == "__main__":
    main() 