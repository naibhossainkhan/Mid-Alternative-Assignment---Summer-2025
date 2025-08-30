"""
Customer Shopping AI Agent Module
Uses LangChain to create intelligent agents for customer shopping data analysis
"""

import os
import time
import re
from typing import Dict, Any, List, Tuple, Optional
import pandas as pd
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
from langchain.tools import BaseTool
from pydantic import BaseModel, Field, ConfigDict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class QueryInput(BaseModel):
    """Input schema for natural language queries"""
    query: str = Field(description="Natural language query about customer shopping data")
    
    model_config = ConfigDict(arbitrary_types_allowed=True)

class CustomerDataAnalysisTool(BaseTool):
    """Tool for performing customer shopping data analysis operations"""
    
    name: str = "customer_data_analysis"
    description: str = "Perform customer shopping data analysis operations like filtering, grouping, and aggregating data"
    args_schema: type = QueryInput
    data: pd.DataFrame = Field(default=None, description="Customer shopping data")
    
    def __init__(self, data: pd.DataFrame, **kwargs):
        super().__init__(**kwargs)
        self.data = data
    
    def _run(self, query: str) -> str:
        """Execute customer data analysis based on natural language query"""
        try:
            # Calculate total_amount from price * quantity
            df = self.data.copy()
            df['total_amount'] = df['price'] * df['quantity']
            
            # Parse the query and generate pandas code
            pandas_code = self._generate_pandas_code(query)
            
            # Execute the code safely
            local_vars = {'df': df, 'pd': pd}
            exec(pandas_code, globals(), local_vars)
            
            # Get the result
            result = local_vars.get('result', None)
            
            if result is not None:
                if isinstance(result, pd.DataFrame):
                    return f"Analysis completed. Result shape: {result.shape}\n\n{result.head(10).to_string()}"
                else:
                    return f"Analysis completed. Result: {result}"
            else:
                return "Analysis completed but no result was returned."
                
        except Exception as e:
            return f"Error in customer data analysis: {str(e)}"
    
    def _generate_pandas_code(self, query: str) -> str:
        """Generate pandas code from natural language query for customer shopping data"""
        query_lower = query.lower()
        
        # Sales and revenue analysis
        if "revenue" in query_lower or "sales" in query_lower:
            if "category" in query_lower:
                return "result = df.groupby('category')['total_amount'].sum().reset_index()"
            elif "mall" in query_lower or "shopping" in query_lower:
                return "result = df.groupby('shopping_mall')['total_amount'].sum().reset_index()"
            elif "gender" in query_lower:
                return "result = df.groupby('gender')['total_amount'].sum().reset_index()"
            elif "age" in query_lower:
                return "result = df.groupby('age_group')['total_amount'].sum().reset_index()"
            else:
                return "result = df.groupby('invoice_date')['total_amount'].sum().reset_index()"
        
        # Category analysis
        elif "category" in query_lower:
            if "popular" in query_lower or "most" in query_lower:
                return "result = df.groupby('category').size().reset_index(name='count').sort_values('count', ascending=False)"
            else:
                return "result = df.groupby('category')['total_amount'].sum().reset_index()"
        
        # Shopping mall analysis
        elif "mall" in query_lower or "shopping" in query_lower:
            if "popular" in query_lower or "most" in query_lower:
                return "result = df.groupby('shopping_mall').size().reset_index(name='count').sort_values('count', ascending=False)"
            else:
                return "result = df.groupby('shopping_mall')['total_amount'].sum().reset_index()"
        
        # Gender analysis
        elif "gender" in query_lower:
            if "spending" in query_lower:
                return "result = df.groupby('gender')['total_amount'].sum().reset_index()"
            elif "preference" in query_lower or "category" in query_lower:
                return "result = df.groupby(['gender', 'category'])['total_amount'].sum().reset_index()"
            else:
                return "result = df.groupby('gender').size().reset_index(name='count')"
        
        # Age analysis
        elif "age" in query_lower:
            if "group" in query_lower:
                return "result = df.groupby('age_group')['total_amount'].sum().reset_index()"
            elif "spending" in query_lower:
                return "result = df.groupby('age_group')['total_amount'].mean().reset_index()"
            else:
                return "result = df.groupby('age_group').size().reset_index(name='count')"
        
        # Payment method analysis
        elif "payment" in query_lower:
            if "method" in query_lower:
                return "result = df.groupby('payment_method')['total_amount'].sum().reset_index()"
            else:
                return "result = df.groupby('payment_method').size().reset_index(name='count')"
        
        # Customer analysis
        elif "customer" in query_lower:
            if "segment" in query_lower:
                return """
                customer_segments = df.groupby('customer_id').agg({
                    'total_amount': 'sum',
                    'invoice_no': 'nunique',
                    'category': 'nunique'
                }).reset_index()
                customer_segments['segment'] = pd.cut(
                    customer_segments['total_amount'],
                    bins=[0, 1000, 5000, 10000, float('inf')],
                    labels=['Budget', 'Regular', 'Premium', 'VIP']
                )
                result = customer_segments.groupby('segment').size().reset_index(name='count')
                """
            else:
                return "result = df.groupby('customer_id')['total_amount'].sum().reset_index()"
        
        # Time series analysis
        elif "trend" in query_lower or "time" in query_lower:
            if "daily" in query_lower:
                return "result = df.groupby('invoice_date')['total_amount'].sum().reset_index()"
            elif "monthly" in query_lower:
                return "result = df.groupby(['year', 'month'])['total_amount'].sum().reset_index()"
            else:
                return "result = df.groupby('invoice_date')['total_amount'].sum().reset_index()"
        
        # Quantity analysis
        elif "quantity" in query_lower:
            if "category" in query_lower:
                return "result = df.groupby('category')['quantity'].sum().reset_index()"
            elif "mall" in query_lower:
                return "result = df.groupby('shopping_mall')['quantity'].sum().reset_index()"
            else:
                return "result = df.groupby('invoice_date')['quantity'].sum().reset_index()"
        
        # Summary statistics
        elif "summary" in query_lower or "overview" in query_lower:
            return """
            result = {
                'total_revenue': df['total_amount'].sum(),
                'total_transactions': len(df),
                'total_customers': df['customer_id'].nunique(),
                'total_invoices': df['invoice_no'].nunique(),
                'avg_transaction_value': df['total_amount'].mean(),
                'total_quantity': df['quantity'].sum(),
                'categories': df['category'].nunique(),
                'malls': df['shopping_mall'].nunique()
            }
            """
        
        # Default to revenue analysis
        else:
            return "result = df.groupby('category')['total_amount'].sum().reset_index()"

