import os

import sqlmodel
from sqlmodel import Session, SQLModel

# DATABASE_URL = os.environ.get("DATABASE_URL")
DATABASE_URL = "postgresql+psycopg://dbuser:db-password@db_service:5432/mydb"

if DATABASE_URL == "":
    raise NotImplementedError("`DATABASE_URL` needs to be set.")

DATABASE_URL = DATABASE_URL.replace("postgres://","postgres+psycopg://")

engine  = sqlmodel.create_engine(DATABASE_URL)

# database models
def init_db():
    print("Creating database tables...")
    SQLModel.metadata.create_all(engine)

# api routes
def get_session():
    with Session(engine) as session:
        yield session