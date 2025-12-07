from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_filter import FilterDepends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.filters.consulta_candidato_filters import ConsultaCandidatoFilter
from app.models.candidatos.consulta_candidato import ConsultaCandidatos
from app.schemas.consulta_candidato_schema import ConsultaCandidatoResponse

router = APIRouter(prefix="/consulta_candidatos")


@router.get(
    "/",
    response_model=Page[ConsultaCandidatoResponse],
    summary="Listar consulta de candidatos",
)
async def list_consult_candidates(
        candidate_filter: ConsultaCandidatoFilter = FilterDepends(ConsultaCandidatoFilter),
        db: AsyncSession = Depends(get_db_session),
) -> Page[ConsultaCandidatoResponse]:
    """Lista consulta de candidatos com filtros automáticos."""

    try:
        logger.info(f"📥 Recebendo requisição de candidatos com filtros: {candidate_filter}")
        base_query = candidate_filter.filter(select(ConsultaCandidatos))
        base_query = candidate_filter.sort(base_query)
        return await paginate(db, base_query)
    except Exception as e:
        logger.error(f"❌ Erro no endpoint de candidatos: {e}", exc_info=True)
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            f"Erro ao buscar consulta de candidatos: {str(e)}"
        )
