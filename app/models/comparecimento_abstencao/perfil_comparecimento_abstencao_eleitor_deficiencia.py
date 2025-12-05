import uuid

from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class PerfilComparecimentoAbstencaoEleitorDeficiencia(Base):
    """Pessoas com deficiência"""

    __tablename__ = "perfil_comparecimento_abstencao_eleitor_deficiencia"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    dt_geracao = Column(String(10), nullable=True)
    hh_geracao = Column(String(8), nullable=True)
    ano_eleicao = Column(Integer, nullable=True)
    nr_turno = Column(Integer, nullable=True)
    sq_eleitor = Column(Integer, nullable=True)
    sg_uf = Column(String(2), nullable=True)
    cd_municipio = Column(Integer, nullable=True)
    nm_municipio = Column(String(26), nullable=True)
    nr_zona = Column(Integer, nullable=True)
    cd_genero = Column(Integer, nullable=True)
    ds_genero = Column(String(13), nullable=True)
    cd_estado_civil = Column(Integer, nullable=True)
    ds_estado_civil = Column(String(22), nullable=True)
    cd_faixa_etaria = Column(Integer, nullable=True)
    ds_faixa_etaria = Column(String(16), nullable=True)
    cd_grau_escolaridade = Column(Integer, nullable=True)
    ds_grau_escolaridade = Column(String(29), nullable=True)
    cd_tipo_deficiencia = Column(Integer, nullable=True)
    ds_tipo_deficiencia = Column(String(36), nullable=True)
    st_comparecimento = Column(String(1), nullable=True)
