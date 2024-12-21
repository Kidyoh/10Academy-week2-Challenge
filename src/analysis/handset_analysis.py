"""Handset analysis module."""
import pandas as pd

class HandsetAnalyzer:
    """Class for analyzing handset data."""
    
    def __init__(self, data):
        self.data = data
    
    def get_top_handsets(self, n=10):
        """Get top n handsets by usage."""
        return (self.data['handset']
                .value_counts()
                .head(n)
                .reset_index()
                .rename(columns={'index': 'handset', 'handset': 'count'}))
    
    def get_top_manufacturers(self, n=3):
        """Get top n handset manufacturers."""
        return (self.data['manufacturer']
                .value_counts()
                .head(n)
                .reset_index()
                .rename(columns={'index': 'manufacturer', 'manufacturer': 'count'}))
    
    def get_top_handsets_per_manufacturer(self, manufacturer, n=5):
        """Get top n handsets for a specific manufacturer."""
        manufacturer_data = self.data[self.data['manufacturer'] == manufacturer]
        return (manufacturer_data['handset']
                .value_counts()
                .head(n)
                .reset_index()
                .rename(columns={'index': 'handset', 'handset': 'count'})) 