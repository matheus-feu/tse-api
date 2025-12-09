from typing import Optional, List

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field

from app.models.candidatos.consulta_candidato import ConsultaCandidatos


class ConsultaCandidatoFilter(Filter):
    """Filtros para consulta de candidatos."""

    ano_eleicao: Optional[int] = Field(None, description="Ano da eleição")
    sg_uf: Optional[str] = Field(None, description="Sigla do estado")
    cd_cargo: Optional[int] = Field(None, description="Código do cargo")
    nr_candidato: Optional[int] = Field(None, description="Número do candidato")
    sg_partido: Optional[str] = Field(None, description="Sigla do partido")
    cd_genero: Optional[int] = Field(None, description="Código de gênero")
    cd_grau_instrucao: Optional[int] = Field(None, description="Código grau de instrução")
    cd_cor_raca: Optional[int] = Field(None, description="Código cor/raça")
    cd_ocupacao: Optional[int] = Field(None, description="Código ocupação")

    nm_candidato__ilike: Optional[str] = Field(
        None, description="Nome do candidato (busca parcial, ILIKE)"
    )
    nm_urna_candidato__ilike: Optional[str] = Field(
        None, description="Nome de urna (busca parcial, ILIKE)"
    )
    nm_partido__ilike: Optional[str] = Field(
        None, description="Nome do partido (busca parcial, ILIKE)"
    )
    ds_cargo__ilike: Optional[str] = Field(
        None, description="Descrição do cargo (busca parcial, ILIKE)"
    )

    order_by: Optional[List[str]] = Field(
        default=["nm_candidato"],
        description="Ordenação (ex: 'nm_candidato', '-nr_candidato')",
    )

    search: Optional[str] = Field(
        None,
        description="Busca geral em nome do candidato e partido",
    )

    class Constants(Filter.Constants):
        model = ConsultaCandidatos

        ordering_field_name = "order_by"
        ordering_fields = [
            "ano_eleicao",
            "sg_uf",
            "cd_cargo",
            "nr_candidato",
            "sg_partido",
            "nm_candidato",
            "nm_urna_candidato",
        ]

        search_field_name = "search"
        search_model_fields = [
            "nm_candidato",
            "nm_urna_candidato",
            "nm_partido",
        ]
