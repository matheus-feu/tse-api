from uuid import UUID

from fastapi import APIRouter, Depends, Query, HTTPException, status
from fastapi_filter import FilterDepends
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.filters.votation_filters import VotationCandidateFilter, VotationPartyFilter
from app.models.resultados.votacao_candidato_munzona import VotacaoCandidatoMunZona
from app.models.resultados.votacao_partido_munzona import VotacaoPartidoMunZona
from app.repository.parties_repository import PartiesRepository
from app.repository.votation_repository import VotationRepository
from app.schemas.votation_schemas import VotationPaginatedResponse, VotationCandidateResponse, \
    VotationPartyPaginatedResponse, VotationPartyResponse

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
            select(VotacaoCandidatoMunZona).where(
                VotacaoCandidatoMunZona.id == candidate_id
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


@router.get("/parties", response_model=VotationPartyPaginatedResponse)
async def list_votation_parties(
        votation_filter: VotationPartyFilter = FilterDepends(VotationPartyFilter),
        limit: int = Query(100, ge=1, le=1000, description="Limite de registros"),
        offset: int = Query(0, ge=0, description="Offset para paginação"),
        db: AsyncSession = Depends(get_db_session),
):
    """
    Lista votação por partido com filtros automáticos.

    Exemplos de filtros esperados no VotationPartyFilter:
    - ano_eleicao, sg_uf, cd_municipio, nr_zona
    - nr_partido, sg_partido
    - ds_cargo__ilike, nm_municipio__ilike
    - qt_total_votos_leg_validos__gte / __lte
    - order_by, search
    """
    try:
        logger.info(f"📥 Recebendo requisição de partidos com filtros: {votation_filter}")

        repo = PartiesRepository(db)
        results, total = await repo.find_with_filters(
            filter_model=votation_filter,
            limit=limit,
            offset=offset,
        )
        logger.info(f"✅ Query partidos executada - {len(results)} resultados, total={total}")

        return VotationPartyPaginatedResponse(
            total=total,
            limit=limit,
            offset=offset,
            data=[VotationPartyResponse.model_validate(r) for r in results],
        )
    except Exception as e:
        logger.error(f"❌ Erro no endpoint de partidos: {e}", exc_info=True)
        raise HTTPException(500, f"Erro ao buscar votação por partido: {str(e)}")


@router.get("/parties/{party_vote_id}", response_model=VotationPartyResponse)
async def get_details_party_vote(
        party_vote_id: UUID,
        db: AsyncSession = Depends(get_db_session),
):
    """Retorna detalhes de um registro específico de votação por partido (município/zona)."""
    try:
        logger.info(f"🔍 Buscando votação por partido ID: {party_vote_id}")

        result = await db.execute(
            select(VotacaoPartidoMunZona).where(VotacaoPartidoMunZona.id == party_vote_id)
        )
        party_vote = result.scalar_one_or_none()
        if not party_vote:
            logger.warning(f"Registro de votação por partido não encontrado: {party_vote_id}")
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                "Registro de votação por partido não encontrado",
            )

        return VotationPartyResponse.from_orm(party_vote)

    except Exception as e:
        logger.error(f"Erro ao buscar detalhes de votação por partido: {str(e)}")
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            f"Erro ao buscar detalhes de votação por partido: {str(e)}",
        )
