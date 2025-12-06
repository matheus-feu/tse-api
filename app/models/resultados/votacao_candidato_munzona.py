import uuid

from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class VotacaoCandidatoMunZona(Base):
    """Votação em candidato por município e zona"""

    __tablename__ = "votacao_candidato_munzona"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    dt_geracao = Column(String(10), nullable=True)
    hh_geracao = Column(String(8), nullable=True)
    ano_eleicao = Column(Integer, nullable=True)
    cd_tipo_eleicao = Column(Integer, nullable=True)
    nm_tipo_eleicao = Column(String(17), nullable=True)
    nr_turno = Column(Integer, nullable=True)
    cd_eleicao = Column(Integer, nullable=True)
    ds_eleicao = Column(String(24), nullable=True)
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
    sq_candidato = Column(BigInteger, nullable=True)
    nr_candidato = Column(Integer, nullable=True)
    nm_candidato = Column(String(57), nullable=True)
    nm_urna_candidato = Column(String(30), nullable=True)
    nm_social_candidato = Column(String(25), nullable=True)
    cd_situacao_candidatura = Column(Integer, nullable=True)
    ds_situacao_candidatura = Column(String(3), nullable=True)
    cd_detalhe_situacao_cand = Column(Integer, nullable=True)
    ds_detalhe_situacao_cand = Column(String(3), nullable=True)
    cd_situacao_julgamento = Column(Integer, nullable=True)
    ds_situacao_julgamento = Column(String(22), nullable=True)
    cd_situacao_cassacao = Column(Integer, nullable=True)
    ds_situacao_cassacao = Column(String(7), nullable=True)
    cd_situacao_dconst_diploma = Column(Integer, nullable=True)
    ds_situacao_dconst_diploma = Column(String(6), nullable=True)
    tp_agremiacao = Column(String(15), nullable=True)
    nr_partido = Column(Integer, nullable=True)
    sg_partido = Column(String(13), nullable=True)
    nm_partido = Column(String(39), nullable=True)
    nr_federacao = Column(Integer, nullable=True)
    nm_federacao = Column(String(41), nullable=True)
    sg_federacao = Column(String(14), nullable=True)
    ds_composicao_federacao = Column(String(17), nullable=True)
    sq_coligacao = Column(BigInteger, nullable=True)
    nm_coligacao = Column(String(50), nullable=True)
    ds_composicao_coligacao = Column(String(121), nullable=True)
    st_voto_em_transito = Column(String(1), nullable=True)
    qt_votos_nominais = Column(Integer, nullable=True)
    nm_tipo_destinacao_votos = Column(String(18), nullable=True)
    qt_votos_nominais_validos = Column(Integer, nullable=True)
    cd_sit_tot_turno = Column(Integer, nullable=True)
    ds_sit_tot_turno = Column(String(13), nullable=True)
