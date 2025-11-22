from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
)
from sqlmodel import SQLModel

from app.schemas.model_metadata import ModelMetadata
from app.utils.config import CONFIG


class DatabaseEngineBase(ABC):
    def __init__(self, db_url: str):
        self.db_url = db_url
    
    @abstractmethod
    async def init_db(self):
        pass

    @classmethod
    async def create_db_and_tables(cls, engine: AsyncEngine):
        async with engine.begin() as conn:
            await conn.run_sync(
                SQLModel.metadata.create_all,
                tables=[
                    ModelMetadata.__table__,
                ],
                checkfirst=True
            )

class MysqlEngine(DatabaseEngineBase):
    def __init__(self):
        self.db_url = f"mysql+asyncmy://{CONFIG.database_user}:{CONFIG.database_password}@{CONFIG.database_host}:{CONFIG.database_port}/{CONFIG.database_name}"

    async def init_db(self):
        try:
            engine = create_async_engine(
                self.db_url,
                pool_size=10,
                pool_recycle=300,
                pool_pre_ping=True,
                max_overflow=20)

            await self.create_db_and_tables(engine)

            return engine
        except Exception as e:
            print(f"Error initializing database engine: {e}")
            raise

database_engine_dict = {
    "mysql": MysqlEngine,
}

def get_database_engine(db_type: str):
    return database_engine_dict[db_type]