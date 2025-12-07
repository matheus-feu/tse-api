from datetime import datetime, date
from uuid import UUID

from pydantic import BaseModel, field_validator, FieldValidationInfo, ConfigDict


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
