"""Data loader for Task 1 analysis."""
import pandas as pd
import logging
from pathlib import Path
from typing import Dict, Optional
import os

logger = logging.getLogger('tellco_analysis')

class load_telco_data:
    """Class for loading and preparing Task 1 data."""
    
    def __init__(self, data_path: Optional[str] = None):
        """Initialize with flexible data path options."""
        # Get the project root directory (where src is located)
        project_root = Path(__file__).parent.parent.parent
        
        if data_path:
            self.data_path = Path(data_path)
        else:
            # Try different common locations with absolute paths
            possible_paths = [
                project_root / "Data" / "Copy of Week2_challenge_data_source(CSV).csv",
                project_root / "data" / "Copy of Week2_challenge_data_source(CSV).csv",
                Path.cwd() / "Data" / "Copy of Week2_challenge_data_source(CSV).csv",
                Path.cwd() / "data" / "Copy of Week2_challenge_data_source(CSV).csv",
                Path(os.path.expanduser("~/Downloads/Copy of Week2_challenge_data_source(CSV).csv"))
            ]
            
            logger.info(f"Current working directory: {Path.cwd()}")
            logger.info(f"Project root directory: {project_root}")
            
            for path in possible_paths:
                logger.info(f"Checking path: {path}")
                if path.exists():
                    self.data_path = path
                    logger.info(f"Found data file at: {path}")
                    break
            else:
                available_files = list(project_root.glob("**/*.csv"))
                logger.error(f"Available CSV files in project: {available_files}")
                raise FileNotFoundError(
                    "Could not find the data file. Please specify the correct path using "
                    "Task1DataLoader(data_path='path/to/your/file.csv'). "
                    f"Tried paths: {[str(p) for p in possible_paths]}"
                )
        
        self.data = None
    
    def load_data(self) -> pd.DataFrame:
        """Load the main dataset."""
        try:
            self.data = pd.read_csv(self.data_path)
            logger.info(f"Loaded data with {len(self.data)} records")
            logger.info(f"Columns in dataset: {self.data.columns.tolist()}")
            return self.data
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            logger.error(f"Attempted to load from: {self.data_path}")
            raise
    
    def prepare_task1_data(self) -> Dict[str, pd.DataFrame]:
        """Prepare data specifically for Task 1 requirements."""
        if self.data is None:
            self.load_data()
        
        try:
            # Extract handset information
            handset_info = self.data[['MSISDN/Number', 'Handset Type', 'Handset Manufacturer']].copy()
            handset_info = handset_info.rename(columns={
                'MSISDN/Number': 'msisdn',
                'Handset Type': 'handset',
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
                'Dur. (ms)': 'sum',
                'Bearer Id': 'count'
            }).reset_index()
            
            # Rename columns for consistency
            app_usage = app_usage.rename(columns={
                'MSISDN/Number': 'msisdn',
                'Dur. (ms)': 'session_duration',
                'Bearer Id': 'total_sessions'
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
            
        except Exception as e:
            logger.error(f"Error preparing data: {str(e)}")
            raise 