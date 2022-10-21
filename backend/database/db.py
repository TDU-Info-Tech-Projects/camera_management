from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

db_string = '{}://{}:{}@{}:{}/{}'.format(
    getenv("DATABASE", "postgresql"),
    getenv("POSTGRES_USER"),
    getenv("POSTGRES_PASSWORD"),
    getenv("DATABASE_ADDRESS"),
    getenv("DATABASE_PORT"),
    getenv("POSTGRES_DB")
)

print(db_string, flush=True)
engine = create_engine(db_string)