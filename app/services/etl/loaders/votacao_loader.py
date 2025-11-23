from typing import List, Dict

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.candidates_repository import CandidatesRepository
from app.repository.parties_repository import PartiesRepository


class VotationLoader:
    """Carrega dados transformados no banco de dados."""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.repo_candidate = CandidatesRepository(db_session)
        self.repo_partie = PartiesRepository(db_session)

    async def load_candidates(self, records: List[Dict]) -> int:
        """Carrega dados de votação por candidato no banco."""
        if not records:
            logger.info("Nenhum registro para carregar.")
            return 0

        count = await self.repo_candidate.bulk_upsert_votes(records)
        logger.info(f"✅ {count} registros salvos")
        return count

    async def load_parties(self, records: List[Dict]) -> int:
        """Carrega dados de votação por partido no banco."""
        if not records:
            logger.info("Nenhum registro para carregar.")
            return 0

        count = await self.repo_partie.bulk_upsert_votes(records)
        logger.info(f"✅ {count} registros salvos")
        return count
