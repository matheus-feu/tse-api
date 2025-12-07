from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_filter import FilterDepends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.filters.votacao_candidato_filters import VotacaoCandidatoFilter
from app.models.resultados.votacao_candidato_munzona import VotacaoCandidatoMunZona
from app.schemas.votacao_candidato_schema import VotacaoCandidatoMunZonaResponse

router = APIRouter(prefix="/candidatos")


@router.get(
    "/",
    response_model=Page[VotacaoCandidatoMunZonaResponse],
    summary="Listar votação por candidato",
)
async def list_votation_candidates(
        votation_candidates_filter: VotacaoCandidatoFilter = FilterDepends(VotacaoCandidatoFilter),
        db: AsyncSession = Depends(get_db_session),
) -> Page[VotacaoCandidatoMunZonaResponse]:
    """
    Lista votação por candidato com filtros e paginação automática (page/size).
    """
    try:
        base_query = votation_candidates_filter.filter(select(VotacaoCandidatoMunZona))
        base_query = votation_candidates_filter.sort(base_query)

        page = await paginate(db, base_query)
        return page
    except Exception as e:
        logger.error(f"Erro no endpoint: {e}", exc_info=True)
        raise HTTPException(500, f"Erro ao buscar votação: {str(e)}")


@router.get("/{candidate_id}", response_model=VotacaoCandidatoMunZonaResponse)
async def get_details_candidate(
        candidate_id: UUID,
        db: AsyncSession = Depends(get_db_session)
):
    """Retorna detalhes de um registro específico."""
    try:
        logger.info(f"🔍 Buscando candidato ID: {candidate_id}")

        result = await db.execute(
            select(VotacaoCandidatoMunZona).where(
                VotacaoCandidatoMunZona.id == candidate_id
            )
        )
        candidate = result.scalar_one_or_none()
        if not candidate:
            logger.warning(f"Registro de votação não encontrado: {candidate_id}")
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Registro não encontrado")

        return VotacaoCandidatoMunZonaResponse.from_orm(candidate)

    except Exception as e:
        logger.error(f"Erro ao buscar detalhes do candidato: {str(e)}")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Erro ao buscar detalhes: {str(e)}")
