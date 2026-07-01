"""
user_memory.py
--------------
JSON-file-based persistence for user profiles.

Profiles are saved to data/users/<user_id>.json so they survive
server restarts. In production, swap this for a real database.
"""

import json
import os
from typing import Optional

from app.models.user_model import UserProfile, UserProfileUpdate

# Directory where user profiles are stored
_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "users")


def _ensure_dir() -> None:
    """Create the data/users directory if it doesn't exist."""
    os.makedirs(_DATA_DIR, exist_ok=True)


def _profile_path(user_id: str) -> str:
    return os.path.join(_DATA_DIR, f"{user_id}.json")


def save_profile(profile: UserProfile) -> None:
    """Persist a user profile to disk."""
    _ensure_dir()
    with open(_profile_path(profile.user_id), "w", encoding="utf-8") as f:
        json.dump(profile.model_dump(), f, indent=2)


def load_profile(user_id: str) -> Optional[UserProfile]:
    """Load a user profile from disk. Returns None if not found."""
    path = _profile_path(user_id)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return UserProfile(**data)


def get_or_create_profile(user_id: str, name: str = "") -> UserProfile:
    """Return existing profile or create a new default one."""
    profile = load_profile(user_id)
    if profile is None:
        profile = UserProfile(user_id=user_id, name=name)
        save_profile(profile)
    return profile


def update_profile(user_id: str, update: UserProfileUpdate) -> Optional[UserProfile]:
    """Apply partial update to a profile and save. Returns None if user not found."""
    profile = load_profile(user_id)
    if profile is None:
        return None
    update_data = update.model_dump(exclude_none=True)
    updated = profile.model_copy(update=update_data)
    save_profile(updated)
    return updated


def delete_profile(user_id: str) -> bool:
    """Delete a user profile file. Returns True if it existed."""
    path = _profile_path(user_id)
    if os.path.exists(path):
        os.remove(path)
        return True
    return False


def list_users() -> list[str]:
    """List all user IDs that have saved profiles."""
    _ensure_dir()
    return [
        f.replace(".json", "")
        for f in os.listdir(_DATA_DIR)
        if f.endswith(".json")
    ]
