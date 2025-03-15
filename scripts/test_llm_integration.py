#!/usr/bin/env python
"""
Test script for LLM integration
"""
import os
import sys
import argparse
import logging
from pathlib import Path

# Add parent directory to path so we can import modules
parent_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(parent_dir))

from llm_integration.llm_client import get_llm_client
from llm_integration.context_manager import get_context_manager
from llm_integration.config import get_llm_config, save_llm_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_llm_response(prompt, provider=None, business_type=None):
    """
    Test LLM response generation

    Args:
        prompt (str): The prompt to send to the LLM
        provider (str, optional): The LLM provider to use
        business_type (str, optional): The business type context
    """
    try:
        # Get LLM client
        llm_client = get_llm_client(provider)

        # Set up a test conversation context
        context_manager = get_context_manager()
        session_id = "test_session"

        if business_type:
            context_manager.set_business_type(session_id, business_type)
            print(f"Using business type: {business_type}")

        # Add the user message to context
        context_manager.add_user_message(session_id, prompt)

        # Get the conversation context
        context = context_manager.get_context_for_llm(session_id)

        # Add system prompt with business context
        if business_type:
            if business_type == "healthcare":
                system_prompt = (
                    "You are a helpful assistant for a healthcare business. "
                    "Be empathetic and remind users that you cannot provide medical advice."
                )
            elif business_type == "retail":
                system_prompt = (
                    "You are a helpful assistant for a retail business. "
                    "Focus on helping customers with product information and order tracking."
                )
            elif business_type == "finance":
                system_prompt = (
                    "You are a helpful assistant for a financial services business. "
                    "Be precise and clear in your responses."
                )
            else:
                system_prompt = "You are a helpful assistant for a business."

            # Insert system prompt at the beginning
            context.insert(0, {"role": "system", "content": system_prompt})

        # Generate a response
        print(f"\nSending prompt: \"{prompt}\"")
        print("Generating response...")
        response = llm_client.generate_response(prompt, context)

        # Display the response
        print(f"\nLLM Response:\n{response}\n")

        # Add the assistant response to context
        context_manager.add_assistant_message(session_id, response)

        return response

    except Exception as e:
        logger.error(f"Error testing LLM: {e}")
        print(f"Error: {e}")
        return None


def interactive_mode(provider=None, business_type=None):
    """
    Run an interactive conversation with the LLM

    Args:
        provider (str, optional): The LLM provider to use
        business_type (str, optional): The business type context
    """
    print("\nLLM Integration Interactive Test")
    print("================================")
    print(f"Provider: {provider or get_llm_config().get('default_provider', 'anthropic')}")
    if business_type:
        print(f"Business Type: {business_type}")
    print("Type 'exit' or 'quit' to end the conversation")
    print("================================\n")

    session_id = "interactive_session"
    context_manager = get_context_manager()

    if business_type:
        context_manager.set_business_type(session_id, business_type)

    try:
        while True:
            # Get user input
            user_input = input("You: ")

            # Exit if requested
            if user_input.lower() in ["exit", "quit", "q"]:
                print("Goodbye!")
                break

            # Process the message
            test_llm_response(user_input, provider, business_type)

    except KeyboardInterrupt:
        print("\nExiting interactive mode...")
    except Exception as e:
        logger.error(f"Error in interactive mode: {e}")
        print(f"Error: {e}")


def main():
    """Main entry point for the test script"""
    parser = argparse.ArgumentParser(description="Test LLM integration")
    parser.add_argument("--interactive", "-i", action="store_true", help="Run in interactive mode")
    parser.add_argument("--provider", "-p", choices=["anthropic", "openai"], help="LLM provider to use")
    parser.add_argument("--business-type", "-b", choices=["healthcare", "retail", "finance"],
                        help="Business type context")
    parser.add_argument("--prompt", help="Test prompt to send to the LLM")

    args = parser.parse_args()

    # Check if API keys are set
    config = get_llm_config()
    provider = args.provider or config.get("default_provider", "anthropic")

    if provider == "anthropic" and not (os.environ.get("ANTHROPIC_API_KEY") or config.get("anthropic_api_key")):
        print("Warning: ANTHROPIC_API_KEY environment variable or config setting is not set.")
        print("Set it with: export ANTHROPIC_API_KEY=your_api_key")

    if provider == "openai" and not (os.environ.get("OPENAI_API_KEY") or config.get("openai_api_key")):
        print("Warning: OPENAI_API_KEY environment variable or config setting is not set.")
        print("Set it with: export OPENAI_API_KEY=your_api_key")

    if args.interactive:
        interactive_mode(args.provider, args.business_type)
    elif args.prompt:
        test_llm_response(args.prompt, args.provider, args.business_type)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()