from typing import Optional, List

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field

from app.models.resultados.votacao_partido_munzona import VotacaoPartidoMunZona


class VotacaoPartidoFilter(Filter):
    """Filtros para consulta de votação por partido."""

    ano_eleicao: Optional[int] = Field(None, description="Ano da eleição")
    sg_uf: Optional[str] = Field(None, description="Sigla do estado")
    sg_partido: Optional[str] = Field(None, description="Sigla do partido")

    ds_cargo__ilike: Optional[str] = Field(None, description="Busca no cargo")

    qt_votos_nominais_validos__gte: Optional[int] = Field(None, description="Votos >= valor")
    qt_votos_nominais_validos__lte: Optional[int] = Field(None, description="Votos <= valor")

    order_by: Optional[List[str]] = Field(
        default=["-qt_votos_nominais_validos"],
        description="Ordenação (ex: 'sg_partido', '-qt_votos_nominais_validos')",
    )

    search: Optional[str] = Field(
        None,
        description="Busca geral em sigla do partido"
    )

    class Constants(Filter.Constants):
        model = VotacaoPartidoMunZona

        ordering_field_name = "order_by"
        ordering_fields = [
            "sg_partido",
            "qt_votos_nominais_validos",
            "ds_cargo"
        ]
        search_field_name = "search"
        search_model_fields = ["sg_partido"]
