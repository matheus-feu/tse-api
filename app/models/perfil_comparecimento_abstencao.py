import uuid

from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class PerfilComparecimentoAbstencao(Base):
    __tablename__ = "perfil_comparecimento_abstencao"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    dt_geracao = Column(String(10), nullable=True)
    hh_geracao = Column(String(8), nullable=True)
    ano_eleicao = Column(Integer, nullable=True)
    nr_turno = Column(Integer, nullable=True)
    sg_uf = Column(String(2), nullable=True)
    cd_municipio = Column(Integer, nullable=True)
    nm_municipio = Column(String(23), nullable=True)
    nr_zona = Column(Integer, nullable=True)
    cd_genero = Column(Integer, nullable=True)
    ds_genero = Column(String(9), nullable=True)
    cd_estado_civil = Column(Integer, nullable=True)
    ds_estado_civil = Column(String(22), nullable=True)
    cd_faixa_etaria = Column(Integer, nullable=True)
    ds_faixa_etaria = Column(String(16), nullable=True)
    cd_grau_escolaridade = Column(Integer, nullable=True)
    ds_grau_escolaridade = Column(String(29), nullable=True)
    cd_cor_raca = Column(Integer, nullable=True)
    ds_cor_raca = Column(String(13), nullable=True)
    cd_quilombola = Column(Integer, nullable=True)
    ds_quilombola = Column(String(13), nullable=True)
    cd_interprete_libras = Column(Integer, nullable=True)
    ds_interprete_libras = Column(String(13), nullable=True)
    cd_identidade_genero = Column(Integer, nullable=True)
    ds_identidade_genero = Column(String(20), nullable=True)
    cd_idioma_indigena = Column(Integer, nullable=True)
    ds_idioma_indigena = Column(String(13), nullable=True)
    cd_grupo_indigena = Column(Integer, nullable=True)
    ds_grupo_indigena = Column(String(16), nullable=True)
    qt_aptos = Column(Integer, nullable=True)
    qt_comparecimento = Column(Integer, nullable=True)
    qt_abstencao = Column(Integer, nullable=True)
    qt_comparecimento_deficiencia = Column(Integer, nullable=True)
    qt_abstencao_deficiencia = Column(Integer, nullable=True)
    qt_comparecimento_tte = Column(Integer, nullable=True)
    qt_abstencao_tte = Column(Integer, nullable=True)
    qt_comparec_facultativo = Column(Integer, nullable=True)
    qt_abst_facultativo = Column(Integer, nullable=True)
    qt_comparec_obrigatorio = Column(Integer, nullable=True)
    qt_abst_obrigatorio = Column(Integer, nullable=True)
    qt_comparec_defic_facultativo = Column(Integer, nullable=True)
    qt_abst_defic_facultativo = Column(Integer, nullable=True)
    qt_comparec_defic_obrigatorio = Column(Integer, nullable=True)
    qt_abst_defic_obrigatorio = Column(Integer, nullable=True)