from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.settings import settings

Base = declarative_base()

engine = create_async_engine(settings.database_url, echo=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_db():
	async with AsyncSessionLocal() as async_session:
		yield async_session

# engine = create_engine(settings.database_url)
# SessionLocal = sessionmaker(bind=engine)
