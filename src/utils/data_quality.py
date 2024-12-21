"""Data quality assessment module."""
import pandas as pd
import numpy as np
from typing import Dict, List

class DataQualityChecker:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        
    def check_completeness(self) -> Dict:
        """Check for missing values and completeness."""
        return {
            'missing_values': self.data.isnull().sum().to_dict(),
            'completeness_ratio': (1 - self.data.isnull().sum() / len(self.data)).to_dict()
        }
    
    def check_consistency(self) -> Dict:
        """Check data consistency and anomalies."""
        numeric_columns = self.data.select_dtypes(include=[np.number]).columns
        return {
            'outliers': {col: self._detect_outliers(self.data[col]) 
                        for col in numeric_columns},
            'value_ranges': {col: {'min': self.data[col].min(), 
                                 'max': self.data[col].max()}
                           for col in numeric_columns}
        }
    
    def generate_quality_report(self) -> Dict:
        """Generate comprehensive data quality report."""
        return {
            'completeness': self.check_completeness(),
            'consistency': self.check_consistency(),
            'record_count': len(self.data),
            'column_count': len(self.data.columns)
        } 