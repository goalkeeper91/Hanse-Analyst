from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

DATABASE_URL = "sqlite+aiosqlite:///./hanse_analyst.db"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    content = Column(Text)
    doc_type = Column(String) # e.g., "Rechnung", "Vertrag"
    summary = Column(Text)
    upload_date = Column(DateTime, default=datetime.utcnow)

async def init_db():
    print("Attempting to initialize database...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database initialization complete (or attempted).")
