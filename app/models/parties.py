import uuid

from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class VotoPartidoMunZona(Base):
    """Modelo de banco de dados para votos de partidos por município e zona eleitoral."""

    __tablename__ = "votacao_partido_munzona"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    nr_turno = Column(Integer, nullable=False)
    ano_eleicao = Column(Integer, nullable=False)
    cd_eleicao = Column(Integer, nullable=False)
    ds_eleicao = Column(String(100), nullable=False)
    dt_eleicao = Column(Date, nullable=False)
    sg_uf = Column(String(2), nullable=False)
    sg_ue = Column(String(10), nullable=False)
    nm_ue = Column(String(100), nullable=False)
    cd_municipio = Column(Integer, nullable=False)
    nm_municipio = Column(String(100), nullable=False)
    nr_zona = Column(Integer, nullable=False)
    cd_cargo = Column(Integer, nullable=False)
    ds_cargo = Column(String(50), nullable=False)
    nr_partido = Column(Integer, nullable=False)
    sg_partido = Column(String(10), nullable=False)
    nm_partido = Column(String(100), nullable=False)
    qt_votos_nominais = Column(Integer, nullable=False)
    qt_votos_nominais_validos = Column(Integer, nullable=False)
    qt_votos_nominais_anulados = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<VotoPartidoMunZona(nr_partido={self.nr_partido}, cd_municipio={self.cd_municipio}, nr_zona={self.nr_zona}, qt_votos_nominais={self.qt_votos_nominais})>"
