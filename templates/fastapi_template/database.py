from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

database_name = "db"
database_username = "p"
database_password = "root"
database_hostname = "localhost"

SQLALCHEMY_DATABASE_URL = f"postgresql://{database_username}:{database_password}@{database_hostname}/{database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def run_postgres_script(script_path: str):
    command = f"psql -h {database_hostname} -d {database_name} -U {database_username} -W < {script_path}"
    os.system(command)
