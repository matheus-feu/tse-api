import uuid

from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class ConsultaCandidatos(Base):
    __tablename__ = "consulta_cand"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    dt_geracao = Column(String(10), nullable=True)
    hh_geracao = Column(String(8), nullable=True)
    ano_eleicao = Column(Integer, nullable=True)
    cd_tipo_eleicao = Column(Integer, nullable=True)
    nm_tipo_eleicao = Column(String(19), nullable=True)
    nr_turno = Column(Integer, nullable=True)
    cd_eleicao = Column(Integer, nullable=True)
    ds_eleicao = Column(String(38), nullable=True)
    dt_eleicao = Column(String(10), nullable=True)
    tp_abrangencia = Column(String(9), nullable=True)
    sg_uf = Column(String(2), nullable=True)
    sg_ue = Column(Integer, nullable=True)
    nm_ue = Column(String(32), nullable=True)
    cd_cargo = Column(Integer, nullable=True)
    ds_cargo = Column(String(13), nullable=True)
    sq_candidato = Column(Integer, nullable=True)
    nr_candidato = Column(Integer, nullable=True)
    nm_candidato = Column(String(57), nullable=True)
    nm_urna_candidato = Column(String(30), nullable=True)
    nm_social_candidato = Column(String(30), nullable=True)
    nr_cpf_candidato = Column(Integer, nullable=True)
    ds_email = Column(String(14), nullable=True)
    cd_situacao_candidatura = Column(Integer, nullable=True)
    ds_situacao_candidatura = Column(String(3), nullable=True)
    tp_agremiacao = Column(String(15), nullable=True)
    nr_partido = Column(Integer, nullable=True)
    sg_partido = Column(String(13), nullable=True)
    nm_partido = Column(String(46), nullable=True)
    nr_federacao = Column(Integer, nullable=True)
    nm_federacao = Column(String(41), nullable=True)
    sg_federacao = Column(String(14), nullable=True)
    ds_composicao_federacao = Column(String(14), nullable=True)
    sq_coligacao = Column(Integer, nullable=True)
    nm_coligacao = Column(String(54), nullable=True)
    ds_composicao_coligacao = Column(String(136), nullable=True)
    sg_uf_nascimento = Column(String(2), nullable=True)
    dt_nascimento = Column(String(10), nullable=True)
    nr_titulo_eleitoral_candidato = Column(Integer, nullable=True)
    cd_genero = Column(Integer, nullable=True)
    ds_genero = Column(String(9), nullable=True)
    cd_grau_instrucao = Column(Integer, nullable=True)
    ds_grau_instrucao = Column(String(29), nullable=True)
    cd_estado_civil = Column(Integer, nullable=True)
    ds_estado_civil = Column(String(25), nullable=True)
    cd_cor_raca = Column(Integer, nullable=True)
    ds_cor_raca = Column(String(13), nullable=True)
    cd_ocupacao = Column(Integer, nullable=True)
    ds_ocupacao = Column(String(70), nullable=True)
    cd_sit_tot_turno = Column(Integer, nullable=True)
    ds_sit_tot_turno = Column(String(16), nullable=True)
