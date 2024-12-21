"""Data validation utilities."""
import pandas as pd
import numpy as np
from typing import List, Dict, Union

class DataValidator:
    """Class for validating data quality and structure."""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.validation_results = {}
    
    def validate_required_columns(self, required_columns: List[str]) -> Dict[str, bool]:
        """Validate presence of required columns."""
        results = {}
        for column in required_columns:
            results[column] = column in self.data.columns
        self.validation_results['required_columns'] = results
        return results
    
    def validate_data_types(self, expected_types: Dict[str, str]) -> Dict[str, bool]:
        """Validate data types of columns."""
        results = {}
        for column, expected_type in expected_types.items():
            if column in self.data.columns:
                actual_type = str(self.data[column].dtype)
                results[column] = actual_type == expected_type
        self.validation_results['data_types'] = results
        return results
    
    def validate_value_ranges(self, 
                            ranges: Dict[str, Dict[str, Union[float, int]]]) -> Dict[str, bool]:
        """Validate value ranges for numeric columns."""
        results = {}
        for column, range_values in ranges.items():
            if column in self.data.columns:
                min_val = range_values.get('min')
                max_val = range_values.get('max')
                values_in_range = True
                
                if min_val is not None:
                    values_in_range &= self.data[column].min() >= min_val
                if max_val is not None:
                    values_in_range &= self.data[column].max() <= max_val
                    
                results[column] = values_in_range
        self.validation_results['value_ranges'] = results
        return results
    
    def get_validation_summary(self) -> Dict[str, Dict]:
        """Get summary of all validation results."""
        return self.validation_results 