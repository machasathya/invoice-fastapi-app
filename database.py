from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.config import Settings, settings

# URL-encode the password to handle special characters like '@'
ENCODED_MYSQL_PASSWORD = quote_plus(settings.MYSQL_PASSWORD)  # <--- ENCODE THE PASSWORD

# Replace with your MySQL connection details
SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{settings.MYSQL_USER}:{ENCODED_MYSQL_PASSWORD}@{settings.MYSQL_HOST}/{settings.MYSQL_DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
