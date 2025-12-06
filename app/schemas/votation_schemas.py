from datetime import datetime, date
from typing import List
from uuid import UUID

from pydantic import BaseModel, field_validator, FieldValidationInfo, ConfigDict


class VotationCandidateResponse(BaseModel):
    """Resposta com dados de votação por candidato."""
    id: UUID
    ano_eleicao: int
    nr_turno: int
    dt_eleicao: date
    sg_uf: str
    cd_municipio: int
    nm_municipio: str
    nr_zona: int
    nr_candidato: int
    nm_candidato: str
    nr_partido: int
    sg_partido: str
    nm_partido: str
    ds_cargo: str
    qt_votos_nominais: int
    qt_votos_nominais_validos: int

    model_config = ConfigDict(from_attributes=True)

    @field_validator("dt_eleicao", mode="before")
    @classmethod
    def parse_br_date(cls, v: str, info: FieldValidationInfo) -> date:
        if isinstance(v, date):
            return v
        return datetime.strptime(v, "%d/%m/%Y").date()


class VotationPaginatedResponse(BaseModel):
    """Resposta paginada de votação."""
    total: int
    limit: int
    offset: int
    data: List[VotationCandidateResponse]


class VotationPartyResponse(BaseModel):
    """Resposta com dados de votação por partido."""
    id: UUID
    ano_eleicao: int
    nr_turno: int
    cd_eleicao: int
    ds_eleicao: str
    dt_eleicao: date
    sg_uf: str
    cd_municipio: int
    nm_municipio: str
    nr_zona: int
    cd_cargo: int
    ds_cargo: str
    nr_partido: int
    sg_partido: str
    nm_partido: str
    qt_votos_legenda_validos: int
    qt_votos_nom_convr_leg_validos: int
    qt_total_votos_leg_validos: int
    qt_votos_nominais_validos: int
    qt_votos_legenda_anul_subjud: int
    qt_votos_nominais_anul_subjud: int
    qt_votos_legenda_anulados: int
    qt_votos_nominais_anulados: int

    model_config = ConfigDict(from_attributes=True)


class VotationPartyPaginatedResponse(BaseModel):
    """Resposta paginada de votação por partido."""
    total: int
    limit: int
    offset: int
    data: List[VotationPartyResponse]
