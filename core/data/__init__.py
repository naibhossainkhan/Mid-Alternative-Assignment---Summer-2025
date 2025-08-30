"""
Data handling modules for customer shopping analytics.

This module contains:
- loader: Data loading and preprocessing
- processor: Data processing utilities
"""

from .loader import CustomerShoppingDataLoader, load_and_prepare_customer_data

__all__ = ["CustomerShoppingDataLoader", "load_and_prepare_customer_data"]
