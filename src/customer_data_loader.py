"""
Customer Shopping Data Loader Module
Handles loading, cleaning, and analysis of customer shopping data
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple
import os
from datetime import datetime

class CustomerShoppingDataLoader:
    """Class to handle loading and preprocessing of customer shopping data"""
    
    def __init__(self, file_path: str = "data/customer_shopping_data.csv"):
        """
        Initialize the data loader
        
        Args:
            file_path (str): Path to the CSV file
        """
        self.file_path = file_path
        self.data = None
        self.cleaned_data = None
        
    def load_data(self) -> pd.DataFrame:
        """
        Load the customer shopping data from CSV file
        
        Returns:
            pd.DataFrame: Loaded data
        """
        try:
            self.data = pd.read_csv(self.file_path)
            print(f"Successfully loaded {len(self.data):,} records from {self.file_path}")
            return self.data
        except FileNotFoundError:
            print(f"Error: File {self.file_path} not found")
            return None
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
    
    def clean_data(self) -> pd.DataFrame:
        """
        Clean and preprocess the customer shopping data
        
        Returns:
            pd.DataFrame: Cleaned data
        """
        if self.data is None:
            print("No data loaded. Please load data first.")
            return None
        
        # Create a copy for cleaning
        self.cleaned_data = self.data.copy()
        
        # Convert invoice_date to datetime and ensure Streamlit compatibility
        self.cleaned_data['invoice_date'] = pd.to_datetime(self.cleaned_data['invoice_date'], format='%d/%m/%Y', errors='coerce')
        # Convert to string format for better Streamlit compatibility
        self.cleaned_data['invoice_date_str'] = self.cleaned_data['invoice_date'].dt.strftime('%Y-%m-%d')
        
        # Add derived columns
        self.cleaned_data['month'] = self.cleaned_data['invoice_date'].dt.month
        self.cleaned_data['year'] = self.cleaned_data['invoice_date'].dt.year
        self.cleaned_data['day_of_week'] = self.cleaned_data['invoice_date'].dt.day_name()
        self.cleaned_data['quarter'] = self.cleaned_data['invoice_date'].dt.quarter
        
        # Calculate total amount spent
        self.cleaned_data['total_amount'] = self.cleaned_data['quantity'] * self.cleaned_data['price']
        
        # Create age groups
        self.cleaned_data['age_group'] = pd.cut(
            self.cleaned_data['age'], 
            bins=[0, 25, 35, 45, 55, 100], 
            labels=['18-25', '26-35', '36-45', '46-55', '55+']
        )
        
        # Create spending categories
        self.cleaned_data['spending_category'] = pd.cut(
            self.cleaned_data['total_amount'],
            bins=[0, 100, 500, 1000, 5000, float('inf')],
            labels=['Low (<$100)', 'Medium ($100-$500)', 'High ($500-$1000)', 'Very High ($1000-$5000)', 'Premium ($5000+)']
        )
        
        # Remove any rows with missing values
        initial_rows = len(self.cleaned_data)
        self.cleaned_data = self.cleaned_data.dropna()
        final_rows = len(self.cleaned_data)
        
        if initial_rows != final_rows:
            print(f"Removed {initial_rows - final_rows} rows with missing values")
        
        print(f"Data cleaning completed. Final dataset has {len(self.cleaned_data):,} records")
        return self.cleaned_data
    
    def get_basic_stats(self) -> Dict[str, Any]:
        """
        Get basic statistical information about the dataset
        
        Returns:
            Dict[str, Any]: Dictionary containing basic statistics
        """
        if self.cleaned_data is None:
            print("No cleaned data available. Please clean data first.")
            return {}
        
        stats = {
            'total_records': len(self.cleaned_data),
            'date_range': {
                'start': self.cleaned_data['invoice_date'].min().strftime('%Y-%m-%d'),
                'end': self.cleaned_data['invoice_date'].max().strftime('%Y-%m-%d')
            },
            'total_customers': self.cleaned_data['customer_id'].nunique(),
            'total_invoices': self.cleaned_data['invoice_no'].nunique(),
            'shopping_malls': self.cleaned_data['shopping_mall'].unique().tolist(),
            'categories': self.cleaned_data['category'].unique().tolist(),
            'payment_methods': self.cleaned_data['payment_method'].unique().tolist(),
            'total_revenue': self.cleaned_data['total_amount'].sum(),
            'total_quantity': self.cleaned_data['quantity'].sum(),
            'average_transaction_value': self.cleaned_data['total_amount'].mean(),
            'average_age': self.cleaned_data['age'].mean(),
            'gender_distribution': self.cleaned_data['gender'].value_counts().to_dict()
        }
        
        return stats
    
    def get_summary_by_category(self) -> pd.DataFrame:
        """
        Get summary statistics grouped by product category
        
        Returns:
            pd.DataFrame: Summary statistics by category
        """
        if self.cleaned_data is None:
            print("No cleaned data available. Please clean data first.")
            return None
        
        return self.cleaned_data.groupby('category').agg({
            'total_amount': ['sum', 'mean', 'count'],
            'quantity': ['sum', 'mean'],
            'price': 'mean',
            'customer_id': 'nunique'
        }).round(2)
    
    def get_summary_by_mall(self) -> pd.DataFrame:
        """
        Get summary statistics grouped by shopping mall
        
        Returns:
            pd.DataFrame: Summary statistics by mall
        """
        if self.cleaned_data is None:
            print("No cleaned data available. Please clean data first.")
            return None
        
        return self.cleaned_data.groupby('shopping_mall').agg({
            'total_amount': ['sum', 'mean', 'count'],
            'quantity': ['sum', 'mean'],
            'customer_id': 'nunique',
            'invoice_no': 'nunique'
        }).round(2)
    
    def get_summary_by_gender(self) -> pd.DataFrame:
        """
        Get summary statistics grouped by gender
        
        Returns:
            pd.DataFrame: Summary statistics by gender
        """
        if self.cleaned_data is None:
            print("No cleaned data available. Please clean data first.")
            return None
        
        return self.cleaned_data.groupby('gender').agg({
            'total_amount': ['sum', 'mean', 'count'],
            'quantity': ['sum', 'mean'],
            'age': 'mean',
            'customer_id': 'nunique'
        }).round(2)
    
    def get_time_series_data(self) -> pd.DataFrame:
        """
        Get time series aggregated data
        
        Returns:
            pd.DataFrame: Time series data
        """
        if self.cleaned_data is None:
            print("No cleaned data available. Please clean data first.")
            return None
        
        return self.cleaned_data.groupby('invoice_date').agg({
            'total_amount': 'sum',
            'quantity': 'sum',
            'customer_id': 'nunique',
            'invoice_no': 'nunique'
        }).reset_index()
    
    def get_age_group_analysis(self) -> pd.DataFrame:
        """
        Get analysis by age groups
        
        Returns:
            pd.DataFrame: Age group analysis
        """
        if self.cleaned_data is None:
            print("No cleaned data available. Please clean data first.")
            return None
        
        return self.cleaned_data.groupby('age_group').agg({
            'total_amount': ['sum', 'mean', 'count'],
            'quantity': ['sum', 'mean'],
            'customer_id': 'nunique',
            'category': lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else 'Unknown'
        }).round(2)
    
    def get_payment_method_analysis(self) -> pd.DataFrame:
        """
        Get analysis by payment method
        
        Returns:
            pd.DataFrame: Payment method analysis
        """
        if self.cleaned_data is None:
            print("No cleaned data available. Please clean data first.")
            return None
        
        return self.cleaned_data.groupby('payment_method').agg({
            'total_amount': ['sum', 'mean', 'count'],
            'quantity': ['sum', 'mean'],
            'customer_id': 'nunique'
        }).round(2)
    
    def get_data_for_visualization(self, group_by: str = 'category') -> Tuple[pd.DataFrame, str]:
        """
        Get data formatted for visualization
        
        Args:
            group_by (str): Column to group by ('category', 'shopping_mall', 'gender', 'age_group', 'payment_method')
            
        Returns:
            Tuple[pd.DataFrame, str]: Formatted data and title
        """
        if self.cleaned_data is None:
            print("No cleaned data available. Please clean data first.")
            return None, ""
        
        valid_groups = ['category', 'shopping_mall', 'gender', 'age_group', 'payment_method']
        if group_by not in valid_groups:
            print(f"Invalid group_by parameter: {group_by}. Must be one of {valid_groups}")
            return None, ""
        
        viz_data = self.cleaned_data.groupby(group_by).agg({
            'total_amount': 'sum',
            'quantity': 'sum',
            'customer_id': 'nunique',
            'invoice_no': 'nunique'
        }).reset_index()
        
        title = f"Customer Shopping Analysis by {group_by.replace('_', ' ').title()}"
        
        return viz_data, title
    
    def get_customer_segments(self) -> pd.DataFrame:
        """
        Get customer segmentation analysis
        
        Returns:
            pd.DataFrame: Customer segments
        """
        if self.cleaned_data is None:
            print("No cleaned data available. Please clean data first.")
            return None
        
        # Create customer segments based on spending behavior
        customer_segments = self.cleaned_data.groupby('customer_id').agg({
            'total_amount': 'sum',
            'invoice_no': 'nunique',
            'category': 'nunique',
            'shopping_mall': 'nunique'
        }).reset_index()
        
        # Add segment labels
        customer_segments['segment'] = pd.cut(
            customer_segments['total_amount'],
            bins=[0, 1000, 5000, 10000, float('inf')],
            labels=['Budget', 'Regular', 'Premium', 'VIP']
        )
        
        return customer_segments

def load_and_prepare_customer_data(file_path: str = "data/customer_shopping_data.csv") -> Tuple[CustomerShoppingDataLoader, pd.DataFrame]:
    """
    Convenience function to load and prepare customer shopping data
    
    Args:
        file_path (str): Path to the CSV file
        
    Returns:
        Tuple[CustomerShoppingDataLoader, pd.DataFrame]: Data loader instance and cleaned data
    """
    loader = CustomerShoppingDataLoader(file_path)
    loader.load_data()
    cleaned_data = loader.clean_data()
    return loader, cleaned_data
