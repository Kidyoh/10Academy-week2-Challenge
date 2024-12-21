"""User overview dashboard component."""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def render_overview_section(analyzer):
    """Render user overview section."""
    stats = analyzer.get_user_statistics()
    
    # Display metrics in columns
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Users", f"{stats['total_users']:,}")
    with col2:
        st.metric("Active Users", f"{stats['active_users']:,}")
    with col3:
        active_rate = (stats['active_users'] / stats['total_users']) * 100
        st.metric("Active Rate", f"{active_rate:.1f}%")
    
    # Add user activity distribution
    st.subheader("User Activity Distribution")
    fig = go.Figure()
    # Add visualization logic here
    st.plotly_chart(fig) 