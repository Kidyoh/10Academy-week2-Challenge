"""Script to verify handset analysis."""
import pandas as pd
from src.data.task1_loader import Task1DataLoader
from src.analysis.task1_analyzer import Task1Analyzer

def main():
    # Load data
    loader = Task1DataLoader()
    data = loader.prepare_task1_data()
    
    # Initialize analyzer
    analyzer = Task1Analyzer(data)
    
    # Get handset analysis results
    results = analyzer.analyze_handsets()
    
    # Print results
    print("\nTop 10 Handsets:")
    print(results['top_handsets'])
    
    print("\nTop 3 Manufacturers:")
    print(results['top_manufacturers'])
    
    # Save results to CSV for verification
    results['top_handsets'].to_csv('reports/data/top_handsets.csv', index=False)
    results['top_manufacturers'].to_csv('reports/data/top_manufacturers.csv', index=False)

if __name__ == "__main__":
    main() 