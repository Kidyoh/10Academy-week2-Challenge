"""User Overview Analysis Page"""
import streamlit as st
from data_preparation import prepare_dashboard_data
from overview_loader import Task1DataLoader

# Cache data loading
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
        
        # Your existing overview page code here
        from overview import render_overview_page
        render_overview_page(data)
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.exception(e)

if __name__ == "__main__":
    main() 