from typing import Optional, List

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field

from app.models.comparecimento_abstencao.perfil_comparecimento_abstencao import (
    PerfilComparecimentoAbstencao,
)


class PerfilComparecimentoFilter(Filter):
    """Filtros para perfil de comparecimento e abstenção."""

    ano_eleicao: Optional[int] = Field(None, description="Ano da eleição")
    sg_uf: Optional[str] = Field(None, description="Sigla do estado")
    cd_municipio: Optional[int] = Field(None, description="Código do município")
    nr_zona: Optional[int] = Field(None, description="Número da zona")

    ds_genero__ilike: Optional[str] = Field(None, description="Filtro por gênero (ILIKE)")
    ds_cor_raca__ilike: Optional[str] = Field(None, description="Filtro por cor/raça (ILIKE)")
    ds_faixa_etaria__ilike: Optional[str] = Field(None, description="Filtro por faixa etária (ILIKE)")
    ds_grau_escolaridade__ilike: Optional[str] = Field(
        None, description="Filtro por grau de escolaridade (ILIKE)"
    )

    qt_comparecimento__gte: Optional[int] = Field(
        None, description="Comparecimento >= valor"
    )
    qt_comparecimento__lte: Optional[int] = Field(
        None, description="Comparecimento <= valor"
    )

    order_by: Optional[List[str]] = Field(
        default=["-qt_comparecimento"],
        description="Ordenação (ex: 'sg_uf', '-qt_comparecimento')",
    )

    class Constants(Filter.Constants):
        model = PerfilComparecimentoAbstencao

        ordering_field_name = "order_by"
        ordering_fields = [
            "ano_eleicao",
            "sg_uf",
            "cd_municipio",
            "nr_zona",
            "ds_genero",
            "ds_cor_raca",
            "ds_faixa_etaria",
            "ds_grau_escolaridade",
            "qt_comparecimento",
            "qt_abstencao",
        ]
