import uuid

from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class PerfilEleitorado(Base):
    """Perfil do eleitorado por município e zona eleitoral"""

    __tablename__ = "perfil_eleitorado"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    dt_geracao = Column(String(10), nullable=True)
    hh_geracao = Column(String(8), nullable=True)
    ano_eleicao = Column(Integer, nullable=True, unique=True)
    sg_uf = Column(String(2), nullable=True)
    cd_municipio = Column(Integer, nullable=True)
    nm_municipio = Column(String(30), nullable=True)
    nr_zona = Column(Integer, nullable=True)
    cd_genero = Column(Integer, nullable=True)
    ds_genero = Column(String(13), nullable=True)
    cd_estado_civil = Column(Integer, nullable=True)
    ds_estado_civil = Column(String(22), nullable=True)
    cd_faixa_etaria = Column(Integer, nullable=True)
    ds_faixa_etaria = Column(String(16), nullable=True)
    cd_grau_escolaridade = Column(Integer, nullable=True)
    ds_grau_escolaridade = Column(String(29), nullable=True)
    cd_raca_cor = Column(Integer, nullable=True)
    ds_raca_cor = Column(String(13), nullable=True)
    cd_identidade_genero = Column(Integer, nullable=True)
    ds_identidade_genero = Column(String(20), nullable=True)
    cd_quilombola = Column(Integer, nullable=True)
    ds_quilombola = Column(String(13), nullable=True)
    cd_interprete_libras = Column(Integer, nullable=True)
    ds_interprete_libras = Column(String(13), nullable=True)
    tp_obrigatoriedade_voto = Column(String(11), nullable=True)
    qt_eleitores_perfil = Column(Integer, nullable=True)
    qt_eleitores_biometria = Column(Integer, nullable=True)
    qt_eleitores_deficiencia = Column(Integer, nullable=True)
    qt_eleitores_inc_nm_social = Column(Integer, nullable=True)
