import os

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, declarative_base
from settings import settings

# engine = create_async_engine(settings.database_url)
# SessionLocal = sessionmaker(bind=engine, autoflush=False, class_=AsyncSession) autocommit=False
# DATABASE_URL = "postgresql+psycopg2://restaurant:restaurant@localhost:5432/restaurant"

# engine = create_engine(os.getenv('DATABASE_URL', default=''))


engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
#
# Base.metadata.create_all(engine)

