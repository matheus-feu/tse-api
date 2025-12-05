from typing import Sequence

from fastapi_filter.contrib.sqlalchemy import Filter
from loguru import logger
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.resultados.votacao_candidato_munzona import VotacaoCandidatoMunZona


class VotationRepository:
    """Repository para consultas de votação."""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def find_with_filters(
            self,
            filter_model: Filter,
            limit: int = 100,
            offset: int = 0
    ) -> tuple[Sequence[VotacaoCandidatoMunZona], int]:
        """
        Busca votação com filtros usando fastapi-filter.

        Args:
            filter_model: Filtros aplicados
            limit: Limite de registros
            offset: Offset para paginação

        Returns:
            Tupla (resultados, total)
        """
        try:
            query = select(VotacaoCandidatoMunZona)
            query = filter_model.filter(query)
            query = filter_model.sort(query)
            query = query.limit(limit).offset(offset)

            count_query = select(func.count()).select_from(VotacaoCandidatoMunZona)
            count_query = filter_model.filter(count_query)

            import asyncio
            result, total_result = await asyncio.gather(
                self.db_session.execute(query),
                self.db_session.execute(count_query)
            )

            results = result.scalars().all()
            total = total_result.scalar()

            logger.debug(f"✅ Query executada - {len(results)} resultados, total={total}")
            return results, total

        except Exception as e:
            logger.error(f"❌ Erro em find_with_filters: {e}", exc_info=True)
            raise
