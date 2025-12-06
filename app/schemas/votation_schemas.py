from datetime import datetime, date
from typing import List
from uuid import UUID

from pydantic import BaseModel, field_validator, FieldValidationInfo, ConfigDict


class VotacaoCandidatoMunZonaResponse(BaseModel):
    """Resposta com dados de votação por candidato."""
    id: UUID

    dt_geracao: date | None
    hh_geracao: str | None
    cd_tipo_eleicao: int | None
    nm_tipo_eleicao: str | None
    nr_turno: int | None
    cd_eleicao: int | None
    ds_eleicao: str | None
    dt_eleicao: date | None
    tp_abrangencia: str | None
    sg_uf: str | None
    sg_ue: int | None
    nm_ue: str | None
    cd_municipio: int | None
    nm_municipio: str | None
    nr_zona: int | None
    cd_cargo: int | None
    ds_cargo: str | None
    sq_candidato: int | None
    nr_candidato: int | None
    nm_candidato: str | None
    nm_urna_candidato: str | None
    nm_social_candidato: str | None
    cd_situacao_candidatura: int | None
    ds_situacao_candidatura: str | None
    cd_detalhe_situacao_cand: int | None
    ds_detalhe_situacao_cand: str | None
    cd_situacao_julgamento: int | None
    ds_situacao_julgamento: str | None
    cd_situacao_cassacao: int | None
    ds_situacao_cassacao: str | None
    cd_situacao_dconst_diploma: int | None
    ds_situacao_dconst_diploma: str | None
    tp_agremiacao: str | None
    nr_partido: int | None
    sg_partido: str | None
    nm_partido: str | None
    nr_federacao: int | None
    nm_federacao: str | None
    sg_federacao: str | None
    ds_composicao_federacao: str | None
    sq_coligacao: int | None
    nm_coligacao: str | None
    ds_composicao_coligacao: str | None
    st_voto_em_transito: str | None
    qt_votos_nominais_validos: int | None
    nm_tipo_destinacao_votos: str | None
    qt_votos_nominais: int | None
    cd_sit_tot_turno: int | None
    ds_sit_tot_turno: str | None

    model_config = ConfigDict(from_attributes=True)

    @field_validator("dt_eleicao", "dt_geracao", mode="before")
    @classmethod
    def parse_br_date(cls, v: str, info: FieldValidationInfo) -> date:
        if isinstance(v, date):
            return v
        return datetime.strptime(v, "%d/%m/%Y").date()


class VotacaoCandidatoMunZonaPaginatedResponse(BaseModel):
    """Resposta paginada de votação."""
    total: int
    limit: int
    offset: int
    data: List[VotacaoCandidatoMunZonaResponse]


class VotacaoPartidoMunZonaResponse(BaseModel):
    """Resposta com dados de votacao_partido_munzona."""
    id: UUID

    dt_geracao: date | None
    hh_geracao: str | None
    ano_eleicao: int | None
    cd_tipo_eleicao: int | None
    nm_tipo_eleicao: str | None
    nr_turno: int | None
    cd_eleicao: int | None
    ds_eleicao: str | None
    dt_eleicao: date | None
    tp_abrangencia: str | None
    sg_uf: str | None
    sg_ue: int | None
    nm_ue: str | None
    cd_municipio: int | None
    nm_municipio: str | None
    nr_zona: int | None
    cd_cargo: int | None
    ds_cargo: str | None
    tp_agremiacao: str | None
    nr_partido: int | None
    sg_partido: str | None
    nm_partido: str | None
    nr_federacao: int | None
    nm_federacao: str | None
    sg_federacao: str | None
    ds_composicao_federacao: str | None
    sq_coligacao: int | None
    nm_coligacao: str | None
    ds_composicao_coligacao: str | None
    st_voto_em_transito: str | None
    qt_votos_legenda_validos: int | None
    qt_votos_nom_convr_leg_validos: int | None
    qt_total_votos_leg_validos: int | None
    qt_votos_nominais_validos: int | None
    qt_votos_legenda_anul_subjud: int | None
    qt_votos_nominais_anul_subjud: int | None
    qt_votos_legenda_anulados: int | None
    qt_votos_nominais_anulados: int | None

    model_config = ConfigDict(from_attributes=True)

    @field_validator("dt_geracao", "dt_eleicao", mode="before")
    @classmethod
    def parse_br_date(cls, v: str | None, info: FieldValidationInfo) -> date | None:
        if v is None:
            return None
        if isinstance(v, date):
            return v
        # CSV vem como "DD/MM/AAAA"
        return datetime.strptime(v, "%d/%m/%Y").date()


class VotacaoPartidoMunZonaPaginatedResponse(BaseModel):
    total: int
    limit: int
    offset: int
    data: List[VotacaoPartidoMunZonaResponse]
