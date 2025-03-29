# src/core/context_manager.py
"""Module for managing session context using Redis Cloud."""

import redis
import json
import os
import logging
from dotenv import load_dotenv
from typing import Dict, List

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class ContextManager:
    """Manages chat history for context-aware function retrieval using Redis Cloud."""

    def __init__(self, max_history: int = 5, session_ttl: int = 86400):
        """
        Initialize Redis Cloud connection.
        :param max_history: Max interactions to store per session.
        :param session_ttl: Time-to-live for each session (default: 24 hours).
        """
        try:
            self.redis_client = redis.Redis(
                host=os.getenv("REDIS_HOST"),
                port=int(os.getenv("REDIS_PORT")),
                password=os.getenv("REDIS_PASSWORD"),
                decode_responses=True
            )
            self.redis_client.ping()  # Check if Redis is reachable
            logger.info("Connected to Redis Cloud successfully.")
        except redis.ConnectionError as e:
            logger.error(f"Redis Connection Failed: {e}")
            raise Exception("Redis connection error. Check your credentials.")

        self.max_history = max_history
        self.session_ttl = session_ttl  # Auto-expire sessions after given time

    def add_interaction(self, session_id: str, prompt: str, function_metadata: Dict) -> None:
        """Store a new interaction in Redis."""
        try:
            history_key = f"session:{session_id}"
            history = self.get_context_list(session_id)

            # Append new interaction while maintaining max history size
            history.append({"prompt": prompt, "function": function_metadata["name"]})
            history = history[-self.max_history:]

            # Store updated history in Redis with TTL
            self.redis_client.set(history_key, json.dumps(history), ex=self.session_ttl)
            logger.info(f"Updated session history for {session_id}.")
        except Exception as e:
            logger.error(f"Failed to store interaction: {e}")

    def get_context(self, session_id: str) -> str:
        """Retrieve session history as a JSON string."""
        history = self.get_context_list(session_id)
        return json.dumps(history) if history else ""

    def get_context_list(self, session_id: str) -> List[Dict]:
        """Retrieve session history as a Python list."""
        try:
            history_key = f"session:{session_id}"
            history_data = self.redis_client.get(history_key)
            return json.loads(history_data) if history_data else []
        except Exception as e:
            logger.error(f"Error retrieving session {session_id}: {e}")
            return []

    def reset_session(self, session_id: str) -> None:
        """Clear session history in Redis."""
        try:
            self.redis_client.delete(f"session:{session_id}")
            logger.info(f"Session {session_id} cleared.")
        except Exception as e:
            logger.error(f"Error clearing session {session_id}: {e}")

# For testing with Redis Cloud
if __name__ == "__main__":
    cm = ContextManager()

    cm.add_interaction("session1", "Open Chrome", {"name": "open_chrome"})
    cm.add_interaction("session1", "List running processes", {"name": "list_running_processes"})

    print("Context for session1:")
    print(cm.get_context("session1"))

    # Reset session and check history
    cm.reset_session("session1")
    print("Context after reset:", cm.get_context("session1"))
