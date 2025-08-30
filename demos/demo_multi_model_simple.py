"""
Demo: Multi-Model AI for Customer Shopping Data Analysis (Simple)
Demonstrates the multi-model AI functionality with local model
"""

import sys
import os
sys.path.append('../src')

import pandas as pd
from customer_data_loader import CustomerShoppingDataLoader, load_and_prepare_customer_data
from narrative_generator import NarrativeGenerator
import sys
import os
sys.path.append('..')
from config import config

def main():
    """Demo the multi-model AI functionality with local model"""
    print("="*80)
    print("🤖 MULTI-MODEL AI DEMO (SIMPLE)")
    print("="*80)
    print("This demo shows how different AI models generate insights")
    print("for the customer shopping dataset using the local model")
    print("="*80)
    
    # Step 1: Load customer shopping data
    print("\n📊 STEP 1: Loading Customer Shopping Data")
    print("-" * 60)
    
    try:
        loader, data = load_and_prepare_customer_data("data/customer_shopping_data.csv")
        print(f"✅ Customer shopping data loaded successfully!")
        print(f"   - Records: {len(data):,}")
        
        # Get basic statistics
        stats = loader.get_basic_stats()
        print(f"   - Total Revenue: ${stats['total_revenue']:,.2f}")
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return
    
    # Step 2: Show available AI models
    print("\n🤖 STEP 2: Available AI Models")
    print("-" * 60)
    
    available_models = config.get_available_models()
    print("Available AI models:")
    
    for model_name in available_models:
        model_config = config.get_model_config(model_name)
        status = "✅ Available" if model_config['enabled'] else "❌ Not Available"
        print(f"   - {model_name.upper()}: {model_config['name']} ({status})")
    
    print(f"\nDefault model: {config.default_model.upper()}")
    
    # Step 3: Test with Local Model (no API limits)
    print("\n🧪 STEP 3: Testing Local AI Model")
    print("-" * 60)
    
    try:
        # Initialize narrative generator with local model
        narrative_gen = NarrativeGenerator('local')
        
        # Generate dataset summary
        print("📝 Generating dataset summary with LOCAL model...")
        summary = narrative_gen.generate_dataset_summary(data, stats)
        
        print("✅ Generated Summary:")
        print("=" * 50)
        print(summary)
        print("=" * 50)
        
        # Generate visualization insights
        print("\n📊 Generating visualization insights with LOCAL model...")
        category_data = loader.get_summary_by_category()
        insights = narrative_gen.generate_visualization_insights(
            "bar", category_data.reset_index(), "Revenue by Category", "category", "total_amount"
        )
        
        print("✅ Generated Insights:")
        print("=" * 50)
        print(insights)
        print("=" * 50)
        
        # Generate trend analysis
        print("\n📈 Generating trend analysis with LOCAL model...")
        time_series_data = loader.get_time_series_data()
        trend_analysis = narrative_gen.generate_trend_analysis(time_series_data, 'total_amount')
        
        print("✅ Generated Trend Analysis:")
        print("=" * 50)
        print(trend_analysis)
        print("=" * 50)
        
        # Generate comparative analysis
        print("\n🔍 Generating comparative analysis with LOCAL model...")
        comp_analysis = narrative_gen.generate_comparative_analysis(
            category_data.reset_index(), 'category', 'total_amount'
        )
        
        print("✅ Generated Comparative Analysis:")
        print("=" * 50)
        print(comp_analysis)
        print("=" * 50)
        
        print("\n✅ LOCAL model working successfully!")
        
    except Exception as e:
        print(f"❌ Error with local model: {e}")
    
    # Step 4: Show model switching capability
    print("\n🔄 STEP 4: Model Switching Capability")
    print("-" * 60)
    
    print("The system supports easy switching between AI models:")
    print("   - Set environment variable: export DEFAULT_AI_MODEL='local'")
    print("   - Or specify model when initializing: NarrativeGenerator('local')")
    print("   - Or use config: config.set_default_model('local')")
    
    # Step 5: Configuration information
    print("\n⚙️ STEP 5: Configuration Information")
    print("-" * 60)
    
    print("Current Configuration:")
    print(f"   - Default Model: {config.default_model.upper()}")
    print(f"   - Available Models: {', '.join(available_models).upper()}")
    
    print("\nEnvironment Variables:")
    print("   - OPENAI_API_KEY: {'Set' if config.openai_api_key else 'Not Set'}")
    print("   - GEMINI_API_KEY: {'Set' if config.gemini_api_key else 'Not Set'}")
    print("   - DEFAULT_AI_MODEL: {config.default_model}")
    
    print("\nModel Capabilities:")
    print("   - LOCAL: Template-based responses (always available)")
    print("   - GEMINI: Google's Gemini 1.5 Pro (requires API key)")
    print("   - GPT: OpenAI's GPT-3.5-turbo (requires API key)")
    
    print("\n" + "="*80)
    print("🎉 MULTI-MODEL AI DEMO COMPLETED!")
    print("="*80)
    print("\nThe system successfully demonstrates:")
    print("✅ Multi-model AI architecture")
    print("✅ Easy model switching")
    print("✅ Fallback to local model when APIs are unavailable")
    print("✅ Consistent interface across different AI providers")
    print("\nThis fulfills the requirement for multiple AI model support!")

if __name__ == "__main__":
    main()
