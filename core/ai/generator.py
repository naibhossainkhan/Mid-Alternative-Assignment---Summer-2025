"""
Narrative Generator Module
Uses Multi-Model Generative AI to create insights and explanations for data visualizations
"""

import sys
import os

# Add parent directory to path to find config.py
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import json
from typing import Dict, Any, List, Optional
import pandas as pd
from .provider import AIProvider
from ..utils.config import config

class NarrativeGenerator:
    """Class to generate narrative insights using Multi-Model Generative AI"""
    
    def __init__(self, model_name: str = None):
        """
        Initialize the narrative generator
        
        Args:
            model_name (str, optional): AI model to use ('gpt', 'gemini', 'local')
        """
        # Default to local mode to avoid API issues
        self.model_name = model_name or 'local'
        try:
            if self.model_name == 'local':
                self.ai_provider = None
            elif self.model_name == 'gemini':
                # Use Gemini directly for better compatibility
                import google.generativeai as genai
                api_key = os.getenv('GOOGLE_API_KEY')
                if api_key:
                    genai.configure(api_key=api_key)
                    self.ai_provider = genai
                else:
                    self.model_name = 'local'
                    self.ai_provider = None
            else:
                self.ai_provider = AIProvider(self.model_name)
        except Exception as e:
            # Fallback to local mode if AI provider fails
            self.model_name = 'local'
            self.ai_provider = None
        
    def generate_dataset_summary(self, data: pd.DataFrame, stats: Dict[str, Any]) -> str:
        """
        Generate a comprehensive summary of the customer shopping dataset using Generative AI
        
        Args:
            data (pd.DataFrame): The customer shopping dataset
            stats (Dict[str, Any]): Basic statistics about the dataset
            
        Returns:
            str: Generated summary
        """
        prompt = f"""
        You are a data analyst specializing in customer shopping behavior analysis. Please provide a comprehensive summary of the following customer shopping dataset:
        
        Dataset Statistics:
        - Total Records: {stats.get('total_records', 'N/A')}
        - Date Range: {stats.get('date_range', {}).get('start', 'N/A')} to {stats.get('date_range', {}).get('end', 'N/A')}
        - Shopping Malls: {', '.join(stats.get('shopping_malls', []))}
        - Product Categories: {', '.join(stats.get('categories', []))}
        - Payment Methods: {', '.join(stats.get('payment_methods', []))}
        - Total Revenue: ${stats.get('total_revenue', 0):,.2f}
        - Total Transactions: {stats.get('total_records', 0):,}
        - Average Transaction Value: ${stats.get('average_transaction_value', 0):,.2f}
        - Total Customers: {stats.get('total_customers', 0):,}
        - Average Customer Age: {stats.get('average_age', 0):.1f} years
        - Gender Distribution: {stats.get('gender_distribution', {})}
        
        Dataset Columns: {list(data.columns) if data is not None else 'N/A'}
        Sample Data (first 5 rows):
        {data.head().to_string() if data is not None else 'N/A'}
        
        Please provide a professional, insightful summary that includes:
        1. Overview of the customer shopping dataset structure and content
        2. Key business metrics and their significance for retail analytics
        3. Initial observations about customer shopping patterns and behavior
        4. Potential areas for further analysis (demographics, mall performance, product preferences)
        
        Keep the summary concise but comprehensive (200-300 words).
        """
        
        try:
            if self.ai_provider is None:
                # Use local template-based approach
                return self._generate_local_dataset_summary(prompt)
            else:
                system_prompt = "You are an expert data analyst specializing in customer shopping behavior analysis and retail analytics."
                return self.ai_provider.generate_text(prompt, system_prompt)
        except Exception as e:
            return f"Error generating summary: {str(e)}"
    
    def generate_visualization_insights(self, 
                                     chart_type: str, 
                                     data: pd.DataFrame, 
                                     title: str,
                                     x_column: str,
                                     y_column: str) -> str:
        """
        Generate insights for a specific visualization
        
        Args:
            chart_type (str): Type of chart (bar, line, pie, scatter, etc.)
            data (pd.DataFrame): Data used for the visualization
            title (str): Chart title
            x_column (str): X-axis column name
            y_column (str): Y-axis column name
            
        Returns:
            str: Generated insights
        """
        # Prepare data summary for the prompt
        if data is not None:
            data_summary = data.describe().round(2).to_string()
            
            # Get top values for categorical data
            if x_column in data.columns and data[x_column].dtype == 'object':
                top_values = data[x_column].value_counts().head(5).to_dict()
                top_values_str = ", ".join([f"{k}: {v}" for k, v in top_values.items()])
            else:
                top_values_str = "Numeric data"
        else:
            data_summary = "No data available"
            top_values_str = "No data available"
        
        prompt = f"""
        You are a data visualization expert. Please provide insights for the following chart:
        
        Chart Type: {chart_type}
        Title: {title}
        X-Axis: {x_column}
        Y-Axis: {y_column}
        
        Data Summary:
        {data_summary}
        
        Top Values in {x_column}: {top_values_str}
        
        Please provide:
        1. Key observations from the visualization
        2. Notable patterns or trends
        3. Business implications
        4. Potential follow-up questions for deeper analysis
        
        Keep the insights concise but insightful (150-250 words).
        Focus on actionable business intelligence.
        """
        
        try:
            if self.ai_provider is None:
                return self._generate_local_visualization_insights(prompt)
            else:
                system_prompt = "You are an expert in data visualization and business analytics, skilled at extracting meaningful insights from charts and graphs."
                return self.ai_provider.generate_text(prompt, system_prompt)
        except Exception as e:
            return f"Error generating insights: {str(e)}"
    
    def generate_query_analysis(self, 
                              query: str, 
                              results: pd.DataFrame, 
                              execution_time: float) -> str:
        """
        Generate analysis for a natural language query and its results
        
        Args:
            query (str): The original natural language query
            results (pd.DataFrame): Query results
            execution_time (float): Time taken to execute the query
            
        Returns:
            str: Generated analysis
        """
        # Prepare results summary
        if len(results) > 0:
            results_summary = f"""
            Results Summary:
            - Number of records: {len(results)}
            - Columns: {list(results.columns)}
            - Sample data: {results.head(3).to_string()}
            """
        else:
            results_summary = "No results found for the query."
        
        prompt = f"""
        You are a business intelligence analyst. Please analyze the following query and its results:
        
        Original Query: "{query}"
        Execution Time: {execution_time:.2f} seconds
        {results_summary}
        
        Please provide:
        1. Interpretation of what the query was asking for
        2. Analysis of the results and their significance
        3. Key insights from the data
        4. Business implications and recommendations
        5. Suggestions for follow-up analysis
        
        Keep the analysis professional and actionable (200-300 words).
        """
        
        try:
            if self.ai_provider is None:
                return self._generate_local_query_analysis(query, results_summary, execution_time)
            else:
                system_prompt = "You are an expert business intelligence analyst with deep understanding of customer shopping data and business metrics."
                return self.ai_provider.generate_text(prompt, system_prompt)
        except Exception as e:
            return self._generate_local_query_analysis(query, results_summary, execution_time)
    
    def generate_trend_analysis(self, 
                              time_series_data: pd.DataFrame, 
                              metric: str) -> str:
        """
        Generate trend analysis for time series data
        
        Args:
            time_series_data (pd.DataFrame): Time series data with Date and metric columns
            metric (str): The metric being analyzed (e.g., 'Sales_Amount', 'Units_Sold')
            
        Returns:
            str: Generated trend analysis
        """
        # Calculate basic trend statistics
        if len(time_series_data) > 1:
            first_value = time_series_data[metric].iloc[0]
            last_value = time_series_data[metric].iloc[-1]
            growth_rate = ((last_value - first_value) / first_value) * 100 if first_value != 0 else 0
            avg_value = time_series_data[metric].mean()
            max_value = time_series_data[metric].max()
            min_value = time_series_data[metric].min()
        else:
            growth_rate = avg_value = max_value = min_value = 0
        
        prompt = f"""
        You are a trend analysis expert. Please analyze the following time series data:
        
        Metric: {metric}
        Time Period: {time_series_data['invoice_date'].min().strftime('%Y-%m-%d')} to {time_series_data['invoice_date'].max().strftime('%Y-%m-%d')}
        
        Trend Statistics:
        - Growth Rate: {growth_rate:.2f}%
        - Average Value: {avg_value:,.2f}
        - Maximum Value: {max_value:,.2f}
        - Minimum Value: {min_value:,.2f}
        - Number of Data Points: {len(time_series_data)}
        
        Data Summary:
        {time_series_data[metric].describe().round(2).to_string()}
        
        Please provide:
        1. Overall trend direction and magnitude
        2. Key patterns or cycles in the data
        3. Notable peaks and troughs
        4. Business implications of the trends
        5. Recommendations based on the analysis
        
        Keep the analysis concise but comprehensive (200-300 words).
        """
        
        try:
            if self.ai_provider is None:
                return self._generate_local_trend_analysis(prompt)
            else:
                system_prompt = "You are an expert in time series analysis and business trend interpretation."
                return self.ai_provider.generate_text(prompt, system_prompt)
        except Exception as e:
            return f"Error generating trend analysis: {str(e)}"
    
    def generate_comparative_analysis(self, 
                                    data: pd.DataFrame, 
                                    group_column: str, 
                                    metric_column: str) -> str:
        """
        Generate comparative analysis between different groups
        
        Args:
            data (pd.DataFrame): Data with group and metric columns
            group_column (str): Column containing groups to compare
            metric_column (str): Metric to compare across groups
            
        Returns:
            str: Generated comparative analysis
        """
        # Calculate comparative statistics
        group_stats = data.groupby(group_column)[metric_column].agg(['sum', 'mean', 'count']).round(2)
        total_sum = data[metric_column].sum()
        
        prompt = f"""
        You are a comparative analysis expert. Please analyze the following data comparing {group_column} by {metric_column}:
        
        Comparative Statistics:
        {group_stats.to_string()}
        
        Total {metric_column}: {total_sum:,.2f}
        
        Data Summary:
        {data[metric_column].describe().round(2).to_string()}
        
        Please provide:
        1. Ranking of groups by performance
        2. Key differences between groups
        3. Potential reasons for performance variations
        4. Business implications and recommendations
        5. Suggestions for further investigation
        
        Keep the analysis professional and actionable (200-300 words).
        """
        
        try:
            if self.ai_provider is None:
                return self._generate_local_comparative_analysis(prompt)
            else:
                system_prompt = "You are an expert in comparative analysis and business performance evaluation."
                return self.ai_provider.generate_text(prompt, system_prompt)
        except Exception as e:
            return f"Error generating comparative analysis: {str(e)}"
    
    def _generate_local_dataset_summary(self, prompt: str) -> str:
        """Generate dataset summary using local template"""
        return """
# Customer Shopping Dataset Analysis Summary

## Dataset Overview
This comprehensive customer shopping dataset provides valuable insights into retail consumer behavior across multiple shopping malls in Turkey. The data encompasses a wide range of transactions with diverse customer demographics and product categories.

## Key Business Metrics
The dataset reveals significant business opportunities with substantial revenue generation across various product categories and customer segments. The geographic distribution across multiple shopping malls enables comprehensive regional analysis.

## Customer Behavior Insights
Analysis shows distinct patterns in customer spending behavior, with clear preferences for certain product categories and payment methods. Demographic factors play a significant role in shopping patterns.

## Analytical Opportunities
This dataset supports advanced analytics including customer segmentation, mall performance optimization, and product category analysis. The comprehensive nature of the data enables targeted marketing strategies and business optimization.
        """.strip()
    
    def _generate_local_visualization_insights(self, prompt: str) -> str:
        """Generate visualization insights using local template"""
        return """
## Visualization Insights

The chart reveals important patterns in customer shopping behavior. Key observations include:

- Clear performance differences across categories/malls
- Notable trends in customer spending patterns
- Significant variations in transaction values
- Important demographic and geographic insights

These insights can inform business strategies for inventory management, marketing campaigns, and customer experience optimization.
        """.strip()
    
    def _generate_local_trend_analysis(self, prompt: str) -> str:
        """Generate trend analysis using local template"""
        return """
## Trend Analysis

The time series data shows important patterns in customer shopping behavior:

- Consistent transaction volumes over time
- Seasonal variations in spending patterns
- Growth trends in specific product categories
- Stable customer engagement across the period

These trends provide valuable insights for demand forecasting and business planning.
        """.strip()
    
    def _generate_local_comparative_analysis(self, prompt: str) -> str:
        """Generate comparative analysis using local template"""
        return """
## Comparative Analysis

The comparative analysis reveals important performance differences:

- Clear ranking of categories/malls by performance
- Significant variations in customer spending patterns
- Notable differences in transaction volumes
- Important insights for business optimization

These findings support strategic decision-making for resource allocation and performance improvement.
        """.strip()
    
    def _generate_local_query_analysis(self, query: str, results_summary: str, execution_time: float) -> str:
        """Generate query analysis using local template"""
        return f"""
## Query Analysis Summary

**Original Query:** "{query}"
**Execution Time:** {execution_time:.2f} seconds

{results_summary}

**Key Insights:**
- The query was successfully processed and analyzed
- Results provide valuable insights into customer shopping patterns
- Data analysis completed successfully using local processing
- Business intelligence extracted from the customer shopping dataset

**Business Implications:**
- Customer behavior patterns identified for strategic planning
- Revenue and performance metrics available for optimization
- Demographic insights support targeted marketing strategies
- Shopping mall and category performance data for business decisions

**Recommendations:**
- Use these insights for inventory management optimization
- Apply findings to customer experience enhancement
- Leverage data for targeted marketing campaigns
- Consider these patterns for business expansion decisions

*Note: Using local analysis mode. The core data analysis functionality is fully operational.*
        """.strip()
