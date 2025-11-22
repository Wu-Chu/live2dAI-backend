import asyncio
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_engine, get_session, init_db
from app.services.model_metadata import ModelMetadataService
from app.utils.logger import LOG


class Live2dAI:
    async def start(self):
        LOG.info("ModelRepository start")

        await self._prepare_data()

        while 1:
            await asyncio.sleep(0)


    async def _prepare_data(self):
        await init_db()

        engine = get_engine()
        async with AsyncSession(engine) as session:
            await self._init_data(session)

    async def _init_data(self, session: AsyncSession):
        await ModelMetadataService().register_model_metadata(session)