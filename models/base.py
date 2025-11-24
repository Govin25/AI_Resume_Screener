from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

database = os.getenv("POSTGRES_DB")
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")

DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{database}"
SQLITE_DATABASE_URL = f"sqlite:///{database}.db"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# for creating models use this base
Base = declarative_base()

# for getting data using this session
session = SessionLocal()

