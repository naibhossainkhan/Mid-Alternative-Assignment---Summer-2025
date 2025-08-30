#!/usr/bin/env python3
"""
Simple Streamlit app to test data loading
"""

import streamlit as st
import pandas as pd
import os
import sys

# Add src to path
sys.path.append('src')

st.set_page_config(page_title="Data Loading Test", page_icon="🧪")

st.title("🧪 Data Loading Test")

st.write("Testing data loading functionality...")

# Check current directory
st.write(f"**Current working directory:** {os.getcwd()}")

# Check file existence
possible_paths = [
    "data/customer_shopping_data.csv",
    "../data/customer_shopping_data.csv",
    "./data/customer_shopping_data.csv",
    os.path.join(os.path.dirname(__file__), "..", "data", "customer_shopping_data.csv"),
    os.path.join(os.getcwd(), "data", "customer_shopping_data.csv"),
    "customer_shopping_data.csv"
]

st.write("**Checking file existence:**")
for path in possible_paths:
    exists = os.path.exists(path)
    st.write(f"- {path}: {'✅' if exists else '❌'}")

# Try to load data
st.write("**Attempting to load data...**")

try:
    from customer_data_loader import load_and_prepare_customer_data
    st.success("✅ Successfully imported customer_data_loader")
    
    # Try loading with each path
    for path in possible_paths:
        if os.path.exists(path):
            st.write(f"Trying to load from: {path}")
            try:
                loader, cleaned_data = load_and_prepare_customer_data(path)
                if cleaned_data is not None:
                    st.success(f"✅ Successfully loaded {len(cleaned_data)} rows from {path}")
                    st.write(f"Columns: {list(cleaned_data.columns)}")
                    
                    # Show a sample
                    st.write("**Sample data:**")
                    st.dataframe(cleaned_data.head())
                    
                    # Show basic stats
                    st.write("**Basic statistics:**")
                    st.write(f"- Total rows: {len(cleaned_data):,}")
                    st.write(f"- Total columns: {len(cleaned_data.columns)}")
                    st.write(f"- Revenue: ${cleaned_data['total_amount'].sum():,.0f}")
                    
                    break
                else:
                    st.error("❌ Loader returned None")
            except Exception as e:
                st.error(f"❌ Error loading data: {e}")
                st.exception(e)
    else:
        st.error("❌ Failed to load data from any path")
        
except ImportError as e:
    st.error(f"❌ Could not import customer_data_loader: {e}")
    st.exception(e)
