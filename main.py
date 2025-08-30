#!/usr/bin/env python3
"""
Main Entry Point for AI-Powered Customer Shopping Analytics
Data Visualization Assignment - Summer 2025
"""

import sys
import os
import argparse
from pathlib import Path

def main():
    """Main entry point with command-line interface"""
    parser = argparse.ArgumentParser(
        description="AI-Powered Customer Shopping Analytics",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py streamlit          # Run Streamlit app
  python main.py demo               # Run demo workflow
  python main.py test               # Run tests
  python main.py --help             # Show this help
        """
    )
    
    parser.add_argument(
        'command',
        choices=['streamlit', 'demo', 'test', 'install'],
        help='Command to execute'
    )
    
    parser.add_argument(
        '--simple',
        action='store_true',
        help='Use simple version (no LangChain dependencies)'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=8501,
        help='Port for Streamlit app (default: 8501)'
    )
    
    args = parser.parse_args()
    
    if args.command == 'streamlit':
        run_streamlit(args.simple, args.port)
    elif args.command == 'demo':
        run_demo(args.simple)
    elif args.command == 'test':
        run_tests()
    elif args.command == 'install':
        install_dependencies()

def run_streamlit(simple=True, port=8501):
    """Run Streamlit application"""
    import subprocess
    import sys
    
    if simple:
        app_file = "streamlit/streamlit_app_simple.py"
    else:
        app_file = "streamlit/streamlit_app.py"
    
    if not os.path.exists(app_file):
        print(f"❌ Streamlit app not found: {app_file}")
        sys.exit(1)
    
    print(f"🚀 Starting Streamlit app: {app_file}")
    print(f"🌐 URL: http://localhost:{port}")
    print("Press Ctrl+C to stop")
    
    try:
        # Set PYTHONPATH to include src directory
        env = os.environ.copy()
        env['PYTHONPATH'] = os.path.join(os.getcwd(), 'src') + os.pathsep + env.get('PYTHONPATH', '')
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", app_file,
            "--server.port", str(port),
            "--server.address", "localhost"
        ], env=env)
    except KeyboardInterrupt:
        print("\n👋 Streamlit app stopped")

def run_demo(simple=True):
    """Run demo workflow"""
    import subprocess
    import sys
    
    if simple:
        demo_file = "demos/demo_agentic_workflow_simple.py"
    else:
        demo_file = "demos/demo_agentic_workflow.py"
    
    if not os.path.exists(demo_file):
        print(f"❌ Demo file not found: {demo_file}")
        sys.exit(1)
    
    print(f"🎯 Running demo: {demo_file}")
    
    try:
        # Set PYTHONPATH to include src directory
        env = os.environ.copy()
        env['PYTHONPATH'] = os.path.join(os.getcwd(), 'src') + os.pathsep + env.get('PYTHONPATH', '')
        subprocess.run([sys.executable, demo_file], env=env)
    except KeyboardInterrupt:
        print("\n👋 Demo stopped")

def run_tests():
    """Run test suite"""
    import subprocess
    import sys
    
    test_file = "tests/test_installation.py"
    
    if not os.path.exists(test_file):
        print(f"❌ Test file not found: {test_file}")
        sys.exit(1)
    
    print("🧪 Running test suite...")
    
    try:
        # Set PYTHONPATH to include src directory
        env = os.environ.copy()
        env['PYTHONPATH'] = os.path.join(os.getcwd(), 'src') + os.pathsep + env.get('PYTHONPATH', '')
        result = subprocess.run([sys.executable, test_file], env=env)
        if result.returncode == 0:
            print("✅ All tests passed!")
        else:
            print("❌ Some tests failed")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        sys.exit(1)

def install_dependencies():
    """Install project dependencies"""
    import subprocess
    import sys
    
    print("📦 Installing dependencies...")
    
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True)
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
