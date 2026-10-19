# Engine and session setup(Connect to the database)

from sqlmodel import create_engine
# Use SQLite and tell the databse to create this file named apicraft.db if it does not exists
DATABASE_URL=(
    "mssql+pyodbc://localhost/APICraft"
    "?driver=ODBC+Driver+18+for+SQL+Server"
    "&trusted_connection=yes"
    "&TrustServerCertificate=yes"
    )


engine=create_engine(
    DATABASE_URL,
    echo=True
)