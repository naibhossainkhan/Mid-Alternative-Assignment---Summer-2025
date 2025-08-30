#!/usr/bin/env python3
"""
Test script to simulate Streamlit data loading
"""

import os
import sys
import pandas as pd

# Simulate the path setup from streamlit app
sys.path.append('src')

def simulate_streamlit_data_loading():
    """Simulate the data loading process from Streamlit app"""
    
    print("Simulating Streamlit data loading...")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Script location: {__file__}")
    
    # Try the same paths as in the Streamlit app
    possible_paths = [
        "data/customer_shopping_data.csv",
        "../data/customer_shopping_data.csv",
        "./data/customer_shopping_data.csv",
        os.path.join(os.path.dirname(__file__), "..", "data", "customer_shopping_data.csv"),
        os.path.join(os.getcwd(), "data", "customer_shopping_data.csv"),
        "customer_shopping_data.csv"
    ]
    
    print("\nChecking file existence:")
    for path in possible_paths:
        exists = os.path.exists(path)
        print(f"  {path}: {'✓' if exists else '✗'}")
    
    # Try to import and use the data loader
    try:
        from customer_data_loader import load_and_prepare_customer_data
        print("\n✓ Successfully imported customer_data_loader")
        
        # Try loading with each path
        for path in possible_paths:
            if os.path.exists(path):
                print(f"\nTrying to load from: {path}")
                try:
                    loader, cleaned_data = load_and_prepare_customer_data(path)
                    if cleaned_data is not None:
                        print(f"✓ Successfully loaded {len(cleaned_data)} rows")
                        print(f"  Columns: {list(cleaned_data.columns)}")
                        return True
                    else:
                        print("✗ Loader returned None")
                except Exception as e:
                    print(f"✗ Error loading data: {e}")
                    import traceback
                    traceback.print_exc()
        
        print("\n✗ Failed to load data from any path")
        return False
        
    except ImportError as e:
        print(f"\n✗ Could not import customer_data_loader: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = simulate_streamlit_data_loading()
    if success:
        print("\n✅ Data loading simulation successful!")
    else:
        print("\n❌ Data loading simulation failed!")
