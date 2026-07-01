"""
run.py
------
Convenience launcher so you can start the app with: `python run.py`
Equivalent to running uvicorn manually.
"""

import uvicorn
from app.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=(settings.app_env == "development"),  # auto-reload in dev only
    )