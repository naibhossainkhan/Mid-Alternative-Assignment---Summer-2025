"""
AI and machine learning components for customer shopping analytics.

This module contains:
- agent: LangChain AI agent for data analysis
- generator: AI narrative generation
- provider: AI service providers (OpenAI, Gemini, etc.)
"""

from .agent import CustomerShoppingAgent
from .generator import NarrativeGenerator
from .provider import AIProvider

__all__ = ["CustomerShoppingAgent", "NarrativeGenerator", "AIProvider"]
