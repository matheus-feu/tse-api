import uuid

from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class VotacaoPartidoMunZona(Base):
    """Votação em partido por município e zona"""

    __tablename__ = "votacao_partido_munzona"

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
    tp_agremiacao = Column(String(15), nullable=True)
    nr_partido = Column(Integer, nullable=True)
    sg_partido = Column(String(13), nullable=True)
    nm_partido = Column(String(46), nullable=True)
    nr_federacao = Column(Integer, nullable=True)
    nm_federacao = Column(String(41), nullable=True)
    sg_federacao = Column(String(14), nullable=True)
    ds_composicao_federacao = Column(String(17), nullable=True)
    sq_coligacao = Column(Integer, nullable=True)
    nm_coligacao = Column(String(84), nullable=True)
    ds_composicao_coligacao = Column(String(185), nullable=True)
    st_voto_em_transito = Column(String(1), nullable=True)
    qt_votos_legenda_validos = Column(Integer, nullable=True)
    qt_votos_nom_convr_leg_validos = Column(Integer, nullable=True)
    qt_total_votos_leg_validos = Column(Integer, nullable=True)
    qt_votos_nominais_validos = Column(Integer, nullable=True)
    qt_votos_legenda_anul_subjud = Column(Integer, nullable=True)
    qt_votos_nominais_anul_subjud = Column(Integer, nullable=True)
    qt_votos_legenda_anulados = Column(Integer, nullable=True)
    qt_votos_nominais_anulados = Column(Integer, nullable=True)
