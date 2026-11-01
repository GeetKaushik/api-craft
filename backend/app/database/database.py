import os

from dotenv import load_dotenv
from sqlalchemy.engine import URL
from sqlmodel import create_engine

# Load environment variables from backend/.env
load_dotenv()

DB_PASSWORD = os.getenv("DB_PASSWORD")

if not DB_PASSWORD:
    raise ValueError("DB_PASSWORD is missing from the .env file")

DATABASE_URL = URL.create(
    drivername="mssql+pyodbc",
    username="sa",
    password=DB_PASSWORD,
    host="127.0.0.1",
    port=1433,
    database="APICraft",
    query={
        "driver": "ODBC Driver 18 for SQL Server",
        "TrustServerCertificate": "yes",
    },
)

engine = create_engine(
    DATABASE_URL,
    echo=True,
)
