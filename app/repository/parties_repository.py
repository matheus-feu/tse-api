from typing import List, Dict

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.bulk_upsert import bulk_upsert
from app.models.parties import VotoPartidoMunZona


class PartiesRepository:
    """Repository para votação por partido - versão otimizada."""

    def __init__(self, db_session: AsyncSession):
        """
        Inicializa o repository.
        """
        self.db_session = db_session

    async def bulk_upsert_votes(self, vote_records: List[Dict]) -> int:
        """
        Realiza um upsert em massa dos registros de votação por partido.
        """
        unique_fields = [
            'ano_eleicao', 'sg_uf', 'cd_municipio', 'nr_zona', 'nr_turno', 'nr_partido', 'cd_cargo'

        ]
        return await bulk_upsert(
            self.db_session,
            VotoPartidoMunZona,
            vote_records,
            unique_fields,
            skip_update=['id']
        )
