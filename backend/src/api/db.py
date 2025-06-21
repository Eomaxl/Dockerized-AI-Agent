import os
import sqlmodel
from sqlmodel import Session, SQLModel, inspect
from sqlalchemy.exc import ProgrammingError

DATABASE_URL = os.environ.get("DATABASE_URL", "")
if not DATABASE_URL:
    raise NotImplementedError("`DATABASE_URL` needs to be set.")

DATABASE_URL = DATABASE_URL.replace("postgres://", "postgres+psycopg://")
engine = sqlmodel.create_engine(DATABASE_URL)

def init_db():
    from api.chat.models import ChatMessage  # lazy import to avoid circular imports
    try:
        inspector = inspect(engine)
        if "chatmessage" not in inspector.get_table_names():
            print("✅ Creating table 'chatmessage'...")
            SQLModel.metadata.create_all(engine, tables=[ChatMessage.__table__])
        else:
            print("ℹ️ Table 'chatmessage' already exists.")
    except ProgrammingError as e:
        print(f"❌ DB privilege error: {e}")
        print("⚠️ Skipping table creation due to permission error.")

def get_session():
    with Session(engine) as session:
        yield session