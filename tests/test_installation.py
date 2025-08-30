"""
Test Installation Script
Verifies that all dependencies are properly installed and modules can be imported
"""

import sys
import os

def test_imports():
    """Test if all required packages can be imported"""
    print("Testing package imports...")
    
    packages = [
        ('pandas', 'pd'),
        ('numpy', 'np'),
        ('matplotlib.pyplot', 'plt'),
        ('seaborn', 'sns'),
        ('plotly.express', 'px'),
        ('plotly.graph_objects', 'go'),
        ('streamlit', 'st'),
        ('openai', 'openai'),
        ('langchain', 'langchain'),
        ('langchain_openai', 'langchain_openai'),
        ('dotenv', 'dotenv'),
        ('sklearn', 'sklearn'),
        ('scipy', 'scipy'),
        ('requests', 'requests'),
        ('tqdm', 'tqdm')
    ]
    
    failed_imports = []
    
    for package, alias in packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError as e:
            print(f"❌ {package}: {e}")
            failed_imports.append(package)
    
    return failed_imports

def test_custom_modules():
    """Test if our custom modules can be imported"""
    print("\nTesting custom module imports...")
    
    # Add src to path
    sys.path.append('../src')
    
    modules = [
        'customer_data_loader',
        'visualization',
        'narrative_generator',
        'customer_ai_agent'
    ]
    
    failed_modules = []
    
    for module in modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            failed_modules.append(module)
    
    return failed_modules

def test_data_file():
    """Test if the data file exists"""
    print("\nTesting data file...")
    
    data_file = "data/customer_shopping_data.csv"
    
    if os.path.exists(data_file):
        print(f"✅ {data_file} exists")
        return True
    else:
        print(f"❌ {data_file} not found")
        return False

def test_basic_functionality():
    """Test basic functionality without AI components"""
    print("\nTesting basic functionality...")
    
    try:
        # Add src to path
        sys.path.append('../src')
        
        # Import modules
        from customer_data_loader import load_and_prepare_customer_data
        from visualization import DataVisualizer
        
        # Load data
        loader, data = load_and_prepare_customer_data("data/customer_shopping_data.csv")
        print("✅ Data loading successful")
        
        # Test visualization
        visualizer = DataVisualizer()
        print("✅ Visualization module initialized")
        
        # Test basic stats
        stats = loader.get_basic_stats()
        print(f"✅ Basic stats generated: {len(stats)} metrics")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def main():
    """Main test function"""
    print("="*60)
    print("🧪 INSTALLATION TEST")
    print("="*60)
    
    # Test package imports
    failed_packages = test_imports()
    
    # Test custom modules
    failed_modules = test_custom_modules()
    
    # Test data file
    data_ok = test_data_file()
    
    # Test basic functionality
    functionality_ok = test_basic_functionality()
    
    # Summary
    print("\n" + "="*60)
    print("📋 TEST SUMMARY")
    print("="*60)
    
    if not failed_packages and not failed_modules and data_ok and functionality_ok:
        print("🎉 ALL TESTS PASSED!")
        print("\n✅ Installation is complete and ready to use.")
        print("\nNext steps:")
        print("1. Set your OPENAI_API_KEY environment variable")
        print("2. Run: python demo.py")
        print("3. Run: streamlit run streamlit_app.py")
        print("4. Open the Jupyter notebooks in notebooks/ directory")
    else:
        print("⚠️  SOME TESTS FAILED")
        
        if failed_packages:
            print(f"\n❌ Failed package imports: {len(failed_packages)}")
            print("   Install missing packages with: pip install -r requirements.txt")
        
        if failed_modules:
            print(f"\n❌ Failed module imports: {len(failed_modules)}")
            print("   Check that all files in src/ directory exist")
        
        if not data_ok:
            print("\n❌ Data file missing")
            print("   Check that data/sales_data.csv exists")
        
        if not functionality_ok:
            print("\n❌ Basic functionality failed")
            print("   Check the error messages above")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()
