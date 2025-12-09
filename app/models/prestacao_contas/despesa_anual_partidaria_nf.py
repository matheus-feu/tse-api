import uuid

from sqlalchemy import Column, Integer, Numeric, Text, DateTime, Boolean, String
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base


class DespesaAnualPartidariaNf(Base):
    """Prestação de contas anual partidária - notas fiscais"""

    __tablename__ = "despesa_anual_partidaria_nf"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    dt_geracao = Column(String(10), nullable=True)
    hh_geracao = Column(String(8), nullable=True)
    aa_exercicio = Column(Integer, nullable=True)
    tp_despesa = Column(String(1), nullable=True)
    sg_uf = Column(String(2), nullable=True)
    sq_despesa = Column(Text, nullable=True)
    nr_cnpj_prestador_conta = Column(Integer, nullable=True)
    sg_partido = Column(String(12), nullable=True)
    nr_documento = Column(String(20), nullable=True)
    nr_cpf_cnpj_fornecedor = Column(Integer, nullable=True)
    ds_gasto = Column(String(169), nullable=True)
    dt_pagamento = Column(DateTime(timezone=True), nullable=True)
    vr_documento = Column(Text, nullable=True)
    nm_url = Column(String(217), nullable=True)