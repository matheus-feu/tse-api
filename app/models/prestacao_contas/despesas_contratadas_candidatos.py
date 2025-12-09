import uuid

from sqlalchemy import Column, Integer, Numeric, Text, DateTime, Boolean, String
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base


class DespesasContratadasCandidatos(Base):
    """Prestação de contas de candidatos"""

    __tablename__ = "despesas_contratadas_candidatos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    dt_geracao = Column(String(10), nullable=True)
    hh_geracao = Column(String(8), nullable=True)
    aa_eleicao = Column(Integer, nullable=True)
    cd_tipo_eleicao = Column(Integer, nullable=True)
    nm_tipo_eleicao = Column(String(11), nullable=True)
    cd_eleicao = Column(Integer, nullable=True)
    ds_eleicao = Column(String(37), nullable=True)
    dt_eleicao = Column(String(10), nullable=True)
    st_turno = Column(Integer, nullable=True)
    tp_prestacao_contas = Column(String(24), nullable=True)
    dt_prestacao_contas = Column(String(10), nullable=True)
    sq_prestador_contas = Column(Integer, nullable=True)
    sg_uf = Column(String(2), nullable=True)
    sg_ue = Column(Integer, nullable=True)
    nm_ue = Column(String(32), nullable=True)
    nr_cnpj_prestador_conta = Column(Integer, nullable=True)
    cd_cargo = Column(Integer, nullable=True)
    ds_cargo = Column(String(8), nullable=True)
    sq_candidato = Column(Integer, nullable=True)
    nr_candidato = Column(Integer, nullable=True)
    nm_candidato = Column(String(48), nullable=True)
    nr_cpf_candidato = Column(Integer, nullable=True)
    nr_cpf_vice_candidato = Column(Integer, nullable=True)
    nr_partido = Column(Integer, nullable=True)
    sg_partido = Column(String(13), nullable=True)
    nm_partido = Column(String(46), nullable=True)
    cd_tipo_fornecedor = Column(Integer, nullable=True)
    ds_tipo_fornecedor = Column(String(15), nullable=True)
    cd_cnae_fornecedor = Column(Integer, nullable=True)
    ds_cnae_fornecedor = Column(String(144), nullable=True)
    nr_cpf_cnpj_fornecedor = Column(Integer, nullable=True)
    nm_fornecedor = Column(String(100), nullable=True)
    nm_fornecedor_rfb = Column(String(81), nullable=True)
    cd_esfera_part_fornecedor = Column(Integer, nullable=True)
    ds_esfera_part_fornecedor = Column(String(5), nullable=True)
    sg_uf_fornecedor = Column(String(6), nullable=True)
    cd_municipio_fornecedor = Column(Integer, nullable=True)
    nm_municipio_fornecedor = Column(String(15), nullable=True)
    sq_candidato_fornecedor = Column(Integer, nullable=True)
    nr_candidato_fornecedor = Column(Integer, nullable=True)
    cd_cargo_fornecedor = Column(Integer, nullable=True)
    ds_cargo_fornecedor = Column(String(8), nullable=True)
    nr_partido_fornecedor = Column(Integer, nullable=True)
    sg_partido_fornecedor = Column(String(5), nullable=True)
    nm_partido_fornecedor = Column(String(26), nullable=True)
    ds_tipo_documento = Column(String(12), nullable=True)
    nr_documento = Column(String(23), nullable=True)
    cd_origem_despesa = Column(Integer, nullable=True)
    ds_origem_despesa = Column(String(50), nullable=True)
    sq_despesa = Column(Integer, nullable=True)
    dt_despesa = Column(String(10), nullable=True)
    ds_despesa = Column(String(50), nullable=True)
    vr_despesa_contratada = Column(String(9), nullable=True)