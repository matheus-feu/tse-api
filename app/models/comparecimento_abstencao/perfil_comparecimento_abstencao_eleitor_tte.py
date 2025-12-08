import uuid

from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class PerfilComparecimentoAbstencaoEleitorTte(Base):
    """Transferência temporária de eleitor"""

    __tablename__ = "perfil_comparecimento_abstencao_eleitor_tte"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    dt_geracao = Column(String(10), nullable=True)
    hh_geracao = Column(String(8), nullable=True)
    ano_eleicao = Column(Integer, nullable=True, unique=True)
    nr_turno = Column(Integer, nullable=True)
    sg_uf_origem = Column(String(2), nullable=True)
    cd_municipio_origem = Column(Integer, nullable=True)
    nm_municipio_origem = Column(String(32), nullable=True)
    nr_zona_origem = Column(Integer, nullable=True)
    sg_uf_destino = Column(String(2), nullable=True)
    cd_municipio_destino = Column(Integer, nullable=True)
    nm_municipio_destino = Column(String(32), nullable=True)
    nr_zona_destino = Column(Integer, nullable=True)
    cd_genero = Column(Integer, nullable=True)
    ds_genero = Column(String(9), nullable=True)
    cd_estado_civil = Column(Integer, nullable=True)
    ds_estado_civil = Column(String(22), nullable=True)
    cd_faixa_etaria = Column(Integer, nullable=True)
    ds_faixa_etaria = Column(String(12), nullable=True)
    cd_grau_escolaridade = Column(Integer, nullable=True)
    ds_grau_escolaridade = Column(String(29), nullable=True)
    cd_tipo_transferencia = Column(Integer, nullable=True)
    ds_tipo_transferencia = Column(String(19), nullable=True)
    qt_aptos_em_tte = Column(Integer, nullable=True)
    qt_comparecimento_tte = Column(Integer, nullable=True)
    qt_abstencao_tte = Column(Integer, nullable=True)
