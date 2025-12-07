from typing import Optional, List

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field

from app.models.resultados.votacao_candidato_munzona import VotacaoCandidatoMunZona


class VotacaoCandidatoFilter(Filter):
    """Filtros para consulta de votação por candidato."""

    ano_eleicao: Optional[int] = Field(None, description="Ano da eleição")
    sg_uf: Optional[str] = Field(None, description="Sigla do estado")
    nr_candidato: Optional[int] = Field(None, description="Número do candidato")
    sg_partido: Optional[str] = Field(None, description="Sigla do partido")

    nm_candidato__ilike: Optional[str] = Field(None, description="Busca no nome do candidato")
    ds_cargo__ilike: Optional[str] = Field(None, description="Busca no cargo")

    qt_votos_nominais__gte: Optional[int] = Field(None, description="Votos >= valor")
    qt_votos_nominais__lte: Optional[int] = Field(None, description="Votos <= valor")

    order_by: Optional[List[str]] = Field(
        default=["-qt_votos_nominais"],
        description="Ordenação (ex: 'nm_candidato', '-qt_votos_nominais')"
    )

    search: Optional[str] = Field(
        None,
        description="Busca geral em nome do candidato"
    )

    class Constants(Filter.Constants):
        model = VotacaoCandidatoMunZona

        ordering_field_name = "order_by"
        ordering_fields = [
            "nm_candidato",
            "sg_partido",
            "qt_votos_nominais",
            "ds_cargo"
        ]
        search_field_name = "search"
        search_model_fields = ["nm_candidato"]
