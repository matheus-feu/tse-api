import uuid

from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class RedeSocialCandidato(Base):
    __tablename__ = "rede_social_cand"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    dt_geracao = Column(String(10), nullable=True)
    hh_geracao = Column(String(8), nullable=True)
    aa_eleicao = Column(Integer, nullable=True)
    sg_uf = Column(String(2), nullable=True)
    cd_tipo_eleicao = Column(Integer, nullable=True)
    nm_tipo_eleicao = Column(String(19), nullable=True)
    cd_eleicao = Column(Integer, nullable=True)
    ds_eleicao = Column(String(33), nullable=True)
    sq_candidato = Column(Integer, nullable=True)
    nr_ordem_rede_social = Column(Integer, nullable=True)
    ds_url = Column(String(135), nullable=True)
