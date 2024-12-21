"""Report generation utilities for Task 1."""
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
        
        report = {
            "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "handset_analysis": {
                "top_handsets": handset_results['top_handsets'].to_dict('records'),
                "top_manufacturers": handset_results['top_manufacturers'].to_dict('records'),
                "top_handsets_per_manufacturer": {
                    mfr: data.to_dict('records')
                    for mfr, data in handset_results['top_handsets_per_manufacturer'].items()
                }
            }
        }
        
        # Save report
        report_path = self.output_dir / f"handset_analysis_{datetime.now().strftime('%Y%m%d')}.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=4)
        
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
                }
            }
        }
        
        # Save report
        report_path = self.output_dir / f"user_behavior_{datetime.now().strftime('%Y%m%d')}.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=4)
        
        return report_path 