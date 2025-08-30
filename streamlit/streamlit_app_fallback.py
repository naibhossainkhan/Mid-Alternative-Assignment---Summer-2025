#!/usr/bin/env python3
"""
Fallback Streamlit app that can work without the data file
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime, timedelta

# Add src to path
sys.path.append('src')

st.set_page_config(
    page_title="AI-Powered Customer Shopping Analytics (Fallback)",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def generate_sample_data():
    """Generate sample data for demonstration purposes"""
    
    # Generate sample customer shopping data
    np.random.seed(42)
    n_records = 1000
    
    # Sample data
    shopping_malls = ['Mall A', 'Mall B', 'Mall C', 'Mall D', 'Mall E']
    categories = ['Electronics', 'Clothing', 'Food', 'Books', 'Sports']
    payment_methods = ['Credit Card', 'Cash', 'Debit Card', 'Mobile Payment']
    genders = ['Male', 'Female']
    
    data = {
        'invoice_no': [f'INV{i:06d}' for i in range(1, n_records + 1)],
        'customer_id': np.random.randint(1000, 9999, n_records),
        'gender': np.random.choice(genders, n_records),
        'age': np.random.randint(18, 70, n_records),
        'category': np.random.choice(categories, n_records),
        'quantity': np.random.randint(1, 10, n_records),
        'price': np.random.uniform(10, 500, n_records).round(2),
        'payment_method': np.random.choice(payment_methods, n_records),
        'invoice_date': [datetime.now() - timedelta(days=np.random.randint(0, 365)) for _ in range(n_records)],
        'shopping_mall': np.random.choice(shopping_malls, n_records)
    }
    
    df = pd.DataFrame(data)
    
    # Add derived columns
    df['total_amount'] = df['quantity'] * df['price']
    df['month'] = df['invoice_date'].dt.month
    df['year'] = df['invoice_date'].dt.year
    df['day_of_week'] = df['invoice_date'].dt.day_name()
    df['quarter'] = df['invoice_date'].dt.quarter
    
    # Age groups
    df['age_group'] = pd.cut(df['age'], bins=[0, 25, 35, 45, 55, 100], 
                            labels=['18-25', '26-35', '36-45', '46-55', '55+'])
    
    # Spending categories
    df['spending_category'] = pd.cut(df['total_amount'], 
                                   bins=[0, 100, 500, 1000, 5000, float('inf')],
                                   labels=['Low (<$100)', 'Medium ($100-$500)', 'High ($500-$1000)', 
                                          'Very High ($1000-$5000)', 'Premium ($5000+)'])
    
    return df

def main():
    """Main application function"""
    
    # Header
    st.markdown('<h1 class="main-header">🛍️ AI-Powered Customer Shopping Analytics (Fallback Mode)</h1>', unsafe_allow_html=True)
    st.markdown("### Using Sample Data for Demonstration")
    
    # Warning about fallback mode
    st.warning("⚠️ **Fallback Mode**: Using sample data because the actual data file could not be loaded. This is for demonstration purposes only.")
    
    # Try to load real data first
    try:
        from customer_data_loader import load_and_prepare_customer_data
        
        # Try multiple paths
        possible_paths = [
            "data/customer_shopping_data.csv",
            "../data/customer_shopping_data.csv",
            "./data/customer_shopping_data.csv",
            "/mount/src/mid-alternative-assignment---summer-2025/data/customer_shopping_data.csv",
            "/app/data/customer_shopping_data.csv",
            "/workspace/data/customer_shopping_data.csv"
        ]
        
        data = None
        for path in possible_paths:
            if os.path.exists(path):
                try:
                    _, data = load_and_prepare_customer_data(path)
                    if data is not None:
                        st.success(f"✅ Successfully loaded real data from: {path}")
                        break
                except Exception as e:
                    st.error(f"Error loading from {path}: {e}")
        
        if data is None:
            st.info("📊 Generating sample data for demonstration...")
            data = generate_sample_data()
            
    except ImportError:
        st.info("📊 Generating sample data for demonstration...")
        data = generate_sample_data()
    
    # Display metrics
    st.markdown("### 📊 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_revenue = data['total_amount'].sum()
        st.metric("Total Revenue", f"${total_revenue:,.0f}")
    
    with col2:
        total_transactions = len(data)
        st.metric("Total Transactions", f"{total_transactions:,}")
    
    with col3:
        avg_transaction = data['total_amount'].mean()
        st.metric("Avg Transaction Value", f"${avg_transaction:,.0f}")
    
    with col4:
        total_customers = data['customer_id'].nunique()
        st.metric("Unique Customers", f"{total_customers:,}")
    
    # Create visualizations
    st.markdown("### 📈 Analytics Dashboard")
    
    # Revenue by Category
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Revenue by Category")
        category_revenue = data.groupby('category')['total_amount'].sum().reset_index()
        st.bar_chart(category_revenue.set_index('category'))
    
    with col2:
        st.subheader("Revenue by Shopping Mall")
        mall_revenue = data.groupby('shopping_mall')['total_amount'].sum().reset_index()
        st.bar_chart(mall_revenue.set_index('shopping_mall'))
    
    # Data preview
    st.markdown("### 📋 Data Preview")
    st.dataframe(data.head(10), use_container_width=True)
    
    # Data info
    st.markdown("### 📊 Data Information")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Dataset Statistics:**")
        st.write(f"- Total records: {len(data):,}")
        st.write(f"- Date range: {data['invoice_date'].min().strftime('%Y-%m-%d')} to {data['invoice_date'].max().strftime('%Y-%m-%d')}")
        st.write(f"- Shopping malls: {data['shopping_mall'].nunique()}")
        st.write(f"- Categories: {data['category'].nunique()}")
    
    with col2:
        st.write("**Data Quality:**")
        missing_data = data.isnull().sum()
        if missing_data.sum() == 0:
            st.success("✅ No missing values")
        else:
            st.write("Missing values:")
            st.write(missing_data[missing_data > 0])
    
    # Troubleshooting section
    with st.expander("🔧 Troubleshooting Data Loading"):
        st.write("If you're seeing this fallback mode, it means the actual data file couldn't be loaded.")
        st.write("**Possible solutions:**")
        st.write("1. Ensure the data file is in the correct location")
        st.write("2. Check file permissions")
        st.write("3. Verify the file path in deployment environment")
        st.write("4. Run the data file checker: `streamlit run streamlit/data_file_check.py`")

if __name__ == "__main__":
    main()
