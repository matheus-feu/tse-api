import uuid

from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class ConsultaVagas(Base):
    __tablename__ = "consulta_vagas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    dt_geracao = Column(String(10), nullable=True)
    hh_geracao = Column(String(8), nullable=True)
    ano_eleicao = Column(Integer, nullable=True, unique=True)
    cd_tipo_eleicao = Column(Integer, nullable=True)
    nm_tipo_eleicao = Column(String(19), nullable=True)
    cd_eleicao = Column(Integer, nullable=True)
    ds_eleicao = Column(String(36), nullable=True)
    dt_eleicao = Column(String(10), nullable=True)
    dt_posse = Column(String(10), nullable=True)
    sg_uf = Column(String(2), nullable=True)
    sg_ue = Column(Integer, nullable=True)
    nm_ue = Column(String(31), nullable=True)
    cd_cargo = Column(Integer, nullable=True)
    ds_cargo = Column(String(13), nullable=True)
    qt_vaga = Column(Integer, nullable=True)
