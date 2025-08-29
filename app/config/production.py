"""
Production configuration settings for AI-Powered Customer Shopping Analytics.

This module contains production-specific configuration settings including:
- Environment variables
- Security settings
- Performance optimizations
- Logging configuration
"""

import os
from typing import Dict, Any
from .settings import AIConfig

class ProductionConfig(AIConfig):
    """Production configuration class."""
    
    def __init__(self):
        super().__init__()
        
        # Production-specific settings
        self.debug = False
        self.log_level = "INFO"
        
        # Security settings
        self.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')
        
        # Performance settings
        self.cache_timeout = 3600  # 1 hour
        self.max_upload_size = 50 * 1024 * 1024  # 50MB
        
        # Database settings (if needed in future)
        self.database_url = os.getenv('DATABASE_URL', '')
        
        # External service settings
        self.api_timeout = 30  # seconds
        self.retry_attempts = 3
        
    def get_logging_config(self) -> Dict[str, Any]:
        """Get logging configuration for production."""
        return {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'standard': {
                    'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
                },
            },
            'handlers': {
                'default': {
                    'level': 'INFO',
                    'formatter': 'standard',
                    'class': 'logging.StreamHandler',
                },
            },
            'loggers': {
                '': {
                    'handlers': ['default'],
                    'level': 'INFO',
                    'propagate': True
                }
            }
        }

# Production configuration instance
production_config = ProductionConfig()
