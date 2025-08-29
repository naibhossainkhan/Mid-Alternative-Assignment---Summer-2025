"""
Multi-Model AI Provider
Supports GPT, Gemini, and Local LLM for text generation
"""

import sys
import os
sys.path.append('..')

from typing import Dict, Any, Optional
import pandas as pd
from config import config

class AIProvider:
    """Multi-model AI provider for text generation"""
    
    def __init__(self, model_name: str = None):
        """
        Initialize AI provider with specified model
        
        Args:
            model_name (str): Model to use ('gpt', 'gemini', 'local')
        """
        self.model_name = model_name or config.default_model
        self.model_config = config.get_model_config(self.model_name)
        
        # Initialize model-specific clients
        self.openai_client = None
        self.gemini_client = None
        
        if self.model_name == 'gpt':
            self._init_openai()
        elif self.model_name == 'gemini':
            self._init_gemini()
        elif self.model_name == 'local':
            self._init_local()
    
    def _init_openai(self):
        """Initialize OpenAI client"""
        try:
            from openai import OpenAI
            self.openai_client = OpenAI(api_key=self.model_config['api_key'])
        except ImportError:
            raise ImportError("OpenAI package not installed. Run: pip install openai")
        except Exception as e:
            raise Exception(f"Failed to initialize OpenAI: {e}")
    
    def _init_gemini(self):
        """Initialize Gemini client"""
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.model_config['api_key'])
            
            # Use gemini-2.5-pro for the latest model
            self.gemini_client = genai.GenerativeModel('gemini-2.5-pro')
                    
        except ImportError:
            raise ImportError("Google Generative AI package not installed. Run: pip install google-generativeai")
        except Exception as e:
            raise Exception(f"Failed to initialize Gemini: {e}")
    
    def _init_local(self):
        """Initialize local LLM (placeholder for future implementation)"""
        # For now, this will use a simple template-based approach
        pass
    
    def generate_text(self, prompt: str, system_prompt: str = None) -> str:
        """
        Generate text using the selected AI model
        
        Args:
            prompt (str): User prompt
            system_prompt (str): System prompt (optional)
            
        Returns:
            str: Generated text
        """
        try:
            if self.model_name == 'gpt':
                return self._generate_with_gpt(prompt, system_prompt)
            elif self.model_name == 'gemini':
                return self._generate_with_gemini(prompt, system_prompt)
            elif self.model_name == 'local':
                return self._generate_with_local(prompt, system_prompt)
            else:
                raise ValueError(f"Unsupported model: {self.model_name}")
        except Exception as e:
            return f"Error generating text with {self.model_name}: {str(e)}"
    
    def _generate_with_gpt(self, prompt: str, system_prompt: str = None) -> str:
        """Generate text using OpenAI GPT"""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        response = self.openai_client.chat.completions.create(
            model=self.model_config['name'],
            messages=messages,
            max_tokens=self.model_config['max_tokens'],
            temperature=self.model_config['temperature']
        )
        
        return response.choices[0].message.content.strip()
    
    def _generate_with_gemini(self, prompt: str, system_prompt: str = None) -> str:
        """Generate text using Google Gemini"""
        full_prompt = prompt
        
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        
        response = self.gemini_client.generate_content(full_prompt)
        
        # Handle different response formats
        if hasattr(response, 'text'):
            return response.text.strip()
        elif hasattr(response, 'parts'):
            return response.parts[0].text.strip()
        else:
            return str(response).strip()
    
    def _generate_with_local(self, prompt: str, system_prompt: str = None) -> str:
        """Generate text using local LLM (template-based for now)"""
        # This is a simple template-based approach
        # In a real implementation, you would integrate with a local LLM like Ollama, LlamaCpp, etc.
        
        if "dataset summary" in prompt.lower():
            return self._generate_local_dataset_summary(prompt)
        elif "visualization" in prompt.lower():
            return self._generate_local_visualization_insights(prompt)
        elif "trend" in prompt.lower():
            return self._generate_local_trend_analysis(prompt)
        else:
            return self._generate_local_generic_response(prompt)
    
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
    
    def _generate_local_generic_response(self, prompt: str) -> str:
        """Generate generic response using local template"""
        return """
## AI Analysis Response

Based on the provided data and query, here are the key insights:

- The dataset contains comprehensive customer shopping information
- Multiple dimensions of analysis are possible including demographics, geography, and product categories
- Significant business opportunities exist for optimization and growth
- Customer behavior patterns provide valuable insights for strategic planning

This analysis supports data-driven decision making for retail operations and customer experience enhancement.
        """.strip()
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model"""
        return {
            'name': self.model_name,
            'provider': self.model_config['provider'],
            'model_name': self.model_config['name'],
            'enabled': self.model_config['enabled']
        }
