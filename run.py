#!/usr/bin/env python3
"""
Simple Launcher for AI-Powered Customer Shopping Analytics
This file provides a quick way to run the application
"""

import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

if __name__ == "__main__":
    # Import and run the main application
    from main import main
    main()
