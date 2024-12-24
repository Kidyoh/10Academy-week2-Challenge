"""Script to generate all visualizations for the presentation."""
import pandas as pd
from src.dashboard.task1_loader import Task1DataLoader
from src.analysis.task1_analyzer import Task1Analyzer
from src.analysis.engagement_analyzer import EngagementAnalyzer
from src.utils.visualization_helper import save_visualizations
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Load data
    loader = Task1DataLoader()
    data = loader.prepare_task1_data()
    
    # Task 1 Analysis
    task1_analyzer = Task1Analyzer(data)
    handset_results = task1_analyzer.analyze_handsets()
    
    # Task 2 Analysis
    engagement_analyzer = EngagementAnalyzer(data['raw_data'])
    engagement_metrics = engagement_analyzer.calculate_engagement_metrics()
    top_users = engagement_analyzer.get_top_users()
    clustered_data, cluster_stats = engagement_analyzer.cluster_users()
    app_engagement = engagement_analyzer.analyze_app_engagement()
    
    # Save visualizations
    viz_paths = save_visualizations({
        'top_handsets': handset_results['top_handsets'],
        'top_manufacturers': handset_results['top_manufacturers'],
        'engagement_metrics': engagement_metrics,
        'app_engagement': app_engagement,
        'cluster_stats': cluster_stats
    })
    
    logger.info("Visualizations saved successfully")
    for name, path in viz_paths.items():
        logger.info(f"{name}: {path}")

if __name__ == "__main__":
    main() 