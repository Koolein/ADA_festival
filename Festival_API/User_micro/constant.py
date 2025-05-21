import os
import urllib.parse

# Cloud SQL Postgres credentials and connection info
DB_USER = os.getenv("DB_USER", "api_user")
DB_PASS = os.getenv("DB_PASS", "yourStrongP@ss")
DB_NAME = os.getenv("DB_NAME", "userdb")
DB_HOST = os.getenv("DB_HOST", "34.46.26.37")
DB_PORT = os.getenv("DB_PORT", "5432")

# Percent-encode special characters (e.g. '@' → '%40')
DB_PASS_ENCODED = urllib.parse.quote_plus(DB_PASS)

DB_URL = (
    f"postgresql+psycopg2://"
    f"{DB_USER}:{DB_PASS_ENCODED}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
