"""AI Scientist package.
Ensures environment variables from .env are loaded on first import.
"""

# Load .env once at import time
from . import config  # noqa: F401

