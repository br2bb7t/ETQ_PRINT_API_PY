from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.config import CONFIG
from infrastructure.database.decrypt import DecryptService
from infrastructure.logging.LoggerImplements import LoggerImplements

log_impl = LoggerImplements("DbContextLogger")

SESSIONS = {}

try:
    encrypted_db_url = CONFIG.get("DB_SQLITE")

    if not encrypted_db_url:
        raise ValueError("DB_SQLITE environment variable not found")

    database_url = DecryptService.decrypt(encrypted_db_url)

    db_echo = CONFIG.get("DB_ECHO", "false").lower() == "true"

    engine = create_engine(database_url, echo=db_echo, connect_args={"check_same_thread": False})

    SESSIONS["sqlite"] = sessionmaker(bind=engine, autocommit=False, autoflush=False)

    log_impl.log_information("SQLite database initialized successfully", "DbContext")

except Exception as ex:
    log_impl.log_error(f"Error initializing database: {str(ex)}", "DbContext")
    raise


@contextmanager
def get_db_session(db_name: str = "sqlite"):
    """
    Context manager to retrieve a session for the specified database.
    Usage:
        with get_db_session("sqlite") as session:
            session.execute(...)
    """

    Session = SESSIONS.get(db_name)

    if not Session:

        raise ValueError(f"Database [{db_name}] is not configured")

    session = Session()

    try:
        log_impl.log_information(f"Opening session [{db_name}]", "get_db_session")
        yield session

        session.commit()

    except Exception as ex:
        session.rollback()
        log_impl.log_error(f"Rollback executed: {str(ex)}", "get_db_session")
        raise

    finally:
        session.close()
        log_impl.log_information(f"Closing session [{db_name}]", "get_db_session")


def get_available_databases():
    """
    Returns configured databases.
    """

    return list(SESSIONS.keys())


def get_engine():
    """
    Returns SQLAlchemy engine.
    """

    return engine


def get_session_factory():
    """
    Returns Session factory.
    """

    return SESSIONS["sqlite"]
