#!/usr/bin/env python3
"""
Application launcher for AI-Powered Customer Shopping Analytics.

Usage:
    python run.py streamlit          # Run main Streamlit app
    python run.py streamlit-simple   # Run simple Streamlit app
    python run.py demo               # Run AI workflow demo
    python run.py demo-simple        # Run simple demo
    python run.py test               # Run tests
"""

import sys
import subprocess
import os
from pathlib import Path

def run_streamlit():
    """Run the main Streamlit application."""
    print("🚀 Starting Streamlit application...")
    subprocess.run(["streamlit", "run", "streamlit_app.py"])

def run_streamlit_simple():
    """Run the simple Streamlit application."""
    print("🚀 Starting simple Streamlit application...")
    subprocess.run(["streamlit", "run", "streamlit_app_simple.py"])

def run_demo():
    """Run the AI workflow demo."""
    print("🤖 Running AI workflow demo...")
    subprocess.run([sys.executable, "demos/demo_agentic_workflow.py"])

def run_demo_simple():
    """Run the simple demo."""
    print("🤖 Running simple demo...")
    subprocess.run([sys.executable, "demos/demo_agentic_workflow_simple.py"])

def run_tests():
    """Run the test suite."""
    print("🧪 Running tests...")
    subprocess.run([sys.executable, "-m", "pytest", "tests/"])

def main():
    """Main launcher function."""
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    command = sys.argv[1].lower()
    
    commands = {
        "streamlit": run_streamlit,
        "streamlit-simple": run_streamlit_simple,
        "demo": run_demo,
        "demo-simple": run_demo_simple,
        "test": run_tests,
    }
    
    if command in commands:
        commands[command]()
    else:
        print(f"❌ Unknown command: {command}")
        print(__doc__)

if __name__ == "__main__":
    main()
