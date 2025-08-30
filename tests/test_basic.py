"""
Basic tests to ensure the test suite works correctly.
"""

import pytest
import sys
import os

def test_python_version():
    """Test that we're using the correct Python version."""
    assert sys.version_info >= (3, 8), "Python 3.8+ required"

def test_imports():
    """Test that core modules can be imported."""
    try:
        from core.data import CustomerShoppingDataLoader
        assert CustomerShoppingDataLoader is not None
    except ImportError:
        # Fallback to old structure
        sys.path.append('src')
        from customer_data_loader import CustomerShoppingDataLoader
        assert CustomerShoppingDataLoader is not None

def test_config():
    """Test that configuration can be loaded."""
    try:
        from core.utils.config import config
        assert config is not None
    except ImportError:
        # Fallback to old structure
        from config import config
        assert config is not None

def test_data_file_exists():
    """Test that the data file exists."""
    data_file = "data/customer_shopping_data.csv"
    assert os.path.exists(data_file), f"Data file {data_file} not found"

def test_requirements_file_exists():
    """Test that requirements file exists."""
    assert os.path.exists("requirements.txt"), "requirements.txt not found"

def test_readme_exists():
    """Test that README exists."""
    assert os.path.exists("README.md"), "README.md not found"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