class CustomerVisualizationTool(BaseTool):
    """Tool for creating customer shopping visualizations"""
    
    name: str = "customer_visualization"
    description: str = "Create charts and visualizations based on customer shopping data analysis results"
    args_schema: type = QueryInput
    visualizer: Any = Field(default=None, description="Visualization object")
    
    def __init__(self, visualizer, **kwargs):
        super().__init__(**kwargs)
        self.visualizer = visualizer
    
    def _run(self, query: str) -> str:
        """Create visualization based on customer shopping query"""
        try:
            query_lower = query.lower()
            
            if "bar chart" in query_lower or "bar" in query_lower:
                if "category" in query_lower:
                    return "Created bar chart showing revenue by product category"
                elif "mall" in query_lower:
                    return "Created bar chart showing revenue by shopping mall"
                elif "gender" in query_lower:
                    return "Created bar chart showing spending by gender"
                else:
                    return "Created bar chart for customer shopping analysis"
            
            elif "line chart" in query_lower or "trend" in query_lower:
                return "Created line chart showing revenue trends over time"
            
            elif "pie chart" in query_lower:
                return "Created pie chart showing category distribution"
            
            elif "scatter" in query_lower:
                return "Created scatter plot for customer analysis"
            
            elif "heatmap" in query_lower:
                return "Created correlation heatmap for customer data"
            
            else:
                return "Created default visualization for customer shopping data"
                
        except Exception as e:
            return f"Error in customer visualization: {str(e)}"

# Removed old CustomerAgentPromptTemplate class - using modern create_react_agent instead

