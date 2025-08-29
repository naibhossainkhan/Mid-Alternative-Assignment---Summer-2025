"""
Visualization Module
Handles creation of various charts and graphs for data analysis
"""

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# Set style for matplotlib
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class DataVisualizer:
    """Class to handle data visualization using multiple libraries"""
    
    def __init__(self, figsize: Tuple[int, int] = (12, 8)):
        """
        Initialize the visualizer
        
        Args:
            figsize (Tuple[int, int]): Default figure size for matplotlib
        """
        self.figsize = figsize
        self.colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
        
    def create_bar_chart(self, 
                        data: pd.DataFrame, 
                        x_column: str, 
                        y_column: str, 
                        title: str = "",
                        chart_type: str = "matplotlib") -> Any:
        """
        Create a bar chart
        
        Args:
            data (pd.DataFrame): Data to visualize
            x_column (str): Column for x-axis
            y_column (str): Column for y-axis
            title (str): Chart title
            chart_type (str): 'matplotlib' or 'plotly'
            
        Returns:
            Any: Figure object
        """
        if chart_type == "plotly":
            fig = px.bar(
                data, 
                x=x_column, 
                y=y_column,
                title=title,
                color_discrete_sequence=self.colors,
                text=y_column
            )
            fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
            fig.update_layout(
                xaxis_title=x_column,
                yaxis_title=y_column,
                showlegend=False
            )
            return fig
        else:
            fig, ax = plt.subplots(figsize=self.figsize)
            bars = ax.bar(data[x_column], data[y_column], color=self.colors[:len(data)])
            ax.set_title(title, fontsize=16, fontweight='bold')
            ax.set_xlabel(x_column, fontsize=12)
            ax.set_ylabel(y_column, fontsize=12)
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:,.0f}', ha='center', va='bottom')
            
            plt.xticks(rotation=45)
            plt.tight_layout()
            return fig
    
    def create_line_chart(self, 
                         data: pd.DataFrame, 
                         x_column: str, 
                         y_column: str, 
                         title: str = "",
                         chart_type: str = "matplotlib") -> Any:
        """
        Create a line chart
        
        Args:
            data (pd.DataFrame): Data to visualize
            x_column (str): Column for x-axis
            y_column (str): Column for y-axis
            title (str): Chart title
            chart_type (str): 'matplotlib' or 'plotly'
            
        Returns:
            Any: Figure object
        """
        if chart_type == "plotly":
            fig = px.line(
                data, 
                x=x_column, 
                y=y_column,
                title=title,
                color_discrete_sequence=self.colors
            )
            fig.update_layout(
                xaxis_title=x_column,
                yaxis_title=y_column
            )
            return fig
        else:
            fig, ax = plt.subplots(figsize=self.figsize)
            ax.plot(data[x_column], data[y_column], marker='o', linewidth=2, markersize=6)
            ax.set_title(title, fontsize=16, fontweight='bold')
            ax.set_xlabel(x_column, fontsize=12)
            ax.set_ylabel(y_column, fontsize=12)
            ax.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()
            return fig
    
    def create_pie_chart(self, 
                        data: pd.DataFrame, 
                        values_column: str, 
                        names_column: str, 
                        title: str = "",
                        chart_type: str = "matplotlib") -> Any:
        """
        Create a pie chart
        
        Args:
            data (pd.DataFrame): Data to visualize
            values_column (str): Column for values
            names_column (str): Column for labels
            title (str): Chart title
            chart_type (str): 'matplotlib' or 'plotly'
            
        Returns:
            Any: Figure object
        """
        if chart_type == "plotly":
            fig = px.pie(
                data, 
                values=values_column, 
                names=names_column,
                title=title,
                color_discrete_sequence=self.colors
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            return fig
        else:
            fig, ax = plt.subplots(figsize=self.figsize)
            wedges, texts, autotexts = ax.pie(
                data[values_column], 
                labels=data[names_column], 
                autopct='%1.1f%%',
                colors=self.colors[:len(data)],
                startangle=90
            )
            ax.set_title(title, fontsize=16, fontweight='bold')
            plt.tight_layout()
            return fig
    
    def create_scatter_plot(self, 
                           data: pd.DataFrame, 
                           x_column: str, 
                           y_column: str, 
                           color_column: Optional[str] = None,
                           title: str = "",
                           chart_type: str = "matplotlib") -> Any:
        """
        Create a scatter plot
        
        Args:
            data (pd.DataFrame): Data to visualize
            x_column (str): Column for x-axis
            y_column (str): Column for y-axis
            color_column (str, optional): Column for color coding
            title (str): Chart title
            chart_type (str): 'matplotlib' or 'plotly'
            
        Returns:
            Any: Figure object
        """
        if chart_type == "plotly":
            if color_column:
                fig = px.scatter(
                    data, 
                    x=x_column, 
                    y=y_column,
                    color=color_column,
                    title=title
                )
            else:
                fig = px.scatter(
                    data, 
                    x=x_column, 
                    y=y_column,
                    title=title,
                    color_discrete_sequence=self.colors
                )
            fig.update_layout(
                xaxis_title=x_column,
                yaxis_title=y_column
            )
            return fig
        else:
            fig, ax = plt.subplots(figsize=self.figsize)
            if color_column:
                scatter = ax.scatter(data[x_column], data[y_column], 
                                   c=data[color_column], cmap='viridis', alpha=0.7)
                plt.colorbar(scatter, ax=ax, label=color_column)
            else:
                ax.scatter(data[x_column], data[y_column], alpha=0.7, color=self.colors[0])
            
            ax.set_title(title, fontsize=16, fontweight='bold')
            ax.set_xlabel(x_column, fontsize=12)
            ax.set_ylabel(y_column, fontsize=12)
            ax.grid(True, alpha=0.3)
            plt.tight_layout()
            return fig
    
    def create_heatmap(self, 
                      data: pd.DataFrame, 
                      title: str = "",
                      chart_type: str = "matplotlib") -> Any:
        """
        Create a correlation heatmap
        
        Args:
            data (pd.DataFrame): Data to visualize
            title (str): Chart title
            chart_type (str): 'matplotlib' or 'plotly'
            
        Returns:
            Any: Figure object
        """
        # Calculate correlation matrix
        numeric_data = data.select_dtypes(include=[np.number])
        corr_matrix = numeric_data.corr()
        
        if chart_type == "plotly":
            fig = px.imshow(
                corr_matrix,
                title=title,
                color_continuous_scale='RdBu',
                aspect='auto'
            )
            fig.update_layout(
                xaxis_title="Variables",
                yaxis_title="Variables"
            )
            return fig
        else:
            fig, ax = plt.subplots(figsize=self.figsize)
            sns.heatmap(corr_matrix, annot=True, cmap='RdBu', center=0, 
                       square=True, ax=ax, fmt='.2f')
            ax.set_title(title, fontsize=16, fontweight='bold')
            plt.tight_layout()
            return fig
    
    def create_multi_chart_dashboard(self, 
                                   data: pd.DataFrame, 
                                   title: str = "Sales Dashboard") -> Any:
        """
        Create a multi-chart dashboard
        
        Args:
            data (pd.DataFrame): Data to visualize
            title (str): Dashboard title
            
        Returns:
            Any: Figure object
        """
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Sales by Region', 'Sales by Product Category', 
                          'Daily Sales Trend', 'Profit Margin by Region'),
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "scatter"}, {"type": "bar"}]]
        )
        
        # Chart 1: Sales by Region
        region_sales = data.groupby('Region')['Sales_Amount'].sum().reset_index()
        fig.add_trace(
            go.Bar(x=region_sales['Region'], y=region_sales['Sales_Amount'], 
                   name='Sales by Region', marker_color=self.colors[0]),
            row=1, col=1
        )
        
        # Chart 2: Sales by Product Category
        category_sales = data.groupby('Product_Category')['Sales_Amount'].sum().reset_index()
        fig.add_trace(
            go.Bar(x=category_sales['Product_Category'], y=category_sales['Sales_Amount'], 
                   name='Sales by Category', marker_color=self.colors[1]),
            row=1, col=2
        )
        
        # Chart 3: Daily Sales Trend
        daily_sales = data.groupby('Date')['Sales_Amount'].sum().reset_index()
        fig.add_trace(
            go.Scatter(x=daily_sales['Date'], y=daily_sales['Sales_Amount'], 
                      mode='lines+markers', name='Daily Sales', line_color=self.colors[2]),
            row=2, col=1
        )
        
        # Chart 4: Profit Margin by Region
        region_profit = data.groupby('Region')['Profit_Margin'].mean().reset_index()
        fig.add_trace(
            go.Bar(x=region_profit['Region'], y=region_profit['Profit_Margin'], 
                   name='Profit Margin', marker_color=self.colors[3]),
            row=2, col=2
        )
        
        fig.update_layout(
            title_text=title,
            showlegend=False,
            height=800
        )
        
        return fig
    
    def create_time_series_analysis(self, 
                                  data: pd.DataFrame, 
                                  date_column: str = 'Date',
                                  value_column: str = 'Sales_Amount') -> Any:
        """
        Create comprehensive time series analysis
        
        Args:
            data (pd.DataFrame): Data to visualize
            date_column (str): Date column name
            value_column (str): Value column name
            
        Returns:
            Any: Figure object
        """
        # Prepare time series data
        ts_data = data.groupby(date_column)[value_column].agg(['sum', 'mean', 'count']).reset_index()
        
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=('Daily Total Sales', 'Daily Average Sales', 'Daily Transaction Count'),
            vertical_spacing=0.1
        )
        
        # Total Sales
        fig.add_trace(
            go.Scatter(x=ts_data[date_column], y=ts_data['sum'], 
                      mode='lines+markers', name='Total Sales', line_color=self.colors[0]),
            row=1, col=1
        )
        
        # Average Sales
        fig.add_trace(
            go.Scatter(x=ts_data[date_column], y=ts_data['mean'], 
                      mode='lines+markers', name='Average Sales', line_color=self.colors[1]),
            row=2, col=1
        )
        
        # Transaction Count
        fig.add_trace(
            go.Scatter(x=ts_data[date_column], y=ts_data['count'], 
                      mode='lines+markers', name='Transaction Count', line_color=self.colors[2]),
            row=3, col=1
        )
        
        fig.update_layout(
            title_text=f"Time Series Analysis - {value_column}",
            showlegend=False,
            height=900
        )
        
        return fig
    
    def save_chart(self, fig: Any, filename: str, chart_type: str = "matplotlib"):
        """
        Save chart to file
        
        Args:
            fig: Figure object
            filename (str): Output filename
            chart_type (str): 'matplotlib' or 'plotly'
        """
        if chart_type == "plotly":
            fig.write_html(f"{filename}.html")
            fig.write_image(f"{filename}.png")
        else:
            fig.savefig(f"{filename}.png", dpi=300, bbox_inches='tight')
            plt.close(fig)
    
    def display_chart(self, fig: Any, chart_type: str = "matplotlib"):
        """
        Display chart
        
        Args:
            fig: Figure object
            chart_type (str): 'matplotlib' or 'plotly'
        """
        if chart_type == "plotly":
            fig.show()
        else:
            plt.show()
