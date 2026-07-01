"""
agent.py
--------
Self-contained entry point for `adk web`.
All agent code is defined here directly so ADK can load it without
needing to resolve the `app` package.
"""

import sys
import os

# Add the project root to Python path so `app` imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.agents.orchestrator_agent import root_agent
