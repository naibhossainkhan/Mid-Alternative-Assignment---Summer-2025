#!/usr/bin/env python3
"""
Debug script to run Streamlit and capture errors
"""

import subprocess
import sys
import os

def run_streamlit_with_debug():
    """Run Streamlit app with debug output"""
    
    print("Starting Streamlit app with debug output...")
    print(f"Current directory: {os.getcwd()}")
    print(f"Python executable: {sys.executable}")
    
    # Check if the app file exists
    app_file = "streamlit/streamlit_app.py"
    if not os.path.exists(app_file):
        print(f"Error: {app_file} not found!")
        return
    
    # Check if data file exists
    data_file = "data/customer_shopping_data.csv"
    if not os.path.exists(data_file):
        print(f"Error: {data_file} not found!")
        return
    
    print(f"App file: {app_file} ✅")
    print(f"Data file: {data_file} ✅")
    
    # Run streamlit with verbose output
    try:
        cmd = [
            "streamlit", "run", 
            app_file, 
            "--server.headless", "true",
            "--server.port", "8504",
            "--logger.level", "debug"
        ]
        
        print(f"Running command: {' '.join(cmd)}")
        
        # Run the command and capture output
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        print("Streamlit process started. Press Ctrl+C to stop.")
        
        # Monitor output
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
        
        # Check for errors
        return_code = process.poll()
        if return_code != 0:
            print(f"Streamlit exited with code {return_code}")
            stderr_output = process.stderr.read()
            if stderr_output:
                print("Error output:")
                print(stderr_output)
        
    except KeyboardInterrupt:
        print("\nStopping Streamlit...")
        process.terminate()
    except Exception as e:
        print(f"Error running Streamlit: {e}")

if __name__ == "__main__":
    run_streamlit_with_debug()
