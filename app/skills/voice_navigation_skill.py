"""
voice_navigation_skill.py
-------------------------
ADK tool: parse and handle voice navigation commands.
Enables users to control the app by voice instead of keyboard/mouse.
"""

import re

# Mapping of voice commands to intent labels
_COMMAND_PATTERNS = {
    "go_back": [r"\bgo back\b", r"\bprevious\b", r"\bback\b"],
    "repeat": [r"\brepeat\b", r"\bsay that again\b", r"\bsay again\b", r"\brepeat that\b"],
    "next": [r"\bnext\b", r"\bcontinue\b", r"\bgo on\b", r"\bgo ahead\b"],
    "stop": [r"\bstop\b", r"\bcancel\b", r"\bquit\b", r"\bexit\b"],
    "help": [r"\bhelp\b", r"\bwhat can you do\b", r"\bcommands\b"],
    "slower": [r"\bspeak slower\b", r"\bslower\b", r"\bslow down\b"],
    "faster": [r"\bspeak faster\b", r"\bfaster\b", r"\bspeed up\b"],
    "louder": [r"\blouder\b", r"\bspeak louder\b", r"\bturn up\b"],
    "softer": [r"\bsofter\b", r"\bquieter\b", r"\bturn down\b"],
    "start_over": [r"\bstart over\b", r"\breset\b", r"\bbeginning\b"],
    "read_results": [r"\bread results\b", r"\bread jobs\b", r"\blist jobs\b"],
}

_HELP_TEXT = (
    "Here are the voice commands you can use. "
    "Say 'go back' to return to the previous step. "
    "Say 'repeat' to hear the last response again. "
    "Say 'next' to continue. "
    "Say 'stop' to cancel. "
    "Say 'help' to hear this message again. "
    "Say 'slower' or 'faster' to adjust speech speed."
)


def parse_navigation_command(user_input: str) -> dict:
    """
    Parse a user's voice input to detect navigation commands.

    Args:
        user_input: Raw text from speech recognition or keyboard.

    Returns:
        dict with:
            'is_command' (bool): True if a navigation command was detected.
            'command' (str | None): The detected command name (e.g. 'go_back').
            'response' (str): A spoken response to give back to the user.
            'original_input' (str): The original input unchanged.
    """
    if not user_input or not user_input.strip():
        return {"is_command": False, "command": None, "response": "", "original_input": user_input}

    text_lower = user_input.lower().strip()

    for command_name, patterns in _COMMAND_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                response = _get_command_response(command_name)
                return {
                    "is_command": True,
                    "command": command_name,
                    "response": response,
                    "original_input": user_input,
                }

    return {
        "is_command": False,
        "command": None,
        "response": "",
        "original_input": user_input,
    }


def _get_command_response(command: str) -> str:
    """Return a spoken response for a recognized command."""
    responses = {
        "go_back": "Going back to the previous step.",
        "repeat": "I'll repeat my last response.",
        "next": "Continuing.",
        "stop": "Stopping. Let me know when you'd like to continue.",
        "help": _HELP_TEXT,
        "slower": "Slowing down my speech.",
        "faster": "Speeding up my speech.",
        "louder": "Speaking louder.",
        "softer": "Speaking softer.",
        "start_over": "Starting over from the beginning.",
        "read_results": "Reading your results now.",
    }
    return responses.get(command, "Command recognized.")


def get_available_commands() -> dict:
    """Return a list of all available voice commands for display/announcement."""
    return {
        "commands": list(_COMMAND_PATTERNS.keys()),
        "help_text": _HELP_TEXT,
        "count": len(_COMMAND_PATTERNS),
    }
