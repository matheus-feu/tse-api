from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.bulk_upsert import bulk_upsert
from app.models.candidates import VotoCandidatoMunZona


class CandidatesRepository:
    """Repositório para operações de banco de dados relacionadas a votos de candidatos por município e zona."""

    def __init__(self, db_session: AsyncSession):
        """
        Inicializa o repository.
        """
        self.db_session = db_session

    async def bulk_upsert_votes(self, vote_records: List[dict]) -> int:
        """
        Realiza um upsert em massa dos registros de votação de candidatos.
        """
        unique_fields = [
            'ano_eleicao', 'nr_turno', 'sg_uf', 'cd_municipio', 'nr_zona', 'nr_candidato'
        ]
        return await bulk_upsert(
            self.db_session,
            VotoCandidatoMunZona,
            vote_records,
            unique_fields,
            skip_update=['id']
        )
