"""
Simplified Streamlit Web Application for AI-Powered Data Analytics
Demonstrates Agentic AI workflow without LangChain dependencies
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
    /* Global text color improvements */
    * {
        color: #1f2937 !important;
    }
    
    /* Set white background only for main content area, not sidebar */
    .main {
        background-color: #ffffff !important;
    }
    
    .block-container {
        background-color: #ffffff !important;
    }
    
    /* Main content area only */
    .main .block-container {
        background-color: #ffffff !important;
    }
    
    /* Exclude sidebar from white background */
    .css-1d391kg {
        background-color: #f8f9fa !important;
    }
    
    /* Main headers */
    .main-header {
        font-size: 3rem;
        color: #1f77b4 !important;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    /* Mobile responsive header */
    @media (max-width: 768px) {
        .main-header {
            font-size: 1.5rem !important;
            margin-bottom: 1rem !important;
            padding: 0.5rem !important;
        }
        
        .sub-header {
            font-size: 1.2rem !important;
            margin-bottom: 0.5rem !important;
        }
        
        h1 {
            font-size: 1.5rem !important;
        }
        
        h2 {
            font-size: 1.3rem !important;
        }
        
        h3 {
            font-size: 1.1rem !important;
        }
    }
    
    /* Extra small mobile devices */
    @media (max-width: 480px) {
        .main-header {
            font-size: 1.2rem !important;
            margin-bottom: 0.5rem !important;
            padding: 0.25rem !important;
        }
        
        .sub-header {
            font-size: 1rem !important;
        }
        
        h1 {
            font-size: 1.3rem !important;
        }
        
        h2 {
            font-size: 1.1rem !important;
        }
        
        h3 {
            font-size: 1rem !important;
        }
    }
    
    .sub-header {
        font-size: 1.5rem;
        color: #2ca02c !important;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    /* All headers with proper contrast */
    h1, h2, h3, h4, h5, h6 {
        color: #1f2937 !important;
        font-weight: 600;
        background-color: #f8f9fa;
        padding: 0.75rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    
    h1 {
        font-size: 2rem;
        background-color: #e3f2fd;
        border-left-color: #1976d2;
    }
    
    h2 {
        font-size: 1.75rem;
        background-color: #f3e5f5;
        border-left-color: #7b1fa2;
    }
    
    h3 {
        font-size: 1.5rem;
        background-color: #e8f5e8;
        border-left-color: #388e3c;
    }
    
    /* Metric cards */
    .metric-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 2px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* AI insights with better contrast */
    .ai-insight {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 2px solid #1f77b4;
        margin: 1rem 0;
        color: #1f2937 !important;
        font-size: 1rem;
        line-height: 1.6;
        font-weight: 400;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Query results */
    .query-result {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 2px solid #e0e0e0;
        margin: 0.5rem 0;
        color: #1f2937 !important;
        font-size: 0.95rem;
        line-height: 1.5;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .query-result code {
        background-color: #f8f9fa;
        padding: 0.3rem 0.6rem;
        border-radius: 0.25rem;
        font-family: 'Courier New', monospace;
        color: #d63384 !important;
        font-size: 0.9rem;
        border: 1px solid #e0e0e0;
    }
    
    /* Streamlit specific elements */
    .stMarkdown {
        color: #1f2937 !important;
    }
    
    .stMarkdown p {
        color: #1f2937 !important;
        font-size: 1rem;
        line-height: 1.6;
    }
    
    .stMarkdown strong {
        color: #1f2937 !important;
        font-weight: 600;
    }
    
    /* Modern button styling with high contrast text */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: #ffffff !important;
        border: none !important;
        padding: 0.75rem 1.5rem;
        border-radius: 10px;
        font-weight: 700;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        width: 100%;
        margin: 0.25rem 0;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%) !important;
        color: #ffffff !important;
    }
    
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
    }
    
    /* Sidebar button specific styling - ensure all buttons are visible */
    .css-1d391kg .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: #ffffff !important;
        border-radius: 8px;
        font-size: 0.9rem;
        font-weight: 600;
        padding: 0.6rem 1rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        border: 2px solid transparent !important;
    }
    
    .css-1d391kg .stButton > button:hover {
        background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%) !important;
        color: #ffffff !important;
        transform: translateY(-1px);
        border: 2px solid #ffffff !important;
    }
    
    /* Override any default Streamlit button styles that might be causing issues */
    .css-1d391kg button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    .css-1d391kg button:hover {
        background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%) !important;
        color: #ffffff !important;
    }
    
    /* Ensure all sidebar text elements are visible */
    .css-1d391kg .stMarkdown {
        color: #1f2937 !important;
    }
    
    .css-1d391kg .stMarkdown p {
        color: #1f2937 !important;
    }
    
    .css-1d391kg .stMarkdown strong {
        color: #1f2937 !important;
    }
    
    /* Ensure all button text is visible */
    button {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* Override any conflicting styles */
    .stButton > button > span {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* Force all button text to be white and visible */
    button, button *, button span, button div {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* Specific sidebar button text visibility */
    .css-1d391kg button, 
    .css-1d391kg button *, 
    .css-1d391kg button span, 
    .css-1d391kg button div {
        color: #ffffff !important;
        font-weight: 600 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3) !important;
    }
    
    /* Ensure button text is always visible regardless of state */
    .stButton button,
    .stButton button *,
    .stButton button span,
    .stButton button div {
        color: #ffffff !important;
        font-weight: 600 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3) !important;
    }
    
    /* Text inputs */
    .stTextInput > div > div > input {
        background-color: #ffffff;
        color: #1f2937 !important;
        border: 2px solid #e0e0e0;
        border-radius: 0.25rem;
    }
    
    /* Sidebar improvements */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    .css-1d391kg .stMarkdown {
        color: #1f2937 !important;
    }
    
    /* Success, info, warning messages */
    .stAlert {
        background-color: #d4edda;
        border-color: #c3e6cb;
        color: #155724 !important;
    }
    
    .stAlert[data-baseweb="notification"] {
        background-color: #d1ecf1;
        border-color: #bee5eb;
        color: #0c5460 !important;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 0.25rem;
    }
    
    /* Ensure all text is readable */
    div, span, p, label, strong, em, b, i {
        color: #1f2937 !important;
    }
    
    /* Code blocks */
    pre, code {
        background-color: #f8f9fa;
        color: #d63384 !important;
        border: 1px solid #e0e0e0;
        border-radius: 0.25rem;
        padding: 0.25rem 0.5rem;
    }
    
    /* Menu styling - simple and effective */
    .stDeployButton .menu *,
    .stDeployButton .menu li,
    .stDeployButton .menu a,
    .stDeployButton .menu span,
    .stDeployButton .menu div,
    .stDeployButton .menu button {
        color: #ffffff !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        font-weight: 600 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3) !important;
        border-radius: 8px !important;
        padding: 0.6rem 1rem !important;
        margin: 0.25rem 0 !important;
        transition: all 0.3s ease !important;
        border: 2px solid transparent !important;
    }
    
    .stDeployButton .menu *:hover,
    .stDeployButton .menu li:hover,
    .stDeployButton .menu a:hover,
    .stDeployButton .menu span:hover,
    .stDeployButton .menu div:hover,
    .stDeployButton .menu button:hover {
        background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%) !important;
        color: #ffffff !important;
        transform: translateY(-1px) !important;
        border: 2px solid #ffffff !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
    }
    
    /* Popover container background */
    .stDeployButton .menu {
        background-color: #f8f9fa !important;
        border: 1px solid #e0e0e0 !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
        padding: 0.5rem !important;
    }
</style>
""", unsafe_allow_html=True)

