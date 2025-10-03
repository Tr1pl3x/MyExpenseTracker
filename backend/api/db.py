import os
from sqlmodel import SQLModel, create_engine
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

def init_db():
    from . import models  # ensure models are imported
    SQLModel.metadata.create_all(engine)
