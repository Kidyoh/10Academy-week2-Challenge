"""Data preprocessing utilities."""
import pandas as pd

class DataPreprocessor:
    """Class for handling data preprocessing tasks."""
    
    def __init__(self):
        self.data = None
    
    def load_data(self, data_path):
        """Load data from CSV or database."""
        self.data = pd.read_csv(data_path)
        return self
    
    def clean_data(self):
        """Basic data cleaning operations."""
        if self.data is None:
            raise ValueError("Data not loaded. Call load_data first.")
        
        # Remove duplicates
        self.data = self.data.drop_duplicates()
        
        # Handle missing values
        self.data = self.data.dropna()
        
        return self 