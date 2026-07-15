from app.db.base import Base
from app.db.engine import engine

# Import tables so SQLAlchemy registers them with Base.metadata.
from app.db import tables  # noqa: F401


def create_database_tables() -> None:
    Base.metadata.create_all(bind=engine)