
"""Main dashboard page."""
import streamlit as st

def main():
    # Configure page settings
    st.set_page_config(
        page_title="TellCo Telecom Analytics",
        page_icon="📱",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Main page content
    st.title("TellCo Telecom Analytics Dashboard")
    
    st.markdown("""
    ### Welcome to TellCo Analytics Dashboard
    
    This dashboard provides comprehensive analysis of telecom user data across multiple dimensions:
    
    - **📈 User Overview**: Basic statistics and user distribution
    - **👥 User Engagement**: Usage patterns and user segmentation
    - **🌟 User Experience**: Network performance and user satisfaction
    - **😊 User Satisfaction**: Customer satisfaction analysis
    
    Navigate through the pages using the sidebar to explore different aspects of the analysis.
    """)
    
    # Add some sample metrics or overview stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("**Navigate** using the sidebar →")
    with col2:
        st.success("**Analyze** user behavior")
    with col3:
        st.warning("**Discover** insights")

if __name__ == "__main__":
    main() 
