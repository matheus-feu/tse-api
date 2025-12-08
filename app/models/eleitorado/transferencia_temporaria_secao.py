import uuid

from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class TransferenciaTemporariaSecao(Base):
    """Transferência Temporária de Eleitores por Seção"""

    __tablename__ = "transferencia_temporaria_secao"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    dt_geracao = Column(String(10), nullable=True)
    hh_geracao = Column(String(8), nullable=True)
    aa_eleicao = Column(Integer, nullable=True, unique=True)
    nr_turno = Column(Integer, nullable=True)
    tp_tte = Column(String(23), nullable=True)
    tp_abrangencia_tte = Column(String(9), nullable=True)
    sg_uf_origem = Column(String(2), nullable=True)
    cd_municipio_origem = Column(Integer, nullable=True)
    nm_municipio_origem = Column(String(32), nullable=True)
    nr_zona_origem = Column(Integer, nullable=True)
    nr_secao_origem = Column(Integer, nullable=True)
    sg_uf_destino = Column(String(2), nullable=True)
    cd_municipio_destino = Column(Integer, nullable=True)
    nm_municipio_destino = Column(String(32), nullable=True)
    nr_zona_destino = Column(Integer, nullable=True)
    nr_secao_destino = Column(Integer, nullable=True)
    qt_eleitor = Column(Integer, nullable=True)
