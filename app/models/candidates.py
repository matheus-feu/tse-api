import uuid

from sqlalchemy import Column, String, Integer, Date, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class VotoCandidatoMunZona(Base):
    """Modelo de banco de dados para votos de candidatos por município e zona eleitoral."""

    __tablename__ = "votacao_candidato_munzona"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    ano_eleicao = Column(Integer, nullable=False)
    nr_turno = Column(Integer, nullable=False)
    cd_eleicao = Column(Integer, nullable=False)
    dt_eleicao = Column(Date, nullable=False)
    sg_uf = Column(String(2), nullable=False)
    sg_ue = Column(String(20), nullable=False)
    nm_ue = Column(String(150), nullable=False)
    cd_municipio = Column(Integer, nullable=False)
    nm_municipio = Column(String(150), nullable=False)
    nr_zona = Column(Integer, nullable=False)
    ds_cargo = Column(String(100), nullable=False)
    nr_candidato = Column(Integer, nullable=False)
    nm_candidato = Column(String(150), nullable=False)
    nr_partido = Column(Integer, nullable=False)
    sg_partido = Column(String(20), nullable=False)
    nm_partido = Column(String(150), nullable=False)

    qt_votos_nominais = Column(Integer, nullable=False)
    qt_votos_nominais_validos = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            'ano_eleicao', 'nr_turno', 'sg_uf',
            'cd_municipio', 'nr_zona', 'nr_candidato',
            name='uq_votacao_candidato'
        ),
    )

    def __repr__(self):
        return (f"<VotoCandidatoMunZona("
                f"nr_candidato={self.nr_candidato}, "
                f"cd_municipio={self.cd_municipio}, "
                f"nr_zona={self.nr_zona}, "
                f"qt_votos_nominais={self.qt_votos_nominais})>")
