"""
config.py
---------
Central configuration loader for the Visual Job Coach Agent.

Design notes:
- We use pydantic-settings so all config is validated and type-safe.
- Secrets are loaded from environment variables (.env locally), NEVER hardcoded.
- A single `settings` object is imported across the app for consistency.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ----- LLM / AI -----
    google_api_key: str = ""
    openai_api_key: str = ""

    # ----- Speech -----
    speech_api_key: str = ""

    # ----- Job API -----
    job_api_key: str = ""
    job_api_base_url: str = "https://jsearch.p.rapidapi.com"

    # ----- Security -----
    app_secret_key: str = "dev_secret_change_me"
    api_auth_token: str = "vjc-dev-token-2024"
    rate_limit_per_minute: int = 60

    # ----- App -----
    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    # Tell pydantic to read from the .env file
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # ignore unknown env vars instead of crashing
    )


# Single shared settings instance used throughout the app
settings = Settings()