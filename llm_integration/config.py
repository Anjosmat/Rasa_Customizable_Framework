"""
Configuration module for LLM integration
"""
import os
import json
import logging
from pathlib import Path
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Default configuration
DEFAULT_CONFIG = {
    "default_provider": "anthropic",  # 'anthropic' or 'openai'
    "anthropic_model": "claude-3-sonnet-20240229",
    "openai_model": "gpt-4",
    "max_tokens": 1000,
    "temperature": 0.7,
    "enable_context": True,
    "max_context_turns": 5,
    "fallback_threshold": 0.3,  # Confidence threshold for Rasa to fallback to LLM
    "cache_responses": True,
    "cache_ttl": 3600  # Time-to-live for cached responses in seconds
}

# Path to the config file
CONFIG_FILE = Path("config/llm_config.json")


def get_llm_config() -> Dict[str, Any]:
    """
    Get the LLM configuration from file or environment variables

    Returns:
        Dict[str, Any]: The configuration dictionary
    """
    config = DEFAULT_CONFIG.copy()

    # Try to load from config file if it exists
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                file_config = json.load(f)
                config.update(file_config)
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Error loading config file: {e}")

    # Override with environment variables if present
    env_mappings = {
        "LLM_PROVIDER": "default_provider",
        "ANTHROPIC_MODEL": "anthropic_model",
        "ANTHROPIC_API_KEY": "anthropic_api_key",
        "OPENAI_MODEL": "openai_model",
        "OPENAI_API_KEY": "openai_api_key",
        "LLM_MAX_TOKENS": "max_tokens",
        "LLM_TEMPERATURE": "temperature",
        "LLM_ENABLE_CONTEXT": "enable_context",
        "LLM_MAX_CONTEXT_TURNS": "max_context_turns",
        "LLM_FALLBACK_THRESHOLD": "fallback_threshold"
    }

    for env_var, config_key in env_mappings.items():
        if env_var in os.environ:
            # Convert string values to appropriate types
            value = os.environ[env_var]
            if value.lower() in ("true", "false"):
                value = value.lower() == "true"
            elif value.replace(".", "", 1).isdigit():
                value = float(value) if "." in value else int(value)

            config[config_key] = value

    return config


def save_llm_config(config: Dict[str, Any]) -> bool:
    """
    Save the LLM configuration to file

    Args:
        config (Dict[str, Any]): The configuration to save

    Returns:
        bool: True if successful, False otherwise
    """
    # Create config directory if it doesn't exist
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=2)
        return True
    except IOError as e:
        logger.error(f"Error saving config file: {e}")
        return False
