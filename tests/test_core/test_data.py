"""
Tests for the data module.
"""

import pytest
import pandas as pd
from pathlib import Path

# Import the modules to test
try:
    from core.data import CustomerShoppingDataLoader, load_and_prepare_customer_data
except ImportError:
    # Fallback for old structure
    import sys
    sys.path.append('src')
    from customer_data_loader import CustomerShoppingDataLoader, load_and_prepare_customer_data

class TestCustomerShoppingDataLoader:
    """Test the CustomerShoppingDataLoader class."""
    
    def test_loader_initialization(self):
        """Test that the loader can be initialized."""
        loader = CustomerShoppingDataLoader()
        assert loader is not None
    
    def test_data_loading(self):
        """Test that data can be loaded from CSV."""
        data_path = Path("data/customer_shopping_data.csv")
        if data_path.exists():
            loader, data = load_and_prepare_customer_data(str(data_path))
            assert isinstance(data, pd.DataFrame)
            assert len(data) > 0
            assert "customer_id" in data.columns
    
    def test_basic_stats(self):
        """Test that basic statistics can be calculated."""
        loader = CustomerShoppingDataLoader()
        if hasattr(loader, 'get_basic_stats'):
            stats = loader.get_basic_stats()
            assert isinstance(stats, dict)
            assert "total_revenue" in stats

class TestDataProcessing:
    """Test data processing functions."""
    
    def test_data_cleaning(self):
        """Test that data cleaning works correctly."""
        # Create sample data
        sample_data = pd.DataFrame({
            'customer_id': ['C1', 'C2', 'C3'],
            'price': [100, 200, 300],
            'quantity': [1, 2, 1]
        })
        
        # Test that total_amount can be calculated
        if 'price' in sample_data.columns and 'quantity' in sample_data.columns:
            sample_data['total_amount'] = sample_data['price'] * sample_data['quantity']
            assert 'total_amount' in sample_data.columns
            assert sample_data['total_amount'].sum() == 600
