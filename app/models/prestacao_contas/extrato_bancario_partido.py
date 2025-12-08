import uuid

from sqlalchemy import Column, Integer, Numeric, Text, DateTime, Boolean, String
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base


class ExtratoBancarioPartido(Base):
    __tablename__ = "extrato_bancario_partido"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    dt_geracao = Column(String(10), nullable=True)
    hh_geracao = Column(String(8), nullable=True)
    aa_referencia = Column(Integer, nullable=True, unique=True)
    sg_partido = Column(String(12), nullable=True)
    nm_esfera = Column(String(9), nullable=True)
    nr_cnpj = Column(Integer, nullable=True)
    cd_banco = Column(Integer, nullable=True)
    nm_banco = Column(String(36), nullable=True)
    nr_agencia = Column(Integer, nullable=True)
    nr_conta = Column(Integer, nullable=True)
    tp_conta = Column(Integer, nullable=True)
    nr_documento = Column(String(20), nullable=True)
    dt_lancamento = Column(String(10), nullable=True)
    tp_lancamento = Column(String(1), nullable=True)
    ds_lancamento = Column(String(39), nullable=True)
    vr_lancamento = Column(String(11), nullable=True)
    cd_tipo_operacao = Column(Integer, nullable=True)
    ds_tipo_operacao = Column(String(38), nullable=True)
    cd_fonte_recurso = Column(String(6), nullable=True)
    ds_fonte_recurso = Column(String(43), nullable=True)
    ds_detalhe_fonte_recurso = Column(String(12), nullable=True)
    nr_cpf_cnpj_contraparte = Column(Integer, nullable=True)
    tp_pessoa_contraparte = Column(Integer, nullable=True)
    nm_contraparte = Column(String(57), nullable=True)
    cd_banco_contraparte = Column(Integer, nullable=True)
    nm_banco_contraparte = Column(String(56), nullable=True)
    nr_agencia_contraparte = Column(Integer, nullable=True)
    nr_conta_contraparte = Column(String(20), nullable=True)