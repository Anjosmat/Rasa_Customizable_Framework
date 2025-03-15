"""
LLM Client for integrating with external Large Language Models (e.g., Claude, OpenAI)
"""
import os
import logging
import json
import requests
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List

from .config import get_llm_config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLMClient(ABC):
    """Abstract base class for LLM client implementations"""

    @abstractmethod
    def generate_response(self, prompt: str, context: Optional[List[Dict[str, str]]] = None) -> str:
        """
        Generate a response from the LLM given a prompt and optional context

        Args:
            prompt (str): The user's message or query
            context (List[Dict[str, str]], optional): Previous conversation turns

        Returns:
            str: The generated response from the LLM
        """
        pass


class AnthropicClient(LLMClient):
    """Client for Anthropic Claude API"""

    def __init__(self):
        """Initialize the Anthropic Claude client"""
        config = get_llm_config()
        self.api_key = config.get("anthropic_api_key", os.getenv("ANTHROPIC_API_KEY"))
        self.api_url = config.get("anthropic_api_url", "https://api.anthropic.com/v1/messages")
        self.model = config.get("anthropic_model", "claude-3-opus-20240229")
        self.max_tokens = config.get("max_tokens", 1000)

        if not self.api_key:
            logger.warning("Anthropic API key not found! Please set ANTHROPIC_API_KEY environment variable.")

    def generate_response(self, prompt: str, context: Optional[List[Dict[str, str]]] = None) -> str:
        """Generate a response using Anthropic Claude"""
        if not self.api_key:
            return "LLM integration not configured. Please set the API key."

        headers = {
            "x-api-key": self.api_key,
            "content-type": "application/json",
            "anthropic-version": "2023-06-01"
        }

        messages = []

        # Add conversation context if provided
        if context:
            for turn in context:
                messages.append(turn)

        # Add the current user message
        messages.append({"role": "user", "content": prompt})

        data = {
            "model": self.model,
            "messages": messages,
            "max_tokens": self.max_tokens
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()

            result = response.json()
            return result["content"][0]["text"]

        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Anthropic API: {e}")
            return "Sorry, I encountered an error while processing your request."


class OpenAIClient(LLMClient):
    """Client for OpenAI GPT API"""

    def __init__(self):
        """Initialize the OpenAI client"""
        config = get_llm_config()
        self.api_key = config.get("openai_api_key", os.getenv("OPENAI_API_KEY"))
        self.api_url = config.get("openai_api_url", "https://api.openai.com/v1/chat/completions")
        self.model = config.get("openai_model", "gpt-4")
        self.max_tokens = config.get("max_tokens", 1000)

        if not self.api_key:
            logger.warning("OpenAI API key not found! Please set OPENAI_API_KEY environment variable.")

    def generate_response(self, prompt: str, context: Optional[List[Dict[str, str]]] = None) -> str:
        """Generate a response using OpenAI GPT"""
        if not self.api_key:
            return "LLM integration not configured. Please set the API key."

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        messages = []

        # Add conversation context if provided
        if context:
            for turn in context:
                messages.append(turn)

        # Add the current user message
        messages.append({"role": "user", "content": prompt})

        data = {
            "model": self.model,
            "messages": messages,
            "max_tokens": self.max_tokens
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()

            result = response.json()
            return result["choices"][0]["message"]["content"]

        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling OpenAI API: {e}")
            return "Sorry, I encountered an error while processing your request."


def get_llm_client(provider: str = None) -> LLMClient:
    """
    Factory function to get the appropriate LLM client

    Args:
        provider (str, optional): The LLM provider to use. If None, uses the default from config.

    Returns:
        LLMClient: An instance of the appropriate LLM client
    """
    if provider is None:
        config = get_llm_config()
        provider = config.get("default_provider", "anthropic")

    if provider.lower() == "anthropic":
        return AnthropicClient()
    elif provider.lower() == "openai":
        return OpenAIClient()
    else:
        logger.warning(f"Unknown LLM provider: {provider}. Using Anthropic Claude as default.")
        return AnthropicClient()