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
        # API Keys
        self.openai_api_key = os.getenv('OPENAI_API_KEY', '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')
        # self.gemini_api_key = os.getenv('GEMINI_API_KEY', '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')
        self.gemini_api_key = os.getenv('GEMINI_API_KEY', 'AIzaSyCSgthqUPp1X--3dAu7bihS_00izLY8PlY')
        
        # Default model settings
        self.default_model = os.getenv('DEFAULT_AI_MODEL', 'gemini')  # 'gpt', 'gemini', 'local'
        
        # Model configurations
        self.models = {
            'gpt': {
                'name': 'GPT-5',
                'provider': 'openai',
                'api_key': self.openai_api_key,
                'max_tokens': 500,
                'temperature': 0.7,
                'enabled': bool(self.openai_api_key)
            },
            'gemini': {
                'name': 'Gemini 2.5 Pro',
                'provider': 'google',
                'api_key': self.gemini_api_key,
                'max_tokens': 500,
                'temperature': 0.7,
                'enabled': bool(self.gemini_api_key)
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
