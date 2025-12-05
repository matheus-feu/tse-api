import uuid

from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class DetalheVotacaoMunzona(Base):
    """Detalhe da apuração por município e zona"""

    __tablename__ = "detalhe_votacao_munzona"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    dt_geracao = Column(String(10), nullable=True)
    hh_geracao = Column(String(8), nullable=True)
    ano_eleicao = Column(Integer, nullable=True)
    cd_tipo_eleicao = Column(Integer, nullable=True)
    nm_tipo_eleicao = Column(String(22), nullable=True)
    nr_turno = Column(Integer, nullable=True)
    cd_eleicao = Column(Integer, nullable=True)
    ds_eleicao = Column(String(38), nullable=True)
    dt_eleicao = Column(String(10), nullable=True)
    tp_abrangencia = Column(String(1), nullable=True)
    sg_uf = Column(String(2), nullable=True)
    sg_ue = Column(Integer, nullable=True)
    nm_ue = Column(String(32), nullable=True)
    cd_municipio = Column(Integer, nullable=True)
    nm_municipio = Column(String(32), nullable=True)
    nr_zona = Column(Integer, nullable=True)
    cd_cargo = Column(Integer, nullable=True)
    ds_cargo = Column(String(8), nullable=True)
    qt_aptos = Column(Integer, nullable=True)
    qt_secoes_principais = Column(Integer, nullable=True)
    qt_secoes_agregadas = Column(Integer, nullable=True)
    qt_secoes_nao_instaladas = Column(Integer, nullable=True)
    qt_total_secoes = Column(Integer, nullable=True)
    qt_comparecimento = Column(Integer, nullable=True)
    qt_eleitores_secoes_nao_instaladas = Column(Integer, nullable=True)
    qt_abstencoes = Column(Integer, nullable=True)
    st_voto_em_transito = Column(String(1), nullable=True)
    qt_votos = Column(Integer, nullable=True)
    qt_votos_concorrentes = Column(Integer, nullable=True)
    qt_total_votos_validos = Column(Integer, nullable=True)
    qt_votos_nominais_validos = Column(Integer, nullable=True)
    qt_total_votos_leg_validos = Column(Integer, nullable=True)
    qt_votos_leg_validos = Column(Integer, nullable=True)
    qt_votos_nom_convr_leg_validos = Column(Integer, nullable=True)
    qt_total_votos_anulados = Column(Integer, nullable=True)
    qt_votos_nominais_anulados = Column(Integer, nullable=True)
    qt_votos_legenda_anulados = Column(Integer, nullable=True)
    qt_total_votos_anul_subjud = Column(Integer, nullable=True)
    qt_votos_nominais_anul_subjud = Column(Integer, nullable=True)
    qt_votos_legenda_anul_subjud = Column(Integer, nullable=True)
    qt_votos_brancos = Column(Integer, nullable=True)
    qt_total_votos_nulos = Column(Integer, nullable=True)
    qt_votos_nulos = Column(Integer, nullable=True)
    qt_votos_nulos_tecnicos = Column(Integer, nullable=True)
    qt_votos_anulados_apu_sep = Column(Integer, nullable=True)
    hh_ultima_totalizacao = Column(String(8), nullable=True)
    dt_ultima_totalizacao = Column(String(10), nullable=True)
