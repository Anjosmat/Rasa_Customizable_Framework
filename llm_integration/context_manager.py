"""
Context Manager for maintaining conversation history for LLM interactions
"""
import time
import logging
from typing import Dict, List, Optional, Any
from .config import get_llm_config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConversationContext:
    """Manages conversation context for LLM interactions"""

    def __init__(self, session_id: str, max_turns: Optional[int] = None):
        """
        Initialize a new conversation context

        Args:
            session_id (str): Unique identifier for the conversation
            max_turns (int, optional): Maximum number of conversation turns to keep
        """
        self.session_id = session_id
        config = get_llm_config()
        self.max_turns = max_turns or config.get("max_context_turns", 5)
        self.turns: List[Dict[str, str]] = []
        self.metadata: Dict[str, Any] = {
            "created_at": time.time(),
            "last_updated": time.time(),
            "business_type": None,
            "user_preferences": {}
        }

    def add_user_message(self, message: str) -> None:
        """
        Add a user message to the conversation context

        Args:
            message (str): The user's message
        """
        self.turns.append({"role": "user", "content": message})
        self._trim_context()
        self.metadata["last_updated"] = time.time()

    def add_assistant_message(self, message: str) -> None:
        """
        Add an assistant message to the conversation context

        Args:
            message (str): The assistant's message
        """
        self.turns.append({"role": "assistant", "content": message})
        self._trim_context()
        self.metadata["last_updated"] = time.time()

    def _trim_context(self) -> None:
        """Trim the conversation context to the maximum number of turns"""
        if len(self.turns) > self.max_turns * 2:  # Each turn is a user message and assistant response
            self.turns = self.turns[-self.max_turns * 2:]

    def get_context_for_llm(self) -> List[Dict[str, str]]:
        """
        Get the conversation context in a format suitable for LLM API

        Returns:
            List[Dict[str, str]]: List of messages with roles and content
        """
        return self.turns

    def set_metadata(self, key: str, value: Any) -> None:
        """
        Set metadata for the conversation

        Args:
            key (str): Metadata key
            value (Any): Metadata value
        """
        self.metadata[key] = value
        self.metadata["last_updated"] = time.time()

    def get_metadata(self, key: str) -> Any:
        """
        Get metadata for the conversation

        Args:
            key (str): Metadata key

        Returns:
            Any: Metadata value
        """
        return self.metadata.get(key)


class ContextManager:
    """Manages conversation contexts for multiple users"""

    def __init__(self):
        """Initialize the context manager"""
        self.contexts: Dict[str, ConversationContext] = {}
        self.config = get_llm_config()

    def get_or_create_context(self, session_id: str) -> ConversationContext:
        """
        Get an existing conversation context or create a new one

        Args:
            session_id (str): Unique identifier for the conversation

        Returns:
            ConversationContext: The conversation context
        """
        if session_id not in self.contexts:
            self.contexts[session_id] = ConversationContext(session_id)

        return self.contexts[session_id]

    def add_user_message(self, session_id: str, message: str) -> None:
        """
        Add a user message to a conversation context

        Args:
            session_id (str): Unique identifier for the conversation
            message (str): The user's message
        """
        context = self.get_or_create_context(session_id)
        context.add_user_message(message)

    def add_assistant_message(self, session_id: str, message: str) -> None:
        """
        Add an assistant message to a conversation context

        Args:
            session_id (str): Unique identifier for the conversation
            message (str): The assistant's message
        """
        context = self.get_or_create_context(session_id)
        context.add_assistant_message(message)

    def get_context_for_llm(self, session_id: str) -> List[Dict[str, str]]:
        """
        Get the conversation context for a session

        Args:
            session_id (str): Unique identifier for the conversation

        Returns:
            List[Dict[str, str]]: Conversation context for LLM
        """
        context = self.get_or_create_context(session_id)
        return context.get_context_for_llm()

    def set_business_type(self, session_id: str, business_type: str) -> None:
        """
        Set the business type for a conversation

        Args:
            session_id (str): Unique identifier for the conversation
            business_type (str): The business type
        """
        context = self.get_or_create_context(session_id)
        context.set_metadata("business_type", business_type)

    def get_business_type(self, session_id: str) -> Optional[str]:
        """
        Get the business type for a conversation

        Args:
            session_id (str): Unique identifier for the conversation

        Returns:
            Optional[str]: The business type
        """
        context = self.get_or_create_context(session_id)
        return context.get_metadata("business_type")

    def clear_context(self, session_id: str) -> None:
        """
        Clear the conversation context for a session

        Args:
            session_id (str): Unique identifier for the conversation
        """
        if session_id in self.contexts:
            del self.contexts[session_id]


# Global instance of the context manager
_context_manager = None


def get_context_manager() -> ContextManager:
    """
    Get the global context manager instance

    Returns:
        ContextManager: The global context manager
    """
    global _context_manager
    if _context_manager is None:
        _context_manager = ContextManager()

    return _context_manager