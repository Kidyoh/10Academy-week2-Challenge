"""Report generation utilities."""
import pandas as pd
from pathlib import Path
import json
from datetime import datetime

class ReportGenerator:
    """Class for generating analysis reports."""
    
    def __init__(self, analyzer, output_dir="reports"):
        self.analyzer = analyzer
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_handset_report(self):
        """Generate handset analysis report."""
        handset_results = self.analyzer.analyze_handsets()
        
        # Generate manufacturer analysis
        manufacturer_analysis = {}
        for _, row in handset_results['handset_data'].groupby('Handset Manufacturer'):
            top_handsets = (row['handset']
                          .value_counts()
                          .head(5)
                          .to_dict())
            manufacturer_analysis[row['Handset Manufacturer'].iloc[0]] = top_handsets
        
        report = {
            "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "handset_analysis": {
                "top_handsets": handset_results['top_handsets'].to_dict('records'),
                "top_manufacturers": handset_results['top_manufacturers'].to_dict('records'),
                "manufacturer_analysis": manufacturer_analysis
            }
        }
        
        # Save report
        report_path = self.output_dir / f"handset_analysis_{datetime.now().strftime('%Y%m%d')}.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=4)
        
        # Generate markdown report
        markdown_report = self._generate_markdown_report(report)
        markdown_path = self.output_dir / f"handset_analysis_{datetime.now().strftime('%Y%m%d')}.md"
        with open(markdown_path, 'w') as f:
            f.write(markdown_report)
        
        return report_path
    
    def generate_user_behavior_report(self):
        """Generate user behavior analysis report."""
        behavior_results = self.analyzer.analyze_user_behavior()
        
        # Convert results to more readable format
        decile_stats = behavior_results['decile_stats'].round(2)
        
        report = {
            "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user_behavior_analysis": {
                "decile_statistics": decile_stats.to_dict(),
                "summary_statistics": {
                    "total_users": len(behavior_results['user_metrics']),
                    "total_sessions": behavior_results['user_metrics']['total_sessions'].sum(),
                    "average_session_duration": behavior_results['user_metrics']['session_duration'].mean()
                },
                "application_usage": {
                    app: {
                        "total_bytes": behavior_results['user_metrics'][f'{app}_total_bytes'].sum(),
                        "average_bytes": behavior_results['user_metrics'][f'{app}_total_bytes'].mean()
                    }
                    for app in ['social_media', 'google', 'email', 'youtube', 'netflix', 'gaming']
                }
            }
        }
        
        # Save report
        report_path = self.output_dir / f"user_behavior_{datetime.now().strftime('%Y%m%d')}.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=4)
        
        return report_path
    
    def _generate_markdown_report(self, report_data):
        """Generate markdown formatted report."""
        markdown = f"""# TellCo Analysis Report
Generated on: {report_data['analysis_date']}

## 1. Handset Analysis

### 1.1 Top 10 Handsets
"""
        
        # Add top handsets
        for handset in report_data['handset_analysis']['top_handsets']:
            markdown += f"- {handset['handset']}: {handset['count']} users\n"
        
        markdown += "\n### 1.2 Top Manufacturers\n"
        
        # Add manufacturer information
        for mfr in report_data['handset_analysis']['top_manufacturers']:
            markdown += f"- {mfr['manufacturer']}: {mfr['count']} users\n"
        
        markdown += "\n### 1.3 Top Handsets by Manufacturer\n"
        
        # Add manufacturer-specific analysis
        for mfr, handsets in report_data['handset_analysis']['manufacturer_analysis'].items():
            markdown += f"\n#### {mfr}\n"
            for handset, count in handsets.items():
                markdown += f"- {handset}: {count} users\n"
        
        return markdown