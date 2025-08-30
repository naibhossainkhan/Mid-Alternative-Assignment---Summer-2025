"""
Demo: Multi-Model AI for Customer Shopping Data Analysis
Demonstrates the use of different AI models (GPT, Gemini, Local LLM) for text generation
"""

import sys
import os
sys.path.append('../src')

import pandas as pd
from core.data import CustomerShoppingDataLoader, load_and_prepare_customer_data
from core.ai import NarrativeGenerator
import sys
import os
sys.path.append('..')
from config import config

def main():
    """Demo the multi-model AI functionality"""
    print("="*80)
    print("🤖 MULTI-MODEL AI DEMO")
    print("="*80)
    print("This demo shows how different AI models generate insights")
    print("for the customer shopping dataset")
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
    
    # Step 3: Test each available model
    print("\n🧪 STEP 3: Testing AI Models")
    print("-" * 60)
    
    for model_name in available_models:
        print(f"\n🔍 Testing {model_name.upper()} Model:")
        print("-" * 40)
        
        try:
            # Initialize narrative generator with specific model
            narrative_gen = NarrativeGenerator(model_name)
            
            # Generate dataset summary
            print(f"   Generating dataset summary with {model_name}...")
            summary = narrative_gen.generate_dataset_summary(data, stats)
            
            # Show first 200 characters of the summary
            preview = summary[:200] + "..." if len(summary) > 200 else summary
            print(f"   Summary preview: {preview}")
            
            # Generate visualization insights
            print(f"   Generating visualization insights with {model_name}...")
            category_data = loader.get_summary_by_category()
            insights = narrative_gen.generate_visualization_insights(
                "bar", category_data.reset_index(), "Revenue by Category", "category", "total_amount"
            )
            
            preview = insights[:150] + "..." if len(insights) > 150 else insights
            print(f"   Insights preview: {preview}")
            
            print(f"   ✅ {model_name.upper()} model working successfully!")
            
        except Exception as e:
            print(f"   ❌ Error with {model_name}: {e}")
    
    # Step 4: Interactive model selection
    print("\n🎯 STEP 4: Interactive Model Selection")
    print("-" * 60)
    
    print("Choose an AI model to generate a detailed analysis:")
    for i, model_name in enumerate(available_models, 1):
        print(f"   {i}. {model_name.upper()}")
    
    print(f"   {len(available_models) + 1}. Test all models")
    
    try:
        choice = input(f"\nEnter your choice (1-{len(available_models) + 1}): ").strip()
        
        if choice.isdigit():
            choice_num = int(choice)
            
            if choice_num == len(available_models) + 1:
                # Test all models
                print("\n🔄 Testing all available models...")
                for model_name in available_models:
                    print(f"\n📝 {model_name.upper()} Analysis:")
                    print("=" * 50)
                    
                    try:
                        narrative_gen = NarrativeGenerator(model_name)
                        summary = narrative_gen.generate_dataset_summary(data, stats)
                        print(summary)
                    except Exception as e:
                        print(f"Error: {e}")
            
            elif 1 <= choice_num <= len(available_models):
                # Test specific model
                selected_model = available_models[choice_num - 1]
                print(f"\n📝 Generating detailed analysis with {selected_model.upper()}:")
                print("=" * 50)
                
                try:
                    narrative_gen = NarrativeGenerator(selected_model)
                    
                    # Generate comprehensive analysis
                    summary = narrative_gen.generate_dataset_summary(data, stats)
                    print("Dataset Summary:")
                    print(summary)
                    
                    print("\n" + "="*50)
                    
                    # Generate trend analysis
                    time_series_data = loader.get_time_series_data()
                    trend_analysis = narrative_gen.generate_trend_analysis(time_series_data, 'total_amount')
                    print("Trend Analysis:")
                    print(trend_analysis)
                    
                    print("\n" + "="*50)
                    
                    # Generate comparative analysis
                    category_data = loader.get_summary_by_category()
                    comp_analysis = narrative_gen.generate_comparative_analysis(
                        category_data.reset_index(), 'category', 'total_amount'
                    )
                    print("Comparative Analysis:")
                    print(comp_analysis)
                    
                except Exception as e:
                    print(f"Error: {e}")
            else:
                print("Invalid choice!")
        else:
            print("Invalid input!")
            
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    
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
    
    print("\nTo change the default model, set the environment variable:")
    print("   export DEFAULT_AI_MODEL='gemini'  # or 'gpt' or 'local'")
    
    print("\n" + "="*80)
    print("🎉 MULTI-MODEL AI DEMO COMPLETED!")
    print("="*80)
    print("\nThe system now supports multiple AI models:")
    print("✅ GPT-3.5-turbo (OpenAI)")
    print("✅ Gemini Pro (Google)")
    print("✅ Local LLM (Template-based)")
    print("\nEach model provides unique insights and analysis capabilities!")

if __name__ == "__main__":
    main()
