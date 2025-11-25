from uuid import UUID

from fastapi import APIRouter, Depends, Query, HTTPException, status
from fastapi_filter import FilterDepends
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.filters.votation_filters import VotationCandidateFilter
from app.models.candidates import VotoCandidatoMunZona
from app.repository.votation_repository import VotationRepository
from app.schemas.votation_schemas import VotationPaginatedResponse, VotationCandidateResponse

router = APIRouter(prefix="/votation")


@router.get("/candidates", response_model=VotationPaginatedResponse)
async def list_votation_candidates(
        votation_filter: VotationCandidateFilter = FilterDepends(VotationCandidateFilter),
        limit: int = Query(100, ge=1, le=1000, description="Limite de registros"),
        offset: int = Query(0, ge=0, description="Offset para paginação"),
        db: AsyncSession = Depends(get_db_session)
):
    """
    Lista votação por candidato com filtros automáticos.

    ## Filtros disponíveis:
    - **ano_eleicao**: Ano da eleição
    - **sg_uf**: Sigla do estado
    - **nr_candidato**: Número do candidato
    - **sg_partido**: Sigla do partido
    - **ds_cargo__ilike**: Cargo (busca parcial)
    - **nm_candidato__ilike**: Nome do candidato (busca parcial)
    - **qt_votos_nominais__gte**: Votos >= valor
    - **qt_votos_nominais__lte**: Votos <= valor
    - **sg_uf__in**: Lista de UFs (ex: ["SP", "RJ"])
    - **order_by**: Ordenação (ex: "-qt_votos_nominais" para desc)
    - **search**: Busca geral em nome_candidato e nome_municipio
    """

    try:
        logger.info(f"📥 Recebendo requisição com filtros: {votation_filter}")

        repo = VotationRepository(db)
        results, total = await repo.find_with_filters(
            filter_model=votation_filter,
            limit=limit,
            offset=offset
        )
        logger.info(f"✅ Query executada - {len(results)} resultados, total={total}")
        
        return VotationPaginatedResponse(
            total=total,
            limit=limit,
            offset=offset,
            data=[VotationCandidateResponse.model_validate(r) for r in results]
        )
    except Exception as e:
        logger.error(f"❌ Erro no endpoint: {e}", exc_info=True)
        raise HTTPException(500, f"Erro ao buscar votação: {str(e)}")


@router.get("/candidates/{candidate_id}", response_model=VotationCandidateResponse)
async def get_details_candidate(
        candidate_id: UUID,
        db: AsyncSession = Depends(get_db_session)
):
    """Retorna detalhes de um registro específico."""
    try:
        logger.info(f"🔍 Buscando candidato ID: {candidate_id}")

        result = await db.execute(
            select(VotoCandidatoMunZona).where(
                VotoCandidatoMunZona.id == candidate_id
            )
        )
        candidate = result.scalar_one_or_none()
        if not candidate:
            logger.warning(f"Registro de votação não encontrado: {candidate_id}")
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Registro não encontrado")

        return VotationCandidateResponse.from_orm(candidate)

    except Exception as e:
        logger.error(f"Erro ao buscar detalhes do candidato: {str(e)}")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Erro ao buscar detalhes: {str(e)}")
