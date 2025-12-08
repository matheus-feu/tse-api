import uuid

from sqlalchemy import Column, Integer, Numeric, Text, DateTime, Boolean, String
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base


class DespesaAnual(Base):
    """Prestação de contas anual partidária"""

    __tablename__ = "despesa_anual"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    dt_geracao = Column(String(10), nullable=True)
    hh_geracao = Column(String(8), nullable=True)
    aa_exercicio = Column(Integer, nullable=True, unique=True)
    tp_despesa = Column(String(6), nullable=True)
    cd_tp_esfera_partidaria = Column(Integer, nullable=True)
    ds_tp_esfera_partidaria = Column(String(9), nullable=True)
    sg_uf = Column(String(2), nullable=True)
    cd_municipio = Column(Integer, nullable=True)
    nm_municipio = Column(String(28), nullable=True)
    nr_zona = Column(Integer, nullable=True)
    nr_cnpj_prestador_conta = Column(Integer, nullable=True)
    sg_partido = Column(String(12), nullable=True)
    nm_partido = Column(String(46), nullable=True)
    cd_tp_documento = Column(String(6), nullable=True)
    ds_tp_documento = Column(String(6), nullable=True)
    nr_documento = Column(String(6), nullable=True)
    aa_aidf = Column(Integer, nullable=True)
    nr_aidf = Column(Integer, nullable=True)
    cd_tp_fornecedor = Column(String(6), nullable=True)
    ds_tp_fornecedor = Column(String(6), nullable=True)
    nr_cpf_cnpj_fornecedor = Column(String(6), nullable=True)
    nm_fornecedor = Column(String(6), nullable=True)
    ds_gasto = Column(String(6), nullable=True)
    dt_pagamento = Column(Text, nullable=True)
    vr_gasto = Column(Integer, nullable=True)
    vr_pagamento = Column(Integer, nullable=True)
    vr_documento = Column(Integer, nullable=True)
    cd_fonte_despesa = Column(Integer, nullable=True)
    ds_fonte_despesa = Column(String(6), nullable=True)
    sq_despesa = Column(Integer, nullable=True)