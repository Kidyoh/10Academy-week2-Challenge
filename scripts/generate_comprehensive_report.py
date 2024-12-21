"""Script to generate comprehensive report for Tasks 1 and 2."""
import pandas as pd
from src.data.task1_loader import Task1DataLoader
from src.analysis.task1_analyzer import Task1Analyzer
from src.analysis.engagement_analyzer import EngagementAnalyzer
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_markdown_report(task1_results, engagement_results):
    """Generate comprehensive markdown report."""
    report = """# TellCo Telecom Analysis Report

## Task 1: User Overview Analysis

### 1.1 Handset Analysis
#### Top 10 Handsets
{}

#### Top 3 Manufacturers
{}

### 1.2 User Behavior Patterns
{}

## Task 2: User Engagement Analysis

### 2.1 Top Users Analysis
#### By Session Count
{}

#### By Duration
{}

#### By Total Traffic
{}

### 2.2 Clustering Analysis
{}

### 2.3 Application Usage
{}

### 2.4 Key Findings and Recommendations
1. Handset Distribution:
   - [Key findings about handset preferences]
   - [Recommendations for handset strategy]

2. User Engagement:
   - [Key findings about user engagement patterns]
   - [Recommendations for improving engagement]

3. Application Usage:
   - [Key findings about application preferences]
   - [Recommendations for application optimization]

4. User Segments:
   - [Description of identified user segments]
   - [Targeted recommendations for each segment]
""".format(
        pd.DataFrame(task1_results['top_handsets']).to_markdown(),
        pd.DataFrame(task1_results['top_manufacturers']).to_markdown(),
        "User behavior analysis results...",
        pd.DataFrame(engagement_results['top_users']['session_count']).to_markdown(),
        pd.DataFrame(engagement_results['top_users']['total_duration']).to_markdown(),
        pd.DataFrame(engagement_results['top_users']['total_traffic']).to_markdown(),
        "Clustering analysis results...",
        "Application usage analysis..."
    )
    
    return report

def main():
    # Create reports directory if it doesn't exist
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    
    # Load data
    loader = Task1DataLoader()
    data = loader.prepare_task1_data()
    
    # Task 1 Analysis
    task1_analyzer = Task1Analyzer(data)
    task1_results = task1_analyzer.analyze_handsets()
    
    # Task 2 Analysis
    engagement_analyzer = EngagementAnalyzer(data['raw_data'])
    engagement_metrics = engagement_analyzer.calculate_engagement_metrics()
    top_users = engagement_analyzer.get_top_users()
    clustered_data, cluster_stats = engagement_analyzer.cluster_users()
    app_engagement = engagement_analyzer.analyze_app_engagement()
    
    # Generate report
    report = generate_markdown_report(
        task1_results,
        {
            'top_users': top_users,
            'cluster_stats': cluster_stats,
            'app_engagement': app_engagement
        }
    )
    
    # Save report
    report_path = reports_dir / "comprehensive_analysis.md"
    with open(report_path, 'w') as f:
        f.write(report)
    
    logger.info(f"Comprehensive report generated: {report_path}")

if __name__ == "__main__":
    main() 