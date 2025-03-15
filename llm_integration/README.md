# LLM Integration for Rasa Customizable Framework

This module integrates Large Language Models (LLMs) like Claude or GPT-4 into the Rasa Customizable Framework to handle unknown intents and provide more intelligent responses.

## Features

- Fallback to LLM when Rasa can't confidently classify an intent
- Conversation context tracking to maintain conversational memory
- Business-specific prompting based on business type
- Support for multiple LLM providers (Anthropic Claude, OpenAI GPT)
- Configurable settings for LLM integration

## Configuration

The LLM integration can be configured in several ways:

1. Environment variables:
   ```
   LLM_PROVIDER=anthropic
   ANTHROPIC_API_KEY=your_api_key
   ANTHROPIC_MODEL=claude-3-sonnet-20240229
   LLM_FALLBACK_THRESHOLD=0.3
   LLM_MAX_CONTEXT_TURNS=5
   ```

2. Configuration file (`config/llm_config.json`):
   ```json
   {
     "default_provider": "anthropic",
     "anthropic_model": "claude-3-sonnet-20240229",
     "max_tokens": 1000,
     "enable_context": true
   }
   ```

## Setup Instructions

1. Create an account with Anthropic or OpenAI to get an API key
2. Set your API key as an environment variable:
   ```
   # For Anthropic Claude
   export ANTHROPIC_API_KEY=your_api_key
   
   # For OpenAI
   export OPENAI_API_KEY=your_api_key
   ```

3. Update your Rasa configuration:
   - Make sure `action_llm_fallback` is included in your `domain.yml`
   - Set appropriate fallback thresholds in your `config.yml`

## Usage

The LLM integration will automatically trigger when:

1. Rasa cannot confidently classify an intent (below the confidence threshold)
2. The user's message is explicitly classified as `nlu_fallback`

The LLM will generate a response based on:
- The current message
- Conversation history (if enabled)
- Business type context

## Example Conversation with LLM Fallback

```
User: Hello
Bot: Hello! How can I assist you today?

User: I need help with something not in your training data
Bot: [LLM generated response based on context and business type]

User: Thank you
Bot: You're welcome! Is there anything else I can help you with?
```

## Extending the LLM Integration

### Adding a New LLM Provider

To add support for a new LLM provider:

1. Create a new class that inherits from `LLMClient` in `llm_client.py`
2. Implement the `generate_response` method
3. Update the `get_llm_client` factory function to return your new client

### Customizing System Prompts

To customize the system prompts used for different business types:

1. Modify the `_build_system_prompt` method in `llm_fallback.py`
2. Add domain-specific instructions based on business needs

## Troubleshooting

- **API Key Issues**: Ensure your API key is correctly set as an environment variable
- **Rate Limiting**: If you encounter rate limiting errors, consider implementing a retry mechanism
- **Response Quality**: Adjust the system prompt or temperature setting for better responses

## Dependencies

- `requests`: For making HTTP requests to LLM APIs
- `rasa_sdk`: For implementing custom actions

## License

Same as the main Rasa Customizable Framework project.