# CareStock Watch - Hospital Inventory Management
# With Smart Alert System
import streamlit as st
from snowflake.snowpark.context import get_active_session
import pandas as pd
import numpy as np
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="CareStock Watch",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Get Snowflake session
session = get_active_session()

# Sidebar navigation
st.sidebar.title("Hospital Inventory Management")
page = st.sidebar.radio("Navigate", ["Dashboard", "Inventory", "Smart Alerts", "Settings"])

if page == "Dashboard":
    st.title("Dashboard")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Items", "245", "+12")
    with col2:
        st.metric("Low Stock Items", "8", "-2")
    with col3:
        st.metric("Expiring Soon", "3", "+1")

elif page == "Inventory":
    st.title("Inventory Management")
    st.info("Inventory management features coming soon...")

elif page == "Smart Alerts":
    st.title("Smart Alerts System")
    
    # Sample alert data
    alerts_data = {
        "Item Name": ["Paracetamol", "Insulin", "Antibiotics", "Saline Solution"],
        "Alert Type": ["Low Stock", "Expiry Alert", "Overstock", "Low Stock"],
        "Severity": ["High", "Critical", "Medium", "High"],
        "Current Level": ["15 units", "8 vials", "250 boxes", "20 liters"],
        "Threshold": ["50 units", "30 vials", "100 boxes", "50 liters"]
    }
    
    smart_alerts_df = pd.DataFrame(alerts_data)
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Alerts", len(smart_alerts_df))
    with col2:
        critical_count = len(smart_alerts_df[smart_alerts_df["Severity"] == "Critical"])
        st.metric("Critical", critical_count)
    with col3:
        high_count = len(smart_alerts_df[smart_alerts_df["Severity"] == "High"])
        st.metric("High Priority", high_count)
    with col4:
        low_stock = len(smart_alerts_df[smart_alerts_df["Alert Type"] == "Low Stock"])
        st.metric("Low Stock", low_stock)
    
    st.subheader("Active Alerts")
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        severity_filter = st.multiselect("Filter by Severity", options=smart_alerts_df["Severity"].unique(), default=smart_alerts_df["Severity"].unique())
    with col2:
        type_filter = st.multiselect("Filter by Alert Type", options=smart_alerts_df["Alert Type"].unique(), default=smart_alerts_df["Alert Type"].unique())
    
    # Apply filters
    filt = smart_alerts_df[(smart_alerts_df["Severity"].isin(severity_filter)) & (smart_alerts_df["Alert Type"].isin(type_filter))]
    
    st.dataframe(filt, use_container_width=True)
    
    if len(filt) == 0:
        st.info("No alerts generated yet.")

elif page == "Settings":
    st.title("Settings")
    st.subheader("Notification Preferences")
    email_alerts = st.checkbox("Enable Email Alerts")
    sms_alerts = st.checkbox("Enable SMS Alerts")
    if st.button("Save Settings"):
        st.success("Settings saved successfully!")

st.sidebar.divider()
st.sidebar.info("CareStock Watch v1.0 - Hospital Inventory Management System")