from datetime import datetime, date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, field_validator, FieldValidationInfo, ConfigDict


class ConsultaCandidatoResponse(BaseModel):
    """Schema de resposta para consulta de candidatos."""
    id: UUID

    dt_geracao: Optional[date] = None
    hh_geracao: Optional[str] = None
    ano_eleicao: Optional[int] = None
    cd_tipo_eleicao: Optional[int] = None
    nm_tipo_eleicao: Optional[str] = None
    nr_turno: Optional[int] = None
    cd_eleicao: Optional[int] = None
    ds_eleicao: Optional[str] = None
    dt_eleicao: Optional[date] = None
    tp_abrangencia: Optional[str] = None
    sg_uf: Optional[str] = None
    sg_ue: Optional[int] = None
    nm_ue: Optional[str] = None
    cd_cargo: Optional[int] = None
    ds_cargo: Optional[str] = None
    sq_candidato: Optional[int] = None
    nr_candidato: Optional[int] = None
    nm_candidato: Optional[str] = None
    nm_urna_candidato: Optional[str] = None
    nm_social_candidato: Optional[str] = None
    nr_cpf_candidato: Optional[int] = None
    ds_email: Optional[str] = None
    cd_situacao_candidatura: Optional[int] = None
    ds_situacao_candidatura: Optional[str] = None
    tp_agremiacao: Optional[str] = None
    nr_partido: Optional[int] = None
    sg_partido: Optional[str] = None
    nm_partido: Optional[str] = None
    nr_federacao: Optional[int] = None
    nm_federacao: Optional[str] = None
    sg_federacao: Optional[str] = None
    ds_composicao_federacao: Optional[str] = None
    sq_coligacao: Optional[int] = None
    nm_coligacao: Optional[str] = None
    ds_composicao_coligacao: Optional[str] = None
    sg_uf_nascimento: Optional[str] = None
    dt_nascimento: Optional[str] = None
    nr_titulo_eleitoral_candidato: Optional[int] = None
    cd_genero: Optional[int] = None
    ds_genero: Optional[str] = None
    cd_grau_instrucao: Optional[int] = None
    ds_grau_instrucao: Optional[str] = None
    cd_estado_civil: Optional[int] = None
    ds_estado_civil: Optional[str] = None
    cd_cor_raca: Optional[int] = None
    ds_cor_raca: Optional[str] = None
    cd_ocupacao: Optional[int] = None
    ds_ocupacao: Optional[str] = None
    cd_sit_tot_turno: Optional[int] = None
    ds_sit_tot_turno: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

    @field_validator("dt_eleicao", "dt_geracao", mode="before")
    @classmethod
    def parse_br_date(cls, v: str, info: FieldValidationInfo) -> date:
        if isinstance(v, date):
            return v
        return datetime.strptime(v, "%d/%m/%Y").date()
