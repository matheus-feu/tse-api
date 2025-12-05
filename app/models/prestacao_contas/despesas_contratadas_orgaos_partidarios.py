import uuid

from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class DespesasContratadasOrgaosPartidarios(Base):
    """Prestação de contas de órgãos partidários"""

    __tablename__ = "despesas_contratadas_orgaos_partidarios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    dt_geracao = Column(String(10), nullable=True)
    hh_geracao = Column(String(8), nullable=True)
    aa_eleicao = Column(Integer, nullable=True)
    cd_tipo_eleicao = Column(Integer, nullable=True)
    nm_tipo_eleicao = Column(String(9), nullable=True)
    tp_prestacao_contas = Column(String(24), nullable=True)
    dt_prestacao_contas = Column(String(10), nullable=True)
    sq_prestador_contas = Column(Integer, nullable=True)
    cd_esfera_partidaria = Column(String(1), nullable=True)
    ds_esfera_partidaria = Column(String(28), nullable=True)
    sg_uf = Column(String(2), nullable=True)
    sg_ue = Column(String(5), nullable=True)
    nm_ue = Column(String(30), nullable=True)
    cd_municipio = Column(Integer, nullable=True)
    nm_municipio = Column(String(30), nullable=True)
    nr_cnpj_prestador_conta = Column(Integer, nullable=True)
    nr_partido = Column(Integer, nullable=True)
    sg_partido = Column(String(13), nullable=True)
    nm_partido = Column(String(46), nullable=True)
    cd_tipo_fornecedor = Column(Integer, nullable=True)
    ds_tipo_fornecedor = Column(String(15), nullable=True)
    cd_cnae_fornecedor = Column(Integer, nullable=True)
    ds_cnae_fornecedor = Column(String(36), nullable=True)
    nr_cpf_cnpj_fornecedor = Column(Integer, nullable=True)
    nm_fornecedor = Column(String(72), nullable=True)
    nm_fornecedor_rfb = Column(String(70), nullable=True)
    cd_esfera_part_fornecedor = Column(String(1), nullable=True)
    ds_esfera_part_fornecedor = Column(String(28), nullable=True)
    sg_uf_fornecedor = Column(String(6), nullable=True)
    cd_municipio_fornecedor = Column(Integer, nullable=True)
    nm_municipio_fornecedor = Column(String(32), nullable=True)
    sq_candidato_fornecedor = Column(Integer, nullable=True)
    nr_candidato_fornecedor = Column(Integer, nullable=True)
    cd_cargo_fornecedor = Column(Integer, nullable=True)
    ds_cargo_fornecedor = Column(String(13), nullable=True)
    nr_partido_fornecedor = Column(Integer, nullable=True)
    sg_partido_fornecedor = Column(String(13), nullable=True)
    nm_partido_fornecedor = Column(String(40), nullable=True)
    ds_tipo_documento = Column(String(5), nullable=True)
    nr_documento = Column(String(6), nullable=True)
    cd_origem_despesa = Column(Integer, nullable=True)
    ds_origem_despesa = Column(String(64), nullable=True)
    sq_despesa = Column(Integer, nullable=True)
    dt_despesa = Column(String(10), nullable=True)
    ds_despesa = Column(String(61), nullable=True)
    vr_despesa_contratada = Column(String(10), nullable=True)
