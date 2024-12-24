"""Script to analyze user experience metrics."""
import pandas as pd
import numpy as np
from src.dashboard.task1_loader import Task1DataLoader
from src.dashboard.experience_analyzer import ExperienceAnalyzer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        # Load data
        logger.info("Loading data...")
        loader = Task1DataLoader()
        data = loader.prepare_task1_data()
        
        # Initialize experience analyzer
        analyzer = ExperienceAnalyzer(data['raw_data'])
        
        # Task 3.1: Aggregate per-customer metrics
        logger.info("Aggregating user experience metrics...")
        experience_metrics = analyzer.aggregate_user_experience()
        print("\nTask 3.1 - Aggregated User Experience Metrics:")
        print(experience_metrics.head())
        
        # Task 3.2: Get metric distributions
        logger.info("Analyzing metric distributions...")
        distributions = analyzer.get_metric_distributions()
        
        print("\nTask 3.2 - Top 10 Values:")
        for metric, values in distributions.items():
            print(f"\n{metric.upper()} Distribution:")
            print("\nTop 10 Values:")
            print(values['top_10'])
            print("\nBottom 10 Values:")
            print(values['bottom_10'])
            print("\nMost Frequent Values:")
            print(values['most_frequent'])
        
        # Task 3.3: Analyze throughput and TCP by handset
        logger.info("Analyzing metrics by handset...")
        throughput_by_handset = analyzer.analyze_throughput_by_handset()
        tcp_by_handset = analyzer.analyze_tcp_by_handset()
        
        print("\nTask 3.3 - Throughput by Handset Type:")
        print(throughput_by_handset)
        print("\nTCP Retransmission by Handset Type:")
        print(tcp_by_handset)
        
        # Task 3.4: Cluster users
        logger.info("Performing user clustering...")
        clustered_data, cluster_stats = analyzer.cluster_users()
        
        print("\nTask 3.4 - User Experience Clusters:")
        print("\nCluster Statistics:")
        print(cluster_stats)
        
        # Save results
        logger.info("Saving results...")
        experience_metrics.to_csv('data/processed/user_experience_metrics.csv', index=False)
        throughput_by_handset.to_csv('data/processed/throughput_by_handset.csv')
        tcp_by_handset.to_csv('data/processed/tcp_by_handset.csv')
        cluster_stats.to_csv('data/processed/experience_clusters.csv')
        
        logger.info("Analysis completed successfully")
        
    except Exception as e:
        logger.error(f"Error in experience analysis: {str(e)}")
        raise

if __name__ == "__main__":
    main() 