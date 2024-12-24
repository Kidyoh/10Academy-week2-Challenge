"""User overview dashboard page."""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def render_overview_page(data):
    st.title("User Overview Analysis")
    
    try:
        raw_data = data['raw_data']
        
        # Basic User Statistics
        total_users = len(raw_data['MSISDN/Number'].unique())
        total_handsets = len(raw_data['Handset Type'].unique())
        total_manufacturers = len(raw_data['Handset Manufacturer'].unique())
        
        # KPI Metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Users", f"{total_users:,}")
        with col2:
            st.metric("Unique Handsets", f"{total_handsets:,}")
        with col3:
            st.metric("Manufacturers", f"{total_manufacturers:,}")
            
        # Handset Analysis
        st.subheader("Handset Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Top 10 Handsets
            handset_counts = raw_data['Handset Type'].value_counts().head(10)
            fig_handsets = px.bar(
                x=handset_counts.index,
                y=handset_counts.values,
                title="Top 10 Handset Types",
                labels={'x': 'Handset Type', 'y': 'Count'}
            )
            st.plotly_chart(fig_handsets, use_container_width=True)
            
        with col2:
            # Manufacturer Distribution
            manufacturer_counts = raw_data['Handset Manufacturer'].value_counts()
            fig_manufacturers = px.pie(
                values=manufacturer_counts.values,
                names=manufacturer_counts.index,
                title="Manufacturer Distribution"
            )
            st.plotly_chart(fig_manufacturers, use_container_width=True)
            
        # Application Usage Overview
        st.subheader("Application Usage Overview")
        
        # Calculate total bytes per application
        app_cols = {
            'Social Media': ['Social Media DL (Bytes)', 'Social Media UL (Bytes)'],
            'Google': ['Google DL (Bytes)', 'Google UL (Bytes)'],
            'Email': ['Email DL (Bytes)', 'Email UL (Bytes)'],
            'Youtube': ['Youtube DL (Bytes)', 'Youtube UL (Bytes)'],
            'Netflix': ['Netflix DL (Bytes)', 'Netflix UL (Bytes)'],
            'Gaming': ['Gaming DL (Bytes)', 'Gaming UL (Bytes)'],
            'Other': ['Other DL (Bytes)', 'Other UL (Bytes)']
        }
        
        app_totals = {}
        for app, cols in app_cols.items():
            app_totals[app] = raw_data[cols[0]].fillna(0).sum() + raw_data[cols[1]].fillna(0).sum()
            
        # Create application usage chart
        fig_apps = px.pie(
            values=list(app_totals.values()),
            names=list(app_totals.keys()),
            title="Total Data Usage by Application"
        )
        st.plotly_chart(fig_apps, use_container_width=True)
        
        # Top Locations
        st.subheader("Top Locations")
        location_counts = raw_data['Last Location Name'].value_counts().head(10)
        fig_locations = px.bar(
            x=location_counts.index,
            y=location_counts.values,
            title="Top 10 Locations",
            labels={'x': 'Location', 'y': 'Count'}
        )
        st.plotly_chart(fig_locations, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error in overview analysis: {str(e)}")
        st.exception(e) 