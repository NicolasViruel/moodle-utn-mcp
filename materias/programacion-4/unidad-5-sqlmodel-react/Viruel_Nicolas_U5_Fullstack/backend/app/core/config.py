import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


@lru_cache
def get_database_url() -> str:
    return os.getenv(
        "DATABASE_URL",
        "postgresql://gestor:gestor@localhost:5432/gestor_productos",
    )
