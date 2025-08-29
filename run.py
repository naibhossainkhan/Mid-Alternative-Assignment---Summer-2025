#!/usr/bin/env python3
"""
Main entry point for AI-Powered Customer Shopping Analytics Application.

This script serves as the primary entry point for running the Streamlit application
in a production environment.
"""

import os
import sys
from pathlib import Path

# Add the app directory to Python path
app_dir = Path(__file__).parent / "app"
sys.path.insert(0, str(app_dir))

def main():
    """Main application entry point."""
    try:
        # Import and run the Streamlit app
        from app.main import main as streamlit_main
        streamlit_main()
    except ImportError as e:
        print(f"Error importing application modules: {e}")
        print("Please ensure all dependencies are installed: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Application error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
