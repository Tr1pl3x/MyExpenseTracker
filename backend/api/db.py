import os
from sqlmodel import SQLModel, create_engine
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# remove/disable: SQLModel.metadata.create_all(engine)
def init_db():
    pass  # migrations own the schema now


