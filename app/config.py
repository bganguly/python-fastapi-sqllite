from __future__ import annotations

import os


def get_database_url() -> str:
    return os.getenv("DATABASE_URL", "sqlite:///./app.db")


def auto_seed_enabled() -> bool:
    return os.getenv("AUTO_SEED_ON_STARTUP", "true").lower() in {"1", "true", "yes"}
