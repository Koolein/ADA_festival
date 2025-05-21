import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# read creds from env
DB_USER = os.getenv("DB_USER", "api_user")
DB_PASS = os.getenv("DB_PASS", "yourStrongP@ss")
DB_NAME = os.getenv("DB_NAME", "userdb")
DB_HOST = os.getenv("DB_HOST", "34.46.26.37")
DB_PORT = int(os.getenv("DB_PORT", "5432"))

# build engine without user:pass@host in the URL
engine = create_engine(
    "postgresql+psycopg2://",
    connect_args={
        "user": DB_USER,
        "password": DB_PASS,
        "host": DB_HOST,
        "port": DB_PORT,
        "database": DB_NAME,
    },
    echo=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
