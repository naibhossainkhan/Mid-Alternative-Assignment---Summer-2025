#!/usr/bin/env python3
"""
Test script to verify data loading functionality
"""

import os
import sys
import pandas as pd

# Add src to path
sys.path.append('src')

def test_data_loading():
    """Test data loading from different paths"""
    
    print("Testing data loading functionality...")
    print(f"Current working directory: {os.getcwd()}")
    
    # Test paths
    possible_paths = [
        "data/customer_shopping_data.csv",
        "../data/customer_shopping_data.csv",
        "./data/customer_shopping_data.csv",
        os.path.join(os.path.dirname(__file__), "data", "customer_shopping_data.csv"),
        os.path.join(os.getcwd(), "data", "customer_shopping_data.csv"),
    ]
    
    print("\nChecking file existence:")
    for path in possible_paths:
        exists = os.path.exists(path)
        print(f"  {path}: {'✓' if exists else '✗'}")
    
    # Test direct pandas loading
    print("\nTesting direct pandas loading:")
    for path in possible_paths:
        if os.path.exists(path):
            try:
                df = pd.read_csv(path)
                print(f"  ✓ Successfully loaded {len(df)} rows from {path}")
                print(f"    Columns: {list(df.columns)}")
                break
            except Exception as e:
                print(f"  ✗ Failed to load {path}: {e}")
    
    # Test our custom loader
    print("\nTesting custom data loader:")
    try:
        from customer_data_loader import load_and_prepare_customer_data
        
        for path in possible_paths:
            if os.path.exists(path):
                try:
                    loader, cleaned_data = load_and_prepare_customer_data(path)
                    if cleaned_data is not None:
                        print(f"  ✓ Successfully loaded and cleaned {len(cleaned_data)} rows from {path}")
                        print(f"    Columns: {list(cleaned_data.columns)}")
                        break
                    else:
                        print(f"  ✗ Loader returned None for {path}")
                except Exception as e:
                    print(f"  ✗ Failed to load with custom loader from {path}: {e}")
    except ImportError as e:
        print(f"  ✗ Could not import customer_data_loader: {e}")

if __name__ == "__main__":
    test_data_loading()
