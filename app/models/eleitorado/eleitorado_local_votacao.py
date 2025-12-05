import uuid

from sqlalchemy import Column, Integer, Text, String
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class EleitoradoLocalVotacao(Base):
    """Eleitorado por Local de Votação"""

    __tablename__ = "eleitorado_local_votacao"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    dt_geracao = Column(String(10), nullable=True)
    hh_geracao = Column(String(8), nullable=True)
    aa_eleicao = Column(Integer, nullable=True)
    dt_eleicao = Column(String(10), nullable=True)
    ds_eleicao = Column(String(8), nullable=True)
    nr_turno = Column(Integer, nullable=True)
    sg_uf = Column(String(2), nullable=True)
    cd_municipio = Column(Integer, nullable=True)
    nm_municipio = Column(String(31), nullable=True)
    nr_zona = Column(Integer, nullable=True)
    nr_secao = Column(Integer, nullable=True)
    cd_tipo_secao_agregada = Column(Integer, nullable=True)
    ds_tipo_secao_agregada = Column(String(9), nullable=True)
    nr_secao_principal = Column(Integer, nullable=True)
    nr_local_votacao = Column(Integer, nullable=True)
    nm_local_votacao = Column(String(70), nullable=True)
    cd_tipo_local = Column(Integer, nullable=True)
    ds_tipo_local = Column(String(16), nullable=True)
    ds_endereco = Column(String(70), nullable=True)
    nm_bairro = Column(String(52), nullable=True)
    nr_cep = Column(Integer, nullable=True)
    nr_telefone_local = Column(String(14), nullable=True)
    nr_latitude = Column(Text, nullable=True)
    nr_longitude = Column(Text, nullable=True)
    cd_situ_local_votacao = Column(Integer, nullable=True)
    ds_situ_local_votacao = Column(String(9), nullable=True)
    cd_situ_zona = Column(Integer, nullable=True)
    ds_situ_zona = Column(String(5), nullable=True)
    cd_situ_secao = Column(Integer, nullable=True)
    ds_situ_secao = Column(String(5), nullable=True)
    cd_situ_localidade = Column(Integer, nullable=True)
    ds_situ_localidade = Column(String(5), nullable=True)
    cd_situ_secao_acessibilidade = Column(Integer, nullable=True)
    ds_situ_secao_acessibilidade = Column(String(18), nullable=True)
    qt_eleitor_secao = Column(Integer, nullable=True)
    qt_eleitor_eleicao_federal = Column(Integer, nullable=True)
    qt_eleitor_eleicao_estadual = Column(Integer, nullable=True)
    qt_eleitor_eleicao_municipal = Column(Integer, nullable=True)
    nr_local_votacao_original = Column(Integer, nullable=True)
    nm_local_votacao_original = Column(String(70), nullable=True)
    ds_endereco_locvt_original = Column(String(70), nullable=True)
