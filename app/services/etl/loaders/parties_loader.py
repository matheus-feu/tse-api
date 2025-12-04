from typing import List, Dict
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.parties_repository import PartiesRepository


class PartiesLoader:
    """Carrega dados transformados no banco de dados."""
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.repo_party = PartiesRepository(db_session)

    async def load_parties(self, records: List[Dict]) -> int:
        """Carrega dados de votação por partido no banco."""
        if not records:
            logger.info("Nenhum registro para carregar.")
            return 0

        return await self.repo_party.bulk_upsert_votes(records)
