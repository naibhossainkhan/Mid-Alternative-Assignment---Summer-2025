"""
Streamlit Web Application for AI-Powered Data Analytics
Demonstrates Agentic AI workflow with natural language query processing
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os
from datetime import datetime
import time

# Add src to path
sys.path.append('src')

# Import our custom modules
from customer_data_loader import CustomerShoppingDataLoader, load_and_prepare_customer_data
from narrative_generator import NarrativeGenerator
from visualization import DataVisualizer
from customer_ai_agent import CustomerShoppingAgent

# Page configuration
st.set_page_config(
    page_title="AI-Powered Customer Shopping Analytics",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2ca02c;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .ai-insight {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ff7f0e;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and cache the customer shopping data"""
    try:
        loader, cleaned_data = load_and_prepare_customer_data("data/customer_shopping_data.csv")
        return loader, cleaned_data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None

def initialize_ai_components():
    """Initialize AI components"""
    try:
        narrative_gen = NarrativeGenerator()
        return narrative_gen
    except Exception as e:
        st.warning(f"AI components not available: {e}")
        return None

def display_metrics(data):
    """Display key metrics"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_revenue = data['total_amount'].sum()
        st.metric("Total Revenue", f"${total_revenue:,.0f}")
    
    with col2:
        total_transactions = len(data)
        st.metric("Total Transactions", f"{total_transactions:,}")
    
    with col3:
        avg_transaction = data['total_amount'].mean()
        st.metric("Avg Transaction Value", f"${avg_transaction:,.0f}")
    
    with col4:
        total_customers = data['customer_id'].nunique()
        st.metric("Unique Customers", f"{total_customers:,}")

def create_customer_dashboard(data):
    """Create comprehensive customer shopping dashboard"""
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Revenue by Category', 'Revenue by Shopping Mall', 
                      'Daily Revenue Trend', 'Spending by Age Group'),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "scatter"}, {"type": "bar"}]]
    )
    
    # Chart 1: Revenue by Category
    category_revenue = data.groupby('category')['total_amount'].sum().reset_index()
    fig.add_trace(
        go.Bar(x=category_revenue['category'], y=category_revenue['total_amount'], 
               name='Revenue by Category', marker_color='#1f77b4'),
        row=1, col=1
    )
    
    # Chart 2: Revenue by Shopping Mall
    mall_revenue = data.groupby('shopping_mall')['total_amount'].sum().reset_index()
    fig.add_trace(
        go.Bar(x=mall_revenue['shopping_mall'], y=mall_revenue['total_amount'], 
               name='Revenue by Mall', marker_color='#ff7f0e'),
        row=1, col=2
    )
    
    # Chart 3: Daily Revenue Trend
    daily_revenue = data.groupby('invoice_date')['total_amount'].sum().reset_index()
    fig.add_trace(
        go.Scatter(x=daily_revenue['invoice_date'], y=daily_revenue['total_amount'], 
                  mode='lines+markers', name='Daily Revenue', line_color='#2ca02c'),
        row=2, col=1
    )
    
    # Chart 4: Spending by Age Group
    age_spending = data.groupby('age_group')['total_amount'].sum().reset_index()
    fig.add_trace(
        go.Bar(x=age_spending['age_group'], y=age_spending['total_amount'], 
               name='Spending by Age', marker_color='#d62728'),
        row=2, col=2
    )
    
    fig.update_layout(
        title_text="Customer Shopping Analytics Dashboard",
        showlegend=False,
        height=600
    )
    
    return fig

def main():
    """Main application function"""
    
    # Header
    st.markdown('<h1 class="main-header">🛍️ AI-Powered Customer Shopping Analytics</h1>', unsafe_allow_html=True)
    st.markdown("### Generative AI + Agentic AI for Customer Shopping Data Analytics and Visualization")
    
    # Load data
    with st.spinner("Loading data..."):
        loader, data = load_data()
    
    if data is None:
        st.error("Failed to load data. Please check the data file.")
        return
    
    # Initialize AI components
    narrative_gen = initialize_ai_components()
    
    # Sidebar
    st.sidebar.title("📊 Analytics Options")
    
    # Main content
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Dashboard", "🤖 AI Agent", "🔍 Query Analysis", "📋 Data Explorer"])
    
    with tab1:
        st.markdown('<h2 class="sub-header">Customer Shopping Analytics Dashboard</h2>', unsafe_allow_html=True)
        
        # Display metrics
        display_metrics(data)
        
        # Create dashboard
        dashboard_fig = create_customer_dashboard(data)
        st.plotly_chart(dashboard_fig, use_container_width=True)
        
        # AI-generated insights
        if narrative_gen:
            with st.expander("🤖 AI-Generated Dashboard Insights"):
                try:
                    insights = narrative_gen.generate_visualization_insights(
                        "dashboard", data, "Customer Shopping Analytics Dashboard", "category", "total_amount"
                    )
                    st.markdown(f'<div class="ai-insight">{insights}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error generating insights: {e}")
    
    with tab2:
        st.markdown('<h2 class="sub-header">Agentic AI Workflow</h2>', unsafe_allow_html=True)
        
        if narrative_gen:
            # Initialize AI agent
            try:
                visualizer = DataVisualizer()
                agent = CustomerShoppingAgent(data, visualizer, narrative_gen)
                
                st.markdown("### Natural Language Query Interface")
                st.markdown("Ask questions about your data in natural language:")
                
                # Query input
                query = st.text_input(
                    "Enter your query:",
                    placeholder="e.g., Show me revenue trends by category"
                )
                
                if st.button("🚀 Analyze with AI Agent"):
                    if query:
                        with st.spinner("AI Agent is processing your query..."):
                            result = agent.process_query(query)
                            
                            if result["success"]:
                                st.success("✅ Analysis completed successfully!")
                                
                                # Display results
                                col1, col2 = st.columns([1, 1])
                                
                                with col1:
                                    st.markdown("### 📊 Agent Response")
                                    st.write(result["agent_response"])
                                
                                with col2:
                                    st.markdown("### ⏱️ Performance")
                                    st.metric("Execution Time", f"{result['execution_time']:.2f}s")
                                
                                # AI insights
                                st.markdown("### 🤖 AI-Generated Insights")
                                st.markdown(f'<div class="ai-insight">{result["insights"]}</div>', unsafe_allow_html=True)
                                
                                # Generate visualization
                                st.markdown("### 📈 Generated Visualization")
                                viz_result = agent.generate_visualization_pipeline(query)
                                
                                if viz_result["chart_type"] == "line":
                                    fig = visualizer.create_line_chart(
                                        viz_result["data"], 
                                        viz_result["data"].columns[0], 
                                        viz_result["data"].columns[1], 
                                        viz_result["title"],
                                        "plotly"
                                    )
                                elif viz_result["chart_type"] == "bar":
                                    fig = visualizer.create_bar_chart(
                                        viz_result["data"], 
                                        viz_result["data"].columns[0], 
                                        viz_result["data"].columns[1], 
                                        viz_result["title"],
                                        "plotly"
                                    )
                                elif viz_result["chart_type"] == "pie":
                                    fig = visualizer.create_pie_chart(
                                        viz_result["data"], 
                                        viz_result["data"].columns[1], 
                                        viz_result["data"].columns[0], 
                                        viz_result["title"],
                                        "plotly"
                                    )
                                else:
                                    fig = visualizer.create_bar_chart(
                                        viz_result["data"], 
                                        viz_result["data"].columns[0], 
                                        viz_result["data"].columns[1], 
                                        viz_result["title"],
                                        "plotly"
                                    )
                                
                                st.plotly_chart(fig, use_container_width=True)
                                
                            else:
                                st.error("❌ Analysis failed. Please try a different query.")
                                st.write(result["agent_response"])
                    else:
                        st.warning("Please enter a query to analyze.")
                
                # Predefined queries
                st.markdown("### 💡 Example Queries")
                example_queries = [
                    "Show me revenue trends by category",
                    "What are the most popular shopping malls?",
                    "Show me spending analysis by gender",
                    "Give me a summary of the customer shopping data",
                    "What are the customer spending patterns by age group?"
                ]
                
                for i, example in enumerate(example_queries):
                    if st.button(f"Query {i+1}: {example}", key=f"query_{i}"):
                        st.session_state.query = example
                        st.rerun()
                
            except Exception as e:
                st.error(f"Error initializing AI agent: {e}")
        else:
            st.warning("AI components not available. Please check your API configuration.")
    
    with tab3:
        st.markdown('<h2 class="sub-header">Advanced Query Analysis</h2>', unsafe_allow_html=True)
        
        if narrative_gen:
            # Time series analysis
            st.markdown("### 📈 Time Series Analysis")
            
            metric_options = ['total_amount', 'quantity', 'price']
            selected_metric = st.selectbox("Select metric for trend analysis:", metric_options)
            
            if st.button("Generate Trend Analysis"):
                with st.spinner("Analyzing trends..."):
                    time_series_data = loader.get_time_series_data()
                    
                    # Create trend chart
                    fig = px.line(time_series_data, x='invoice_date', y=selected_metric, 
                                title=f'{selected_metric} Trend Over Time')
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Generate AI insights
                    try:
                        trend_insights = narrative_gen.generate_trend_analysis(time_series_data, selected_metric)
                        st.markdown("### 🤖 AI Trend Analysis")
                        st.markdown(f'<div class="ai-insight">{trend_insights}</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error generating trend insights: {e}")
            
            # Comparative analysis
            st.markdown("### 🔍 Comparative Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                group_by = st.selectbox("Group by:", ['category', 'shopping_mall', 'gender', 'age_group', 'payment_method'])
            
            with col2:
                compare_metric = st.selectbox("Compare by:", ['total_amount', 'quantity', 'price'])
            
            if st.button("Generate Comparative Analysis"):
                with st.spinner("Generating comparative analysis..."):
                    # Get grouped data
                    grouped_data = data.groupby(group_by)[compare_metric].agg(['sum', 'mean', 'count']).reset_index()
                    
                    # Create comparison chart
                    fig = px.bar(grouped_data, x=group_by, y='sum', 
                               title=f'{compare_metric} by {group_by}')
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Generate AI insights
                    try:
                        comp_insights = narrative_gen.generate_comparative_analysis(
                            grouped_data, group_by, 'sum'
                        )
                        st.markdown("### 🤖 AI Comparative Analysis")
                        st.markdown(f'<div class="ai-insight">{comp_insights}</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error generating comparative insights: {e}")
        else:
            st.warning("AI components not available for advanced analysis.")
    
    with tab4:
        st.markdown('<h2 class="sub-header">Data Explorer</h2>', unsafe_allow_html=True)
        
        # Data overview
        st.markdown("### 📋 Dataset Overview")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Dataset Information:**")
            st.write(f"- **Records:** {len(data):,}")
            st.write(f"- **Columns:** {len(data.columns)}")
            st.write(f"- **Date Range:** {data['invoice_date'].min().strftime('%Y-%m-%d')} to {data['invoice_date'].max().strftime('%Y-%m-%d')}")
        
        with col2:
            st.markdown("**Data Dimensions:**")
            st.write(f"- **Shopping Malls:** {data['shopping_mall'].nunique()}")
            st.write(f"- **Product Categories:** {data['category'].nunique()}")
            st.write(f"- **Payment Methods:** {data['payment_method'].nunique()}")
        
        # Data preview
        st.markdown("### 📊 Data Preview")
        preview_rows = st.slider("Number of rows to display:", 5, 50, 10)
        st.dataframe(data.head(preview_rows), use_container_width=True)
        
        # Statistical summary
        st.markdown("### 📈 Statistical Summary")
        st.dataframe(data.describe(), use_container_width=True)
        
        # Data quality check
        st.markdown("### 🔍 Data Quality Check")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Missing Values:**")
            missing_data = data.isnull().sum()
            if missing_data.sum() == 0:
                st.success("✅ No missing values found!")
            else:
                st.dataframe(missing_data[missing_data > 0])
        
        with col2:
            st.markdown("**Data Types:**")
            st.dataframe(data.dtypes.to_frame('Data Type'))
        
        # AI-generated dataset summary
        if narrative_gen:
            with st.expander("🤖 AI-Generated Dataset Summary"):
                try:
                    stats = loader.get_basic_stats()
                    ai_summary = narrative_gen.generate_dataset_summary(data, stats)
                    st.markdown(f'<div class="ai-insight">{ai_summary}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error generating dataset summary: {e}")

if __name__ == "__main__":
    main()
