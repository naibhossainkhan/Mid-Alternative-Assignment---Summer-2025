"""
Configuration file for AI model settings and API keys
"""

import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AIConfig:
    """Configuration class for AI model settings"""
    
    def __init__(self):
        # API Keys - Load from multiple sources (env vars, Streamlit secrets, etc.)
        self.openai_api_key = self._get_secret('OPENAI_API_KEY')
        self.gemini_api_key = self._get_secret('GEMINI_API_KEY')
        
        # Validate that required API keys are present
        if not self.openai_api_key:
            print("Warning: OPENAI_API_KEY not found in environment variables or Streamlit secrets")
        if not self.gemini_api_key:
            print("Warning: GEMINI_API_KEY not found in environment variables or Streamlit secrets")
        
        # Setup model configurations
        self._setup_models()
    
    def _get_secret(self, key: str) -> str:
        """
        Get secret from multiple sources in order of priority:
        1. Environment variables
        2. Streamlit secrets (if running in Streamlit Cloud)
        3. .env file (already handled by python-dotenv)
        """
        # First try environment variables
        value = os.getenv(key)
        if value:
            return value
        
        # Then try Streamlit secrets (for Streamlit Cloud deployment)
        try:
            import streamlit as st
            if hasattr(st, 'secrets') and hasattr(st.secrets, 'ai_config'):
                # Try to get from Streamlit secrets
                if key == 'OPENAI_API_KEY':
                    return st.secrets.ai_config.get('openai_api_key', '')
                elif key == 'GEMINI_API_KEY':
                    return st.secrets.ai_config.get('gemini_api_key', '')
        except ImportError:
            # Not running in Streamlit environment
            pass
        
        return ''
    
    def _setup_models(self):
        """Setup model configurations after API keys are loaded"""
        # Default model settings
        self.default_model = os.getenv('DEFAULT_AI_MODEL', 'gemini')  # 'gpt', 'gemini', 'local'
        
        # Model configurations
        self.models = {
            'gpt': {
                'name': 'GPT-3.5 Turbo',
                'provider': 'openai',
                'api_key': self.openai_api_key,
                'max_tokens': 500,
                'temperature': 0.7,
                'enabled': bool(self.openai_api_key and self.openai_api_key.strip())
            },
            'gemini': {
                'name': 'Gemini 2.5 Pro',
                'provider': 'google',
                'api_key': self.gemini_api_key,
                'max_tokens': 500,
                'temperature': 0.7,
                'enabled': bool(self.gemini_api_key and self.gemini_api_key.strip())
            },
            'local': {
                'name': 'Local LLM',
                'provider': 'local',
                'api_key': None,
                'max_tokens': 500,
                'temperature': 0.7,
                'enabled': True  # Always enabled for local
            }
        }
    
    def get_model_config(self, model_name: str = None) -> Dict[str, Any]:
        """Get configuration for a specific model"""
        model_name = model_name or self.default_model
        return self.models.get(model_name, self.models['local'])
    
    def get_available_models(self) -> list:
        """Get list of available models"""
        return [name for name, config in self.models.items() if config['enabled']]
    
    def is_model_available(self, model_name: str) -> bool:
        """Check if a model is available"""
        return model_name in self.models and self.models[model_name]['enabled']
    
    def set_default_model(self, model_name: str):
        """Set the default model"""
        if self.is_model_available(model_name):
            self.default_model = model_name
        else:
            raise ValueError(f"Model {model_name} is not available")

# Global config instance
config = AIConfig()