class SimpleAgenticWorkflow:
    """Simplified agentic workflow for Streamlit app"""
    
    def __init__(self, data: pd.DataFrame, visualizer, narrative_generator):
        self.data = data
        self.visualizer = visualizer
        self.narrative_generator = narrative_generator
    
    def translate_query_to_pandas(self, query: str) -> str:
        """Translate natural language query to Pandas code"""
        query_lower = query.lower()
        
        # Sales and revenue analysis
        if "revenue" in query_lower or "sales" in query_lower:
            if "trend" in query_lower and "category" in query_lower:
                return "df.groupby(['invoice_date', 'category'])['total_amount'].sum().reset_index()"
            elif "category" in query_lower:
                return "df.groupby('category')['total_amount'].sum().reset_index()"
            elif "mall" in query_lower or "shopping" in query_lower:
                return "df.groupby('shopping_mall')['total_amount'].sum().reset_index()"
            elif "gender" in query_lower:
                return "df.groupby('gender')['total_amount'].sum().reset_index()"
            elif "age" in query_lower:
                return "df.groupby('age_group')['total_amount'].sum().reset_index()"
            elif "trend" in query_lower:
                return "df.groupby('invoice_date')['total_amount'].sum().reset_index()"
            else:
                return "df.groupby('category')['total_amount'].sum().reset_index()"
        
        # Category analysis
        elif "category" in query_lower:
            if "popular" in query_lower or "most" in query_lower:
                return "df.groupby('category').size().reset_index(name='count').sort_values('count', ascending=False)"
            else:
                return "df.groupby('category')['total_amount'].sum().reset_index()"
        
        # Shopping mall analysis
        elif "mall" in query_lower or "shopping" in query_lower:
            if "popular" in query_lower or "most" in query_lower:
                return "df.groupby('shopping_mall').size().reset_index(name='count').sort_values('count', ascending=False)"
            else:
                return "df.groupby('shopping_mall')['total_amount'].sum().reset_index()"
        
        # Gender analysis
        elif "gender" in query_lower:
            if "spending" in query_lower:
                return "df.groupby('gender')['total_amount'].sum().reset_index()"
            else:
                return "df.groupby('gender').size().reset_index(name='count')"
        
        # Age analysis
        elif "age" in query_lower:
            if "spending" in query_lower:
                return "df.groupby('age_group')['total_amount'].sum().reset_index()"
            else:
                return "df.groupby('age_group').size().reset_index(name='count')"
        
        # Payment method analysis
        elif "payment" in query_lower:
            return "df.groupby('payment_method')['total_amount'].sum().reset_index()"
        
        # Summary statistics
        elif "summary" in query_lower or "overview" in query_lower:
            return "summary_stats = {'total_revenue': df['total_amount'].sum(), 'total_transactions': len(df), 'total_customers': df['customer_id'].nunique()}"
        
        # Default to revenue analysis
        else:
            return "df.groupby('category')['total_amount'].sum().reset_index()"
    
    def execute_query(self, query: str) -> dict:
        """Execute a natural language query and return results"""
        start_time = time.time()
        
        try:
            # Step 1: Translate query to Pandas code
            pandas_code = self.translate_query_to_pandas(query)
            
            # Step 2: Execute the Pandas code
            local_vars = {'df': self.data, 'pd': pd}
            exec(f"result = {pandas_code}", globals(), local_vars)
            result = local_vars.get('result', None)
            
            # Step 3: Generate insights
            insights = self.narrative_generator.generate_query_analysis(
                query, 
                self.data if result is None else (result if isinstance(result, pd.DataFrame) else pd.DataFrame()),
                time.time() - start_time
            )
            
            # Step 4: Generate visualization
            viz_result = self.generate_visualization(query, result)
            
            return {
                "query": query,
                "pandas_code": pandas_code,
                "result": result,
                "insights": insights,
                "visualization": viz_result,
                "execution_time": time.time() - start_time,
                "success": True
            }
            
        except Exception as e:
            return {
                "query": query,
                "pandas_code": "Error in translation",
                "result": None,
                "insights": f"Error processing query: {str(e)}",
                "visualization": None,
                "execution_time": time.time() - start_time,
                "success": False
            }
    
    def generate_visualization(self, query: str, data) -> dict:
        """Generate visualization based on query and data"""
        try:
            query_lower = query.lower()
            
            if data is None or not isinstance(data, pd.DataFrame):
                # Default visualization
                data = self.data.groupby('category')['total_amount'].sum().reset_index()
                chart_type = "bar"
                title = "Revenue by Category"
            elif "trend" in query_lower:
                chart_type = "line"
                if len(data.columns) >= 2:
                    title = f"Trend Analysis: {data.columns[1]} over time"
                else:
                    title = "Trend Analysis"
            elif "category" in query_lower:
                chart_type = "bar"
                title = "Category Analysis"
            elif "mall" in query_lower or "shopping" in query_lower:
                chart_type = "bar"
                title = "Shopping Mall Analysis"
            elif "gender" in query_lower:
                chart_type = "bar"
                title = "Gender Analysis"
            elif "age" in query_lower:
                chart_type = "bar"
                title = "Age Group Analysis"
            elif "distribution" in query_lower or "pie" in query_lower:
                chart_type = "pie"
                title = "Distribution Analysis"
            else:
                chart_type = "bar"
                title = "Data Analysis"
            
            # Create visualization
            if chart_type == "line" and len(data.columns) >= 2:
                fig = self.visualizer.create_line_chart(data, data.columns[0], data.columns[1], title)
            elif chart_type == "bar" and len(data.columns) >= 2:
                fig = self.visualizer.create_bar_chart(data, data.columns[0], data.columns[1], title)
            elif chart_type == "pie" and len(data.columns) >= 2:
                fig = self.visualizer.create_pie_chart(data, data.columns[1], data.columns[0])
            else:
                # Fallback to bar chart
                if len(data.columns) >= 2:
                    fig = self.visualizer.create_bar_chart(data, data.columns[0], data.columns[1], title)
                else:
                    fig = None
            
            return {
                "chart_type": chart_type,
                "title": title,
                "figure": fig,
                "data_shape": data.shape if isinstance(data, pd.DataFrame) else "N/A"
            }
            
        except Exception as e:
            return {
                "chart_type": "error",
                "title": "Error generating visualization",
                "figure": None,
                "data_shape": "N/A",
                "error": str(e)
            }

