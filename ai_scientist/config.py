"""Project configuration loader.
Loads environment variables from a .env file at project root.
"""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv, find_dotenv

# Load .env from project root if present
# find_dotenv will walk up directories to locate the first .env
load_dotenv(find_dotenv(usecwd=True), override=False)

# Provide simple accessors (optional)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
CLAUDE_API_BASE = os.getenv("CLAUDE_API_BASE")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_BASE = os.getenv("GEMINI_API_BASE")

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
