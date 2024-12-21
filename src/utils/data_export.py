"""Data export utilities."""
import pandas as pd
from pathlib import Path
from datetime import datetime

class DataExporter:
    """Class for exporting analysis results."""
    
    def __init__(self, output_dir="exports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def export_analysis_results(self, results, name):
        """Export analysis results to various formats."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Export to CSV
        csv_path = self.output_dir / f"{name}_{timestamp}.csv"
        if isinstance(results, pd.DataFrame):
            results.to_csv(csv_path, index=False)
        elif isinstance(results, dict):
            pd.DataFrame(results).to_csv(csv_path, index=False)
        
        # Export to Excel if it's a complex analysis
        if isinstance(results, dict) and len(results) > 1:
            excel_path = self.output_dir / f"{name}_{timestamp}.xlsx"
            with pd.ExcelWriter(excel_path) as writer:
                for sheet_name, data in results.items():
                    if isinstance(data, pd.DataFrame):
                        data.to_excel(writer, sheet_name=sheet_name)
        
        return {
            'csv_path': csv_path,
            'excel_path': excel_path if 'excel_path' in locals() else None
        } 