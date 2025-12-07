from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_filter import FilterDepends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.filters.perfil_comparecimento_abstencao_filters import PerfilComparecimentoFilter
from app.models.comparecimento_abstencao.perfil_comparecimento_abstencao import PerfilComparecimentoAbstencao
from app.schemas.perfil_comparecimento_abstencao_schema import PerfilComparecimentoAbstencaoResponse

router = APIRouter(prefix="/perfil_votacao")


@router.get(
    "/",
    response_model=Page[PerfilComparecimentoAbstencaoResponse],
    summary="Listar perfil de comparecimento e abstenção"
)
async def list_ṕrofile_votation(
        profile_filters: PerfilComparecimentoFilter = FilterDepends(PerfilComparecimentoFilter),
        db: AsyncSession = Depends(get_db_session)
) -> Page[PerfilComparecimentoAbstencaoResponse]:
    """Lista os perfis de comparecimento e abstenção com base nos filtros fornecidos."""

    try:
        logger.info(f"📥 Recebendo requisição com filtros: {profile_filters}")
        base_query = profile_filters.filter(select(PerfilComparecimentoAbstencao))
        base_query = profile_filters.sort(base_query)
        return await paginate(db, base_query)
    except Exception as e:
        logger.error(f"❌ Erro no endpoint: {e}", exc_info=True)
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            f"Erro ao buscar perfil de comparecimento e abstenção: {str(e)}"
        )
