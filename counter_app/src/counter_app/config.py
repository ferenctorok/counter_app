import os
from typing import Final

POSTGRES_HOST: Final = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT: Final = int(os.getenv("POSTGRES_PORT", "5432"))
POSTGRES_DB: Final = os.getenv("POSTGRES_DB", "appdb")
POSTGRES_USER: Final = os.getenv("POSTGRES_USER", "appuser")
POSTGRES_PASSWORD: Final = os.getenv("POSTGRES_PASSWORD", "secret")
