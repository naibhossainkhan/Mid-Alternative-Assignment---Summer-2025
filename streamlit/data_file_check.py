#!/usr/bin/env python3
"""
Script to check data file location in deployment environment
"""

import os
import glob
import streamlit as st

def check_data_file_location():
    """Check where the data file is located"""
    
    st.title("🔍 Data File Location Checker")
    
    st.write("This tool helps identify where the data file is located in the current environment.")
    
    # Current environment info
    st.write("**Environment Information:**")
    st.write(f"- Current working directory: `{os.getcwd()}`")
    st.write(f"- Script location: `{__file__}`")
    
    # List current directory contents
    st.write("**Current directory contents:**")
    try:
        contents = os.listdir('.')
        st.write(f"- Files and folders: {contents}")
    except Exception as e:
        st.write(f"- Error listing directory: {e}")
    
    # Search for data file
    st.write("**Searching for data file...**")
    
    # Explicit paths to check
    explicit_paths = [
        "data/customer_shopping_data.csv",
        "../data/customer_shopping_data.csv",
        "./data/customer_shopping_data.csv",
        "/mount/src/mid-alternative-assignment---summer-2025/data/customer_shopping_data.csv",
        "/app/data/customer_shopping_data.csv",
        "/workspace/data/customer_shopping_data.csv",
        "customer_shopping_data.csv"
    ]
    
    st.write("**Checking explicit paths:**")
    for path in explicit_paths:
        exists = os.path.exists(path)
        st.write(f"- `{path}`: {'✅' if exists else '❌'}")
        if exists:
            try:
                size = os.path.getsize(path)
                st.write(f"  - Size: {size:,} bytes ({size/1024/1024:.2f} MB)")
            except:
                st.write(f"  - Size: Unable to determine")
    
    # Recursive search
    st.write("**Recursive search results:**")
    patterns = [
        "**/customer_shopping_data.csv",
        "**/data/customer_shopping_data.csv"
    ]
    
    for pattern in patterns:
        try:
            matches = glob.glob(pattern, recursive=True)
            if matches:
                st.write(f"- Pattern `{pattern}` found:")
                for match in matches:
                    st.write(f"  - `{match}`")
                    try:
                        size = os.path.getsize(match)
                        st.write(f"    Size: {size:,} bytes ({size/1024/1024:.2f} MB)")
                    except:
                        st.write(f"    Size: Unable to determine")
            else:
                st.write(f"- Pattern `{pattern}`: No matches found")
        except Exception as e:
            st.write(f"- Pattern `{pattern}`: Error - {e}")
    
    # Try to read a small sample if file is found
    st.write("**Testing file reading:**")
    for path in explicit_paths:
        if os.path.exists(path):
            try:
                import pandas as pd
                df = pd.read_csv(path, nrows=5)
                st.success(f"✅ Successfully read sample from `{path}`")
                st.write(f"- Sample data shape: {df.shape}")
                st.write(f"- Columns: {list(df.columns)}")
                st.dataframe(df)
                break
            except Exception as e:
                st.error(f"❌ Error reading `{path}`: {e}")

if __name__ == "__main__":
    check_data_file_location()