@st.cache_data(show_spinner="Loading customer shopping data...")
def load_data():
    """Load and cache the customer shopping data with Streamlit optimization"""
    try:
        loader, cleaned_data = load_and_prepare_customer_data("data/customer_shopping_data.csv")
        
        # Additional optimization for Streamlit display
        if cleaned_data is not None:
            # Convert datetime to string for display compatibility
            if 'invoice_date' in cleaned_data.columns:
                cleaned_data['invoice_date_display'] = cleaned_data['invoice_date'].dt.strftime('%Y-%m-%d')
            
            # Ensure all categorical columns are strings for Arrow compatibility
            categorical_columns = ['shopping_mall', 'category', 'payment_method', 'gender', 'age_group', 'spending_category']
            for col in categorical_columns:
                if col in cleaned_data.columns:
                    cleaned_data[col] = cleaned_data[col].astype('string')
            
            # Convert numeric columns to appropriate types
            numeric_columns = ['quantity', 'price', 'total_amount', 'age', 'month', 'year', 'quarter']
            for col in numeric_columns:
                if col in cleaned_data.columns:
                    if cleaned_data[col].dtype == 'int64':
                        cleaned_data[col] = cleaned_data[col].astype('int32')
                    elif cleaned_data[col].dtype == 'float64':
                        cleaned_data[col] = cleaned_data[col].astype('float32')
        
        return loader, cleaned_data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None

