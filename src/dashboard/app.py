"""Main dashboard application."""
import streamlit as st
from src.dashboard.pages.overview import render_overview_page
from src.dashboard.pages.engagement import render_engagement_page
from src.dashboard.pages.experience import render_experience_page
from src.dashboard.pages.satisfaction import render_satisfaction_page
from src.data.task1_loader import Task1DataLoader
from src.utils.data_preparation import prepare_dashboard_data
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Configure page settings
    st.set_page_config(
        page_title="TellCo Telecom Analytics",
        page_icon="📱",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Sidebar Configuration
    with st.sidebar:
        st.title("TellCo Analytics")
        
        st.markdown("---")  # Divider
        
        # Main Navigation
        st.sidebar.markdown("## 📊 Main Analysis")
        pages = {
            "📈 User Overview": render_overview_page,
            "👥 User Engagement": render_engagement_page,
            "🌟 User Experience": render_experience_page,
            "😊 User Satisfaction": render_satisfaction_page
        }
        
        selected_page = st.radio("", list(pages.keys()))
        
        st.markdown("---")  # Divider
        
        # About section in sidebar
        st.markdown("## ℹ️ About")
        st.markdown("""
        This dashboard provides comprehensive analysis of:
        - User Overview
        - User Engagement
        - User Experience
        - User Satisfaction
        """)
        
        # Version info
        st.sidebar.markdown("---")
        st.markdown("v1.0.0")
    
    # Main content area
    try:
        # Cache the data loading
        @st.cache_data
        def load_data():
            with st.spinner('Loading data...'):
                loader = Task1DataLoader()
                raw_data = loader.prepare_task1_data()
                return prepare_dashboard_data(raw_data['raw_data'])
        
        # Load data
        data = load_data()
        
        # Remove the radio button label from the page title
        selected_page_clean = selected_page.split(" ", 1)[1]
        
        # Add header to main content area
        st.title(f"{selected_page_clean} Analysis")
        st.markdown("---")
        
        # Render selected page
        pages[selected_page](data)
        
        # Add footer
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center'>
            <p>Developed by [Your Name] | TellCo Analytics Dashboard</p>
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        logger.error(f"Dashboard error: {str(e)}")
        st.exception(e)

if __name__ == "__main__":
    main() 