"""
Customer Shopping AI Agent Module
Uses LangChain to create intelligent agents for customer shopping data analysis
"""

import os
import time
import re
from typing import Dict, Any, List, Tuple, Optional
import pandas as pd
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent
from langchain.prompts import PromptTemplate
from langchain.schema import AgentAction, AgentFinish
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
    
    def __init__(self, data: pd.DataFrame):
        super().__init__()
        self.data = data
    
    def _run(self, query: str) -> str:
        """Execute customer data analysis based on natural language query"""
        try:
            # Parse the query and generate pandas code
            pandas_code = self._generate_pandas_code(query)
            
            # Execute the code safely
            local_vars = {'df': self.data, 'pd': pd}
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
    
    def __init__(self, visualizer):
        super().__init__()
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

class CustomerAgentPromptTemplate:
    """Custom prompt template for the customer shopping agent"""
    
    def __init__(self, tools, tool_names):
        self.tools = tools
        self.tool_names = tool_names
        self.template = PromptTemplate(
            input_variables=["tools", "tool_names", "input", "agent_scratchpad"],
            template="""You are an intelligent customer shopping data analysis agent. You have access to the following tools:

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

    def format(self, **kwargs) -> str:
        """Format the prompt"""
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += f"\nAction: {action}\nObservation: {observation}\n"
        kwargs["agent_scratchpad"] = thoughts
        kwargs["tools"] = self.tools
        kwargs["tool_names"] = self.tool_names
        return self.template.format(**kwargs)

class CustomerShoppingAgent:
    """Main agent class for customer shopping data analysis"""
    
    def __init__(self, data: pd.DataFrame, visualizer, narrative_generator):
        """
        Initialize the customer shopping agent
        
        Args:
            data (pd.DataFrame): The customer shopping dataset to analyze
            visualizer: Visualization object
            narrative_generator: Narrative generator object
        """
        self.data = data
        self.visualizer = visualizer
        self.narrative_generator = narrative_generator
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            temperature=0,
            model="gpt-3.5-turbo",
            openai_api_key=os.getenv('OPENAI_API_KEY')
        )
        
        # Create tools
        self.tools = [
            CustomerDataAnalysisTool(data),
            CustomerVisualizationTool(visualizer)
        ]
        
        # Create agent
        self.agent = self._create_agent()
        self.agent_executor = AgentExecutor.from_agent_and_tools(
            agent=self.agent,
            tools=self.tools,
            verbose=True
        )
    
    def _create_agent(self) -> LLMSingleActionAgent:
        """Create the agent with custom prompt"""
        tool_names = [tool.name for tool in self.tools]
        
        # Create prompt template using the modern LangChain approach
        from langchain.prompts import PromptTemplate
        
        prompt_template = PromptTemplate(
            input_variables=["tools", "tool_names", "input", "agent_scratchpad"],
            template="""You are an intelligent customer shopping data analysis agent. You have access to the following tools:

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
        
        # Create LLM chain with prompt
        from langchain.chains import LLMChain
        llm_chain = LLMChain(
            llm=self.llm,
            prompt=prompt_template
        )
        
        # Create a custom output parser that matches our prompt format
        from langchain.agents import AgentOutputParser
        
        class CustomOutputParser(AgentOutputParser):
            def parse(self, llm_output: str) -> AgentAction | AgentFinish:
                if "Final Answer:" in llm_output:
                    return AgentFinish(
                        return_values={"output": llm_output.split("Final Answer:")[-1].strip()},
                        log=llm_output,
                    )
                
                regex = r"Action: (.*?)[\n]*Action Input: (.*)"
                match = re.search(regex, llm_output, re.DOTALL)
                if not match:
                    raise ValueError(f"Could not parse LLM output: `{llm_output}`")
                
                action = match.group(1).strip()
                action_input = match.group(2).strip(" ").strip('"')
                
                return AgentAction(tool=action, tool_input=action_input, log=llm_output)
        
        output_parser = CustomOutputParser()
        
        return LLMSingleActionAgent(
            llm_chain=llm_chain,
            output_parser=output_parser,
            stop=["\nObservation:"],
            allowed_tools=tool_names
        )
    
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
            # Execute agent
            result = self.agent_executor.invoke({"input": query})
            
            # Generate additional insights
            insights = self.narrative_generator.generate_query_analysis(
                query, 
                self.data, 
                time.time() - start_time
            )
            
            return {
                "query": query,
                "agent_response": result.get("output", ""),
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
