from __future__ import annotations

from threading import Lock
from typing import Generator, Optional

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import DeclarativeBase, Session


class Base(DeclarativeBase):
    """Declarative base class for SQLAlchemy models."""


class DBConnectionManager:
    """
    Static class to manage the database connection.

    Initialize it with a connection to a database, and then use it to access
    the database through sessions.
    """

    engine: Optional[Engine] = None
    _lock = Lock()

    def __init__(self):
        """Delete the initializer to prevent instantiation of this class."""
        raise NotImplementedError(
            "DBConnectionManager is a static class and cannot be instantiated."
            "Use init_with_postgresql_db() method instead."
        )

    @classmethod
    def init_with_postgresql_db(  # noqa: PLR0913
        cls: type[DBConnectionManager],
        user: str,
        password: str,
        host: str = "localhost",
        port: int = 5432,
        db_name: str = "appdb",
    ) -> None:
        """
        Initialize the database and create all tables.

        Parameters allow configuring the database connection.
        """
        if cls.engine is not None:
            raise RuntimeError(
                "The database engine has already been initialized and it is"
                " not permitted to initialize it twice."
            )

        with cls._lock:
            if cls.engine is not None:
                # Double-checked locking.
                raise RuntimeError(
                    "The database engine has already been initialized and it is"
                    " not permitted to initialize it twice."
                )

            url = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"

            cls.engine = create_engine(url)
            Base.metadata.create_all(cls.engine)

    @classmethod
    def get_session(
        cls: type[DBConnectionManager],
    ) -> Generator[Session, None, None]:
        """Get a new database session."""
        if cls.engine is None:
            raise RuntimeError(
                "Database engine not initialized. Call init_db() first."
            )

        with Session(cls.engine) as session:
            yield session
