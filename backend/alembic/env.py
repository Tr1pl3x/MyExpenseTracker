import os
from dotenv import load_dotenv
from sqlmodel import SQLModel
from api import models  # ensure tables are imported

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

from alembic import context
from sqlalchemy import create_engine, pool

config = context.config
target_metadata = SQLModel.metadata

def run_migrations_offline():
    context.configure(url=DATABASE_URL, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = create_engine(DATABASE_URL, poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