def initialize_ai_components(selected_model='local'):
    """Initialize AI components with selected model"""
    try:
        narrative_gen = NarrativeGenerator(selected_model)
        return narrative_gen
    except Exception as e:
        st.warning(f"AI components not available for {selected_model}: {e}")
        # Fallback to local model
        try:
            st.info(f"Falling back to Local LLM...")
            narrative_gen = NarrativeGenerator('local')
            return narrative_gen
        except Exception as fallback_error:
            st.error(f"Failed to initialize any AI model: {fallback_error}")
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
    """Create customer shopping dashboard"""
    st.markdown("### 📊 Customer Shopping Dashboard")
    
    # Revenue by Category
    col1, col2 = st.columns(2)
    
    with col1:
        category_revenue = data.groupby('category')['total_amount'].sum().reset_index()
        fig1 = px.bar(category_revenue, x='category', y='total_amount', 
                     title='Revenue by Product Category',
                     color='total_amount', color_continuous_scale='viridis')
        fig1.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        mall_revenue = data.groupby('shopping_mall')['total_amount'].sum().reset_index()
        fig2 = px.bar(mall_revenue, x='shopping_mall', y='total_amount',
                     title='Revenue by Shopping Mall',
                     color='total_amount', color_continuous_scale='plasma')
        fig2.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig2, use_container_width=True)
    
    # Gender and Age Analysis
    col3, col4 = st.columns(2)
    
    with col3:
        gender_spending = data.groupby('gender')['total_amount'].sum().reset_index()
        fig3 = px.pie(gender_spending, values='total_amount', names='gender',
                     title='Spending by Gender')
        st.plotly_chart(fig3, use_container_width=True)
    
    with col4:
        age_spending = data.groupby('age_group')['total_amount'].sum().reset_index()
        fig4 = px.bar(age_spending, x='age_group', y='total_amount',
                     title='Spending by Age Group',
                     color='total_amount', color_continuous_scale='inferno')
        st.plotly_chart(fig4, use_container_width=True)

