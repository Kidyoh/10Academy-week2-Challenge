"""Data validation for Task 1."""
from src.utils.data_validation import DataValidator

class Task1Validator(DataValidator):
    """Validator specific to Task 1 requirements."""
    
    def validate_task1_requirements(self):
        """Validate all requirements for Task 1."""
        # Required columns for Task 1
        required_columns = [
            'MSISDN/Number',
            'Handset Type',
            'Handset Manufacturer',
            'Social Media DL (Bytes)',
            'Social Media UL (Bytes)',
            'Dur. (ms)',
            'Bearer Id'
        ]
        
        # Expected data types
        expected_types = {
            'MSISDN/Number': 'object',
            'Handset Type': 'object',
            'Handset Manufacturer': 'object',
            'Dur. (ms)': 'float64',
            'Bearer Id': 'object'
        }
        
        # Value ranges for numeric columns
        value_ranges = {
            'Dur. (ms)': {'min': 0},
            'Social Media DL (Bytes)': {'min': 0},
            'Social Media UL (Bytes)': {'min': 0}
        }
        
        results = {
            'columns': self.validate_required_columns(required_columns),
            'types': self.validate_data_types(expected_types),
            'ranges': self.validate_value_ranges(value_ranges)
        }
        
        return results 