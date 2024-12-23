"""User Satisfaction Analysis Page"""
import streamlit as st
from src.utils.data_preparation import prepare_dashboard_data
from src.data.task1_loader import Task1DataLoader

@st.cache_data
def load_data():
    with st.spinner('Loading data...'):
        loader = Task1DataLoader()
        raw_data = loader.prepare_task1_data()
        return prepare_dashboard_data(raw_data['raw_data'])

def main():
    try:
        # Load data
        data = load_data()
        
        # Your existing satisfaction page code here
        from src.dashboard.components.satisfaction import render_satisfaction_page
        render_satisfaction_page(data)
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.exception(e)

if __name__ == "__main__":
    main() 