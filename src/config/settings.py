# src/config/settings.py
"""Configuration settings for the application."""

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Gemini API key for LLM integration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not set in environment variables. Please add it to a .env file.")