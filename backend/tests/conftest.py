import pytest
import asyncio
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models.database import Base
from app.api.endpoints import get_db
from app.main import app

# Test-Datenbank (In-Memory)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestAsyncSessionLocal = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)

async def override_get_db():
    async with TestAsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db():
    # Tabellen in der Test-DB erstellen
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Die Abhängigkeit in der FastAPI App überschreiben
    app.dependency_overrides[get_db] = override_get_db
    
    yield
    
    # Am Ende die Overrides löschen und Engine schließen
    app.dependency_overrides.clear()
    await test_engine.dispose()
