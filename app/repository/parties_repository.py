from typing import Tuple, Sequence

from loguru import logger
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.resultados.votacao_partido_munzona import VotacaoPartidoMunZona


class PartiesRepository:
    """Repository para votação por partido - versão otimizada."""

    def __init__(self, db_session: AsyncSession):
        """
        Inicializa o repository.
        """
        self.db_session = db_session

    async def find_with_filters(
            self,
            filter_model,
            limit: int = 100,
            offset: int = 0,
    ) -> Tuple[Sequence[VotacaoPartidoMunZona], int]:
        """
        Aplica VotationPartyFilter e retorna (results, total).
        """
        try:
            logger.info(
                "🔎 Buscando votação por partido com filtros: {}, limit={}, offset={}",
                filter_model,
                limit,
                offset,
            )

            base_query = select(VotacaoPartidoMunZona)
            filtered_query = filter_model.filter(base_query)

            count_query = select(func.count()).select_from(filtered_query.subquery())
            total = (await self.db_session.execute(count_query)).scalar_one()

            result = await self.db_session.execute(
                filtered_query.limit(limit).offset(offset)
            )
            rows = result.scalars().all()

            logger.info(
                "✅ Consulta de votação por partido concluída: {} registros retornados, total={}",
                len(rows),
                total,
            )
            return rows, total

        except Exception as exc:
            logger.error(
                "❌ Erro ao executar find_with_filters em PartiesRepository: {}",
                exc,
                exc_info=True,
            )
            raise
