"""
Demo: Textual Summary Generation for Customer Shopping Data
Demonstrates the use of Generative AI to create comprehensive dataset summaries
"""

import sys
import os
sys.path.append('../src')

import pandas as pd
from customer_data_loader import CustomerShoppingDataLoader, load_and_prepare_customer_data
from narrative_generator import NarrativeGenerator

def main():
    """Demo the textual summary generation functionality"""
    print("="*80)
    print("📝 TEXTUAL SUMMARY GENERATION DEMO")
    print("="*80)
    print("This demo shows how Generative AI creates comprehensive summaries")
    print("of the customer shopping dataset using GPT-3.5-turbo")
    print("="*80)
    
    # Step 1: Load and prepare customer shopping data
    print("\n📊 STEP 1: Loading Customer Shopping Data")
    print("-" * 60)
    
    try:
        loader, data = load_and_prepare_customer_data("data/customer_shopping_data.csv")
        print(f"✅ Customer shopping data loaded successfully!")
        print(f"   - Records: {len(data):,}")
        print(f"   - Columns: {len(data.columns)}")
        
        # Get basic statistics
        stats = loader.get_basic_stats()
        print(f"   - Total Revenue: ${stats['total_revenue']:,.2f}")
        print(f"   - Total Customers: {stats['total_customers']:,}")
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return
    
    # Step 2: Initialize Narrative Generator
    print("\n🤖 STEP 2: Initializing Generative AI Components")
    print("-" * 60)
    
    try:
        # Check if OpenAI API key is available
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("⚠️  OpenAI API key not found in environment variables")
            print("   To use Generative AI features, set your API key:")
            print("   export OPENAI_API_KEY='your_api_key_here'")
            print("\n📋 DEMO MODE: Showing what the summary would look like")
            print("-" * 40)
            
            # Show what the summary would contain
            print("📝 SAMPLE TEXTUAL SUMMARY STRUCTURE:")
            print("=" * 50)
            print("""
Dataset Overview:
- This customer shopping dataset contains 99,457 transactions across 10 shopping malls in Turkey
- Data spans from 2021-01-01 to 2023-03-08, providing 2+ years of retail analytics
- Total revenue of $251.5M with average transaction value of $2,528.79

Key Business Metrics:
- 99,457 unique customers with diverse demographic profiles
- 8 product categories ranging from Clothing (45.3% of revenue) to Souvenirs
- 3 payment methods: Cash (44.7%), Credit Card (35.1%), Debit Card (20.2%)
- Average customer age of 43.4 years with balanced gender distribution

Customer Behavior Insights:
- Clothing dominates with $114M in revenue, followed by Shoes ($66.6M) and Technology ($57.9M)
- Mall of Istanbul and Kanyon are top performers with $50M+ revenue each
- Age groups 55+ and 36-45 show highest spending patterns
- Customer segmentation reveals 56% Budget, 28% Regular, 12% Premium, 4% VIP customers

Analytical Opportunities:
- Demographic analysis for targeted marketing strategies
- Mall performance optimization and location-based insights
- Payment behavior trends and financial strategy development
- Seasonal patterns and inventory management optimization
            """)
            
            print("\n🔧 TO ENABLE FULL GENERATIVE AI FEATURES:")
            print("1. Get an OpenAI API key from https://platform.openai.com/")
            print("2. Set environment variable: export OPENAI_API_KEY='your_key'")
            print("3. Run this script again for AI-generated summaries")
            
        else:
            print("✅ OpenAI API key found")
            
            # Initialize narrative generator
            narrative_gen = NarrativeGenerator(api_key)
            print("✅ Narrative generator initialized successfully")
            
            # Step 3: Generate textual summary
            print("\n📝 STEP 3: Generating Textual Summary with Generative AI")
            print("-" * 60)
            
            print("🤖 AI is analyzing the dataset and generating insights...")
            
            try:
                # Generate comprehensive summary
                summary = narrative_gen.generate_dataset_summary(data, stats)
                
                print("✅ AI-Generated Textual Summary:")
                print("=" * 50)
                print(summary)
                print("=" * 50)
                
                # Step 4: Generate additional insights
                print("\n🔍 STEP 4: Generating Additional AI Insights")
                print("-" * 60)
                
                # Generate trend analysis
                time_series_data = loader.get_time_series_data()
                trend_analysis = narrative_gen.generate_trend_analysis(time_series_data, 'total_amount')
                
                print("📈 AI-Generated Trend Analysis:")
                print("-" * 30)
                print(trend_analysis)
                
                # Generate comparative analysis
                category_data = loader.get_summary_by_category()
                comp_analysis = narrative_gen.generate_comparative_analysis(
                    category_data.reset_index(), 'category', 'total_amount'
                )
                
                print("\n📊 AI-Generated Comparative Analysis:")
                print("-" * 30)
                print(comp_analysis)
                
            except Exception as e:
                print(f"❌ Error generating AI insights: {e}")
                print("   This might be due to API rate limits or network issues")
    
    except Exception as e:
        print(f"❌ Error initializing AI components: {e}")
    
    # Step 5: Show dataset statistics for reference
    print("\n📊 STEP 5: Dataset Statistics (For Reference)")
    print("-" * 60)
    
    print("Key Statistics Used for Summary Generation:")
    print(f"   - Total Records: {stats['total_records']:,}")
    print(f"   - Date Range: {stats['date_range']['start']} to {stats['date_range']['end']}")
    print(f"   - Shopping Malls: {len(stats['shopping_malls'])}")
    print(f"   - Product Categories: {len(stats['categories'])}")
    print(f"   - Payment Methods: {len(stats['payment_methods'])}")
    print(f"   - Total Revenue: ${stats['total_revenue']:,.2f}")
    print(f"   - Total Customers: {stats['total_customers']:,}")
    print(f"   - Average Transaction Value: ${stats['average_transaction_value']:,.2f}")
    print(f"   - Average Customer Age: {stats['average_age']:.1f} years")
    
    print("\n" + "="*80)
    print("🎉 TEXTUAL SUMMARY GENERATION DEMO COMPLETED!")
    print("="*80)
    print("\nThe Generative AI system is designed to:")
    print("✅ Analyze customer shopping patterns and behavior")
    print("✅ Generate comprehensive business insights")
    print("✅ Provide actionable recommendations for retail analytics")
    print("✅ Create narrative explanations for data visualizations")
    print("\nTo enable full AI features, set your OpenAI API key and run again!")

if __name__ == "__main__":
    main()
