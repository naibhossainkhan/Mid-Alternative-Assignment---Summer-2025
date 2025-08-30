"""
Core application modules for AI-Powered Customer Shopping Analytics.

This package contains the main application logic organized into:
- data: Data loading and processing
- ai: AI and machine learning components
- visualization: Chart and dashboard generation
- utils: Utility functions and helpers
"""

__version__ = "1.0.0"
__author__ = "Data Visualization Assignment - Summer 2025"

from . import data
from . import ai
from . import visualization
from . import utils

__all__ = ["data", "ai", "visualization", "utils"]