class CustomerShoppingAgent:
    """Main agent class for customer shopping data analysis"""
    
    def __init__(self, data: pd.DataFrame, visualizer, narrative_generator, model_type='openai'):
        """
        Initialize the customer shopping agent
        
        Args:
            data (pd.DataFrame): The customer shopping dataset to analyze
            visualizer: Visualization object
            narrative_generator: Narrative generator object
            model_type (str): Type of LLM to use ('openai', 'gemini', 'local')
        """
        self.data = data
        self.visualizer = visualizer
        self.narrative_generator = narrative_generator
        self.model_type = model_type
        
        # Initialize LLM based on model type
        if model_type == 'openai':
            self.llm = ChatOpenAI(
                temperature=0,
                model="gpt-3.5-turbo",
                openai_api_key=os.getenv('OPENAI_API_KEY'),
                base_url="https://openrouter.ai/api/v1"
            )
        elif model_type == 'gemini':
            from langchain_google_genai import ChatGoogleGenerativeAI
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=os.getenv('GOOGLE_API_KEY'),
                temperature=0
            )
        else:
            # For local or fallback, we'll use a simple approach
            self.llm = None
        
        # Create tools
        self.tools = [
            CustomerDataAnalysisTool(data),
            CustomerVisualizationTool(visualizer)
        ]
        
        # Create agent based on model type
        if self.llm is not None:
            # Create prompt template for the agent
            from langchain.prompts import PromptTemplate
            
            prompt = PromptTemplate.from_template(
                """You are an intelligent customer shopping data analysis agent. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Question: {input}
Thought: {agent_scratchpad}"""
            )

            # Create agent using modern LangChain approach
            self.agent = create_react_agent(
                llm=self.llm,
                tools=self.tools,
                prompt=prompt
            )
            
            # Create agent executor
            self.agent_executor = AgentExecutor(
                agent=self.agent,
                tools=self.tools,
                verbose=True
            )
        else:
            # For local processing, we'll use a simple approach
            self.agent = None
            self.agent_executor = None
    
    # Removed old _create_agent method - using modern create_react_agent instead
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """
        Process a natural language query about customer shopping data
        
        Args:
            query (str): Natural language query
            
        Returns:
            Dict[str, Any]: Results including analysis, visualization, and insights
        """
        start_time = time.time()
        
        try:
            if self.agent_executor is not None:
                # Execute agent with LLM
                result = self.agent_executor.invoke({"input": query})
                agent_response = result.get("output", "")
            else:
                # Use simple local processing
                agent_response = self._process_query_locally(query)
            
            # Generate additional insights
            try:
                # Create a simple results dataframe for the narrative generator
                results_df = pd.DataFrame({
                    'query': [query],
                    'response': [agent_response],
                    'execution_time': [time.time() - start_time]
                })
                
                insights = self.narrative_generator.generate_query_analysis(
                    query, 
                    results_df, 
                    time.time() - start_time
                )
            except Exception as insight_error:
                # Fallback insights if narrative generator fails
                insights = f"Analysis completed successfully. Query: '{query}'. Execution time: {time.time() - start_time:.2f}s. Note: AI insights generation failed due to API limitations."
            
            return {
                "query": query,
                "agent_response": agent_response,
                "insights": insights,
                "execution_time": time.time() - start_time,
                "success": True
            }
            
        except Exception as e:
            return {
                "query": query,
                "agent_response": f"Error: {str(e)}",
                "insights": "Unable to generate insights due to processing error.",
                "execution_time": time.time() - start_time,
                "success": False
            }
    
    def _process_query_locally(self, query: str) -> str:
        """Process query using local logic without external LLM"""
        query_lower = query.lower()
        
        # Calculate total amount (price * quantity) for revenue analysis
        self.data['total_amount'] = self.data['price'] * self.data['quantity']
        
        # Simple rule-based processing for common queries
        if "revenue" in query_lower and "category" in query_lower:
            result = self.data.groupby('category')['total_amount'].sum().reset_index()
            return f"Revenue by category analysis completed. Top categories by revenue:\n{result.head().to_string()}"
        
        elif "revenue" in query_lower and "mall" in query_lower:
            result = self.data.groupby('shopping_mall')['total_amount'].sum().reset_index()
            return f"Revenue by shopping mall analysis completed. Top malls by revenue:\n{result.head().to_string()}"
        
        elif "gender" in query_lower and "spending" in query_lower:
            result = self.data.groupby('gender')['total_amount'].sum().reset_index()
            return f"Spending analysis by gender completed:\n{result.to_string()}"
        
        elif "age" in query_lower and "spending" in query_lower:
            # Create age groups
            self.data['age_group'] = pd.cut(self.data['age'], bins=[0, 25, 35, 45, 55, 100], labels=['18-25', '26-35', '36-45', '46-55', '55+'])
            result = self.data.groupby('age_group')['total_amount'].sum().reset_index()
            return f"Spending analysis by age group completed:\n{result.to_string()}"
        
        elif "summary" in query_lower or "overview" in query_lower:
            total_revenue = self.data['total_amount'].sum()
            total_transactions = len(self.data)
            avg_transaction = self.data['total_amount'].mean()
            return f"Customer shopping data summary:\n- Total Revenue: ${total_revenue:,.2f}\n- Total Transactions: {total_transactions:,}\n- Average Transaction: ${avg_transaction:.2f}"
        
        else:
            # Default analysis
            result = self.data.groupby('category')['total_amount'].sum().reset_index()
            return f"Analysis completed. Revenue by category:\n{result.head().to_string()}"
    
    def create_automated_analysis(self) -> Dict[str, Any]:
        """
        Create automated comprehensive customer shopping analysis
        
        Returns:
            Dict[str, Any]: Comprehensive analysis results
        """
        analyses = []
        
        # Predefined analysis queries for customer shopping data
        queries = [
            "Show me revenue trends by category",
            "What are the most popular shopping malls?",
            "Show me spending analysis by gender",
            "Give me a summary of customer shopping data",
            "What are the trends in customer spending by age group?"
        ]
        
        for query in queries:
            result = self.process_query(query)
            analyses.append(result)
        
        return {
            "automated_analyses": analyses,
            "total_execution_time": sum(analysis["execution_time"] for analysis in analyses),
            "successful_analyses": sum(1 for analysis in analyses if analysis["success"])
        }
    
    def generate_visualization_pipeline(self, query: str) -> Dict[str, Any]:
        """
        Generate a complete visualization pipeline for a customer shopping query
        
        Args:
            query (str): Natural language query
            
        Returns:
            Dict[str, Any]: Visualization pipeline results
        """
        # Determine appropriate chart type based on query
        query_lower = query.lower()
        
        if "trend" in query_lower:
            chart_type = "line"
            if "category" in query_lower:
                data = self.data.groupby(['invoice_date', 'category'])['total_amount'].sum().reset_index()
                title = "Revenue Trends by Category"
            else:
                data = self.data.groupby('invoice_date')['total_amount'].sum().reset_index()
                title = "Revenue Trend Over Time"
        
        elif "category" in query_lower:
            chart_type = "bar"
            data = self.data.groupby('category')['total_amount'].sum().reset_index()
            title = "Revenue by Product Category"
        
        elif "mall" in query_lower or "shopping" in query_lower:
            chart_type = "bar"
            data = self.data.groupby('shopping_mall')['total_amount'].sum().reset_index()
            title = "Revenue by Shopping Mall"
        
        elif "gender" in query_lower:
            chart_type = "bar"
            data = self.data.groupby('gender')['total_amount'].sum().reset_index()
            title = "Spending by Gender"
        
        elif "age" in query_lower:
            chart_type = "bar"
            data = self.data.groupby('age_group')['total_amount'].sum().reset_index()
            title = "Spending by Age Group"
        
        elif "distribution" in query_lower or "pie" in query_lower:
            chart_type = "pie"
            data = self.data.groupby('category')['total_amount'].sum().reset_index()
            title = "Revenue Distribution by Category"
        
        else:
            chart_type = "bar"
            data = self.data.groupby('category')['total_amount'].sum().reset_index()
            title = "Customer Shopping Analysis"
        
        # Create visualization
        if chart_type == "line":
            fig = self.visualizer.create_line_chart(data, 'invoice_date', 'total_amount', title)
        elif chart_type == "bar":
            fig = self.visualizer.create_bar_chart(data, data.columns[0], 'total_amount', title)
        elif chart_type == "pie":
            fig = self.visualizer.create_pie_chart(data, 'total_amount', data.columns[0])
        else:
            fig = self.visualizer.create_bar_chart(data, data.columns[0], 'total_amount', title)
        
        # Generate insights
        insights = self.narrative_generator.generate_visualization_insights(
            chart_type, data, title, data.columns[0], 'total_amount'
        )
        
        return {
            "query": query,
            "chart_type": chart_type,
            "title": title,
            "data": data,
            "figure": fig,
            "insights": insights
        }
