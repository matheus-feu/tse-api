import uuid

from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class BemCandidato(Base):
    __tablename__ = "bem_cand"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    dt_geracao = Column(String(10), nullable=True)
    hh_geracao = Column(String(8), nullable=True)
    ano_eleicao = Column(Integer, nullable=True, unique=True)
    cd_tipo_eleicao = Column(Integer, nullable=True)
    nm_tipo_eleicao = Column(String(17), nullable=True)
    cd_eleicao = Column(Integer, nullable=True)
    ds_eleicao = Column(String(24), nullable=True)
    dt_eleicao = Column(String(10), nullable=True)
    sg_uf = Column(String(2), nullable=True)
    sg_ue = Column(Integer, nullable=True)
    nm_ue = Column(String(32), nullable=True)
    sq_candidato = Column(Integer, nullable=True)
    nr_ordem_bem_candidato = Column(Integer, nullable=True)
    cd_tipo_bem_candidato = Column(Integer, nullable=True)
    ds_tipo_bem_candidato = Column(String(112), nullable=True)
    ds_bem_candidato = Column(String(199), nullable=True)
    vr_bem_candidato = Column(String(10), nullable=True)
    dt_ult_atual_bem_candidato = Column(String(10), nullable=True)
    hh_ult_atual_bem_candidato = Column(String(8), nullable=True)