def main():
    """Main application"""
    # Initialize session state at the very beginning
    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = 'local'
    if 'query' not in st.session_state:
        st.session_state.query = ""
    
    st.markdown('<h1 class="main-header">🛍️ AI-Powered Customer Shopping Analytics</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Demonstrating Agentic AI Workflow with Natural Language Query Processing</p>', unsafe_allow_html=True)
    
    # Load data
    loader, data = load_data()
    if data is None:
        st.error("Failed to load data. Please check if the data file exists.")
        return
    
    # Initialize AI components with selected model
    narrative_gen = initialize_ai_components(st.session_state.selected_model)
    
    # Modern Sidebar Design
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <h2 style="color: #1f77b4; margin: 0; font-size: 1.5rem;">🎯 Navigation</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # AI Model Selection Section
    st.sidebar.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 1rem; border-radius: 10px; margin: 1rem 0;">
        <h3 style="color: white; margin: 0 0 1rem 0; font-size: 1.1rem;">🤖 AI Model</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Model selection buttons
    model_options = {
        'local': {'icon': '🧠', 'name': 'Local LLM', 'desc': 'No API Key Required'},
        'gemini': {'icon': '🔮', 'name': 'Gemini 2.5 Pro', 'desc': 'Your API Key Configured'},
        'gpt': {'icon': '⚡', 'name': 'GPT-5', 'desc': 'Your API Key Configured'}
    }
    
    # Create model selection buttons
    for model_key, model_info in model_options.items():
        is_selected = st.session_state.selected_model == model_key
        
        if st.sidebar.button(
            f"{model_info['icon']} {model_info['name']}",
            key=f"model_{model_key}",
            help=model_info['desc']
        ):
            st.session_state.selected_model = model_key
            st.rerun()
        
        # Show selected status
        if is_selected:
            st.sidebar.markdown(f"""
            <div style="background: #e8f5e8; padding: 0.5rem; border-radius: 5px; 
                        border-left: 4px solid #4caf50; margin: 0.5rem 0;">
                <small style="color: #2e7d32;">✅ {model_info['name']} - Active</small>
            </div>
            """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    # Page Navigation Section
    st.sidebar.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 1rem; border-radius: 10px; margin: 1rem 0;">
        <h3 style="color: white; margin: 0 0 1rem 0; font-size: 1.1rem;">📱 Pages</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize page selection in session state
    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = "📊 Dashboard"
    
    # Page navigation buttons
    pages = [
        {"icon": "📊", "name": "Dashboard", "desc": "Analytics Overview"},
        {"icon": "🤖", "name": "AI Agent", "desc": "Natural Language Queries"},
        {"icon": "📈", "name": "Advanced Analysis", "desc": "Deep Analytics"},
        {"icon": "🔍", "name": "Data Explorer", "desc": "Raw Data & Insights"}
    ]
    
    for page_info in pages:
        page_key = f"{page_info['icon']} {page_info['name']}"
        is_selected = st.session_state.selected_page == page_key
        
        if st.sidebar.button(
            f"{page_info['icon']} {page_info['name']}",
            key=f"page_{page_info['name'].lower().replace(' ', '_')}",
            help=page_info['desc']
        ):
            st.session_state.selected_page = page_key
            st.rerun()
        
        # Show selected status
        if is_selected:
            st.sidebar.markdown(f"""
            <div style="background: #e3f2fd; padding: 0.5rem; border-radius: 5px; 
                        border-left: 4px solid #2196f3; margin: 0.5rem 0;">
                <small style="color: #1565c0;">📍 {page_info['name']} - Current Page</small>
            </div>
            """, unsafe_allow_html=True)
    
    page = st.session_state.selected_page
    
    if page == "📊 Dashboard":
        st.markdown("## 📊 Customer Shopping Analytics Dashboard")
        
        # Display metrics
        display_metrics(data)
        
        # Create dashboard
        create_customer_dashboard(data)
        
        # Generate AI insights for dashboard
        if narrative_gen:
            st.markdown("### 🤖 AI-Generated Dashboard Insights")
            insights = narrative_gen.generate_dataset_summary(data, loader.get_basic_stats())
            st.markdown(f'<div class="ai-insight">{insights}</div>', unsafe_allow_html=True)
    
    elif page == "🤖 AI Agent":
        st.markdown("## 🤖 AI Agent - Natural Language Query Processing")
        
        # Show current model being used
        model_names = {
            'local': '🧠 Local LLM',
            'gemini': '🔮 Gemini 2.5 Pro',
            'gpt': '⚡ GPT-5'
        }
        current_model = model_names.get(st.session_state.selected_model, 'Unknown')
        st.info(f"**Current AI Model:** {current_model}")
        
        st.markdown("### This demonstrates the complete Agentic AI workflow:")
        st.markdown("1. **Natural Language Query** → User enters query in plain English")
        st.markdown("2. **Query Translation** → AI translates to Pandas code")
        st.markdown("3. **Data Analysis** → Executes analysis and generates results")
        st.markdown("4. **Visualization** → Creates interactive charts")
        st.markdown("5. **AI Insights** → Generates narrative analytics")
        
        if narrative_gen:
            # Initialize simplified agentic workflow
            visualizer = DataVisualizer()
            workflow = SimpleAgenticWorkflow(data, visualizer, narrative_gen)
            
            st.markdown("### 💬 Natural Language Query Interface")
            st.markdown("Ask questions about your data in natural language:")
            
            # Query input
            query = st.text_input(
                "Enter your query:",
                value=st.session_state.query,
                placeholder="e.g., Show me revenue trends by category"
            )
            
            # Add clear button next to analyze button
            col1, col2 = st.columns([3, 1])
            with col1:
                analyze_clicked = st.button("🚀 Analyze with AI Agent")
            with col2:
                if st.button("🗑️ Clear Query"):
                    st.session_state.query = ""
                    st.rerun()
            
            if analyze_clicked:
                if query:
                    with st.spinner("AI Agent is processing your query..."):
                        result = workflow.execute_query(query)
                        
                        if result["success"]:
                            st.success("✅ Analysis completed successfully!")
                            
                            # Display results in columns
                            col1, col2 = st.columns([1, 1])
                            
                            with col1:
                                st.markdown("### 📊 Query Translation")
                                st.markdown(f'<div class="query-result"><strong>Natural Language:</strong> "{result["query"]}"</div>', unsafe_allow_html=True)
                                st.markdown(f'<div class="query-result"><strong>Pandas Code:</strong> <code>{result["pandas_code"]}</code></div>', unsafe_allow_html=True)
                                
                                if isinstance(result['result'], pd.DataFrame):
                                    st.markdown(f"**Results:** {result['result'].shape[0]} rows, {result['result'].shape[1]} columns")
                                    st.dataframe(result['result'].head(10))
                                else:
                                    st.write(f"**Results:** {result['result']}")
                            
                            with col2:
                                st.markdown("### ⏱️ Performance")
                                st.metric("Execution Time", f"{result['execution_time']:.2f}s")
                                st.metric("Success", "✅ Yes")
                                
                                if result['visualization']['chart_type'] != 'error':
                                    st.markdown(f"**Chart Type:** {result['visualization']['chart_type']}")
                                    st.markdown(f"**Title:** {result['visualization']['title']}")
                            
                            # AI insights
                            st.markdown("### 🤖 AI-Generated Insights")
                            st.markdown(f'<div class="ai-insight">{result["insights"]}</div>', unsafe_allow_html=True)
                            
                            # Generate visualization
                            st.markdown("### 📈 Generated Visualization")
                            if result['visualization']['figure'] is not None:
                                st.plotly_chart(result['visualization']['figure'], use_container_width=True)
                            else:
                                st.warning("Visualization could not be generated.")
                            
                        else:
                            st.error("❌ Analysis failed. Please try a different query.")
                            st.write(result["insights"])
                else:
                    st.warning("Please enter a query to analyze.")
            
            # Predefined queries
            st.markdown("### 💡 Example Queries")
            st.markdown("Click any example below to automatically fill the query field:")
            
            example_queries = [
                "Show me revenue trends by category",
                "What are the most popular shopping malls?",
                "Show me spending analysis by gender",
                "Give me a summary of the customer shopping data",
                "What are the customer spending patterns by age group?",
                "Show me payment method preferences"
            ]
            
            # Create a more compact layout
            cols = st.columns(3)
            for i, example in enumerate(example_queries):
                col_idx = i % 3
                with cols[col_idx]:
                    # Create shorter button text
                    button_text = f"📊 {example[:30]}{'...' if len(example) > 30 else ''}"
                    if st.button(button_text, key=f"query_{i}", help=example):
                        st.session_state.query = example
                        st.rerun()
        
        else:
            st.warning("AI components not available. Please check your configuration.")
    
    elif page == "📈 Advanced Analysis":
        st.markdown("## 📈 Advanced Query Analysis")
        
        if narrative_gen:
            visualizer = DataVisualizer()
            workflow = SimpleAgenticWorkflow(data, visualizer, narrative_gen)
            
            # Trend Analysis
            st.markdown("### 📈 Trend Analysis")
            if st.button("Show me daily revenue trends"):
                result = workflow.execute_query("Show me daily revenue trends")
                if result["success"]:
                    st.plotly_chart(result['visualization']['figure'], use_container_width=True)
                    st.markdown(f'<div class="ai-insight">{result["insights"]}</div>', unsafe_allow_html=True)
            
            # Comparative Analysis
            st.markdown("### 🔍 Comparative Analysis")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Revenue by Category"):
                    result = workflow.execute_query("Show me revenue by category")
                    if result["success"]:
                        st.plotly_chart(result['visualization']['figure'], use_container_width=True)
                        st.markdown(f'<div class="ai-insight">{result["insights"]}</div>', unsafe_allow_html=True)
            
            with col2:
                if st.button("Spending by Gender"):
                    result = workflow.execute_query("Show me spending analysis by gender")
                    if result["success"]:
                        st.plotly_chart(result['visualization']['figure'], use_container_width=True)
                        st.markdown(f'<div class="ai-insight">{result["insights"]}</div>', unsafe_allow_html=True)
    
    elif page == "🔍 Data Explorer":
        st.markdown("## 🔍 Data Explorer")
        
        st.markdown("### 📋 Dataset Information")
        st.write(f"**Total Records:** {len(data):,}")
        st.write(f"**Columns:** {list(data.columns)}")
        st.write(f"**Date Range:** {data['invoice_date'].min().strftime('%Y-%m-%d')} to {data['invoice_date'].max().strftime('%Y-%m-%d')}")
        
        st.markdown("### 📊 Data Preview")
        st.dataframe(data.head(20))
        
        st.markdown("### 📈 Column Statistics")
        st.write(data.describe())
        
        # Generate AI insights about the dataset
        if narrative_gen:
            st.markdown("### 🤖 AI-Generated Dataset Insights")
            insights = narrative_gen.generate_dataset_summary(data, loader.get_basic_stats())
            st.markdown(f'<div class="ai-insight">{insights}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
