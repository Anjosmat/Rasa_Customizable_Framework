from pathlib import Path
from .db_config import SessionLocal, BusinessIntent, BotConfig, Base, engine

MIGRATIONS_DIR = Path(__file__).parent
VERSIONS_DIR = MIGRATIONS_DIR / "versions"
# Create directories if they don't exist
VERSIONS_DIR.mkdir(parents=True, exist_ok=True)

__all__ = ['SessionLocal', 'BusinessIntent', 'BotConfig', 'Base', 'engine']
