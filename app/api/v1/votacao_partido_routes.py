from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_filter import FilterDepends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.filters.votacao_partido_filters import VotacaoPartidoFilter
from app.models.resultados.votacao_partido_munzona import VotacaoPartidoMunZona
from app.schemas.votacao_partido_schema import VotacaoPartidoMunZonaResponse

router = APIRouter(prefix="/partidos")


@router.get(
    "/",
    response_model=Page[VotacaoPartidoMunZonaResponse],
    summary="Listar votação por partido",
)
async def list_votation_parties(
        votation_parties_filter: VotacaoPartidoFilter = FilterDepends(VotacaoPartidoFilter),
        db: AsyncSession = Depends(get_db_session),
) -> Page[VotacaoPartidoMunZonaResponse]:
    """
    Lista votação por partido com filtros automáticos.
    """
    try:
        logger.info(f"📥 Recebendo requisição de partidos com filtros: {votation_parties_filter}")
        base_query = votation_parties_filter.filter(select(VotacaoPartidoMunZona))
        base_query = votation_parties_filter.sort(base_query)
        return await paginate(db, base_query)
    except Exception as e:
        logger.error(f"❌ Erro no endpoint de partidos: {e}", exc_info=True)
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            f"Erro ao buscar votação por partido: {str(e)}"
        )


@router.get("/{party_id}", response_model=VotacaoPartidoMunZonaResponse)
async def get_details_party_vote(
        party_id: UUID,
        db: AsyncSession = Depends(get_db_session),
):
    """Retorna detalhes de um registro específico de votação por partido (município/zona)."""
    try:
        logger.info(f"🔍 Buscando votação por partido ID: {party_id}")

        result = await db.execute(
            select(VotacaoPartidoMunZona).where(VotacaoPartidoMunZona.id == party_id)
        )
        party_vote = result.scalar_one_or_none()
        if not party_vote:
            logger.warning(f"Registro de votação por partido não encontrado: {party_id}")
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                "Registro de votação por partido não encontrado",
            )

        return VotacaoPartidoMunZonaResponse.from_orm(party_vote)

    except Exception as e:
        logger.error(f"Erro ao buscar detalhes de votação por partido: {str(e)}")
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            f"Erro ao buscar detalhes de votação por partido: {str(e)}",
        )
