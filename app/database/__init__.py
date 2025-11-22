from sqlmodel.ext.asyncio.session import AsyncSession

from app.database.engine import MysqlEngine, get_database_engine
from app.utils.config import CONFIG

_engine = None

def get_engine():
    return _engine

async def get_session():
    async with AsyncSession(_engine) as session:
        yield session

async def init_db():
    db_engine = get_database_engine(CONFIG.database_engine)
    global _engine
    _engine = await db_engine().init_db()
