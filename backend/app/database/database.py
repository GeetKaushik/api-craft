# Engine and session setup(Connect to the database)

from sqlmodel import create_engine

# Use SQLite and tell the databse to create this file named apicraft.db if it does not exists
DATABASE_URL="sqlite:///apicraft.db"


engine=create_engine(
    DATABASE_URL,
    echo=True
)