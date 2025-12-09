import uuid

from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class MotivoCassacao(Base):
    __tablename__ = "motivo_cassacao"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    dt_geracao = Column(String(10), nullable=True)
    hh_geracao = Column(String(8), nullable=True)
    ano_eleicao = Column(Integer, nullable=True)
    cd_tipo_eleicao = Column(Integer, nullable=True)
    nm_tipo_eleicao = Column(String(19), nullable=True)
    cd_eleicao = Column(Integer, nullable=True)
    ds_eleicao = Column(String(38), nullable=True)
    sg_uf = Column(String(2), nullable=True)
    sg_ue = Column(Integer, nullable=True)
    nm_ue = Column(String(31), nullable=True)
    sq_candidato = Column(Integer, nullable=True)
    tp_motivo = Column(String(1), nullable=True)
    ds_tp_motivo = Column(String(32), nullable=True)
    cd_motivo = Column(Integer, nullable=True)
    ds_motivo = Column(String(61), nullable=True)
