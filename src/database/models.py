from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.utils.config import get_settings

settings = get_settings()
engine = create_engine(settings.db_url, connect_args={"check_same_thread": False} if settings.db_url.startswith("sqlite") else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    from src.database.models import Base
    Base.metadata.create_all(bind=engine)


def check_db() -> bool:
    try:
        with engine.connect() as connection:
            connection.execute("SELECT 1")
        return True
    except Exception:
        return False
