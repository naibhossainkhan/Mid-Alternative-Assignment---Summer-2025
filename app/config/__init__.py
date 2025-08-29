"""
Configuration management for AI-Powered Customer Shopping Analytics.

This package handles all application configuration including:
- AI model settings
- API keys management
- Environment variables
- Application constants
"""

from .settings import AIConfig, config

__all__ = ["AIConfig", "config"]
