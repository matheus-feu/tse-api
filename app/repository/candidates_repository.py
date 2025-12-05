from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.bulk_upsert import bulk_upsert
from app.models.resultados.votacao_candidato_munzona import VotacaoCandidatoMunZona


class CandidatesRepository:
    """Repositório para operações de banco de dados relacionadas a votos de candidatos por município e zona."""

    def __init__(self, db_session: AsyncSession):
        """
        Inicializa o repository.
        """
        self.db_session = db_session

    async def _dedupe_by_key(self, records: List[dict], unique_fields: list[str]) -> List[dict]:
        seen = set()
        deduped = []
        for r in records:
            key = tuple(r.get(f) for f in unique_fields)
            if key in seen:
                continue
            seen.add(key)
            deduped.append(r)
        return deduped

    async def bulk_upsert_votes(self, vote_records: List[dict]) -> int:
        """
        Realiza um upsert em massa dos registros de votação de candidatos.
        """
        unique_fields = [
            'ano_eleicao', 'nr_turno', 'sg_uf', 'cd_municipio', 'nr_zona', 'nr_candidato'
        ]

        records = await self._dedupe_by_key(vote_records, unique_fields)

        return await bulk_upsert(
            self.db_session,
            VotacaoCandidatoMunZona,
            records,
            unique_fields,
            skip_update=['id']
        )
