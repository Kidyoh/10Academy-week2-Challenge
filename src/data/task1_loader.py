"""Data loader for Task 1 analysis."""
import pandas as pd
import logging
from pathlib import Path
from typing import Dict, Optional

logger = logging.getLogger('tellco_analysis')

class Task1DataLoader:
    """Class for loading and preparing Task 1 data."""
    
    def __init__(self, data_dir: str = "Data"):
        self.data_dir = Path(data_dir)
        self.data = None
        
    def load_data(self) -> pd.DataFrame:
        """Load the main dataset."""
        try:
            file_path = self.data_dir / "Copy of Week2_challenge_data_source(CSV).csv"
            self.data = pd.read_csv(file_path)
            logger.info(f"Loaded data with {len(self.data)} records")
            return self.data
        except FileNotFoundError:
            logger.error(f"Data file not found at {file_path}")
            raise
    
    def prepare_task1_data(self) -> Dict[str, pd.DataFrame]:
        """Prepare data specifically for Task 1 requirements."""
        if self.data is None:
            self.load_data()
        
        # Extract handset information
        handset_info = self.data[['MSISDN/Number', 'Handset Type', 'Handset Manufacturer']].copy()
        handset_info = handset_info.rename(columns={
            'MSISDN/Number': 'msisdn',
            'Handset Type': 'handset',
            'Handset Manufacturer': 'manufacturer'
        })
        
        # Prepare application usage data
        app_usage = self.data.groupby('MSISDN/Number').agg({
            'Social Media DL (Bytes)': 'sum',
            'Social Media UL (Bytes)': 'sum',
            'Google DL (Bytes)': 'sum',
            'Google UL (Bytes)': 'sum',
            'Email DL (Bytes)': 'sum',
            'Email UL (Bytes)': 'sum',
            'Youtube DL (Bytes)': 'sum',
            'Youtube UL (Bytes)': 'sum',
            'Netflix DL (Bytes)': 'sum',
            'Netflix UL (Bytes)': 'sum',
            'Gaming DL (Bytes)': 'sum',
            'Gaming UL (Bytes)': 'sum',
            'Other DL (Bytes)': 'sum',
            'Other UL (Bytes)': 'sum',
            'Duration (ms)': 'sum',
            'Session ID': 'count'
        }).reset_index()
        
        # Rename columns for consistency
        app_usage = app_usage.rename(columns={
            'MSISDN/Number': 'msisdn',
            'Duration (ms)': 'session_duration',
            'Session ID': 'total_sessions'
        })
        
        # Calculate total bytes per application
        apps = ['Social Media', 'Google', 'Email', 'Youtube', 'Netflix', 'Gaming', 'Other']
        for app in apps:
            app_usage[f'{app.lower()}_total_bytes'] = (
                app_usage[f'{app} DL (Bytes)'] + app_usage[f'{app} UL (Bytes)']
            )
        
        logger.info("Data preparation for Task 1 completed")
        
        return {
            'app_usage': app_usage,
            'handset_info': handset_info,
            'raw_data': self.data
        } 