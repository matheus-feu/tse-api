import uuid

from sqlalchemy import Column, Integer, Numeric, Text, DateTime, Boolean, String
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base


class DespesasPagasCandidatos(Base):
    __tablename__ = "despesas_pagas_candidatos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    dt_geracao = Column(String(10), nullable=True)
    hh_geracao = Column(String(8), nullable=True)
    aa_eleicao = Column(Integer, nullable=True)
    cd_tipo_eleicao = Column(Integer, nullable=True)
    nm_tipo_eleicao = Column(String(11), nullable=True)
    cd_eleicao = Column(Integer, nullable=True)
    ds_eleicao = Column(String(38), nullable=True)
    dt_eleicao = Column(String(10), nullable=True)
    st_turno = Column(Integer, nullable=True)
    tp_prestacao_contas = Column(String(24), nullable=True)
    dt_prestacao_contas = Column(String(10), nullable=True)
    sq_prestador_contas = Column(Integer, nullable=True)
    sg_uf = Column(String(2), nullable=True)
    ds_tipo_documento = Column(String(12), nullable=True)
    nr_documento = Column(String(23), nullable=True)
    cd_fonte_despesa = Column(Integer, nullable=True)
    ds_fonte_despesa = Column(String(43), nullable=True)
    cd_origem_despesa = Column(Integer, nullable=True)
    ds_origem_despesa = Column(String(64), nullable=True)
    cd_natureza_despesa = Column(Integer, nullable=True)
    ds_natureza_despesa = Column(String(10), nullable=True)
    cd_especie_recurso = Column(Integer, nullable=True)
    ds_especie_recurso = Column(String(24), nullable=True)
    sq_despesa = Column(Integer, nullable=True)
    sq_parcelamento_despesa = Column(Integer, nullable=True)
    dt_pagto_despesa = Column(String(10), nullable=True)
    ds_despesa = Column(String(253), nullable=True)
    vr_pagto_despesa = Column(String(9), nullable=True)