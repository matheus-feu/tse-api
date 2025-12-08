import uuid

from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class DetalheVotacaoSecao(Base):
    """"Detalhe da apuração por seção eleitoral"""

    __tablename__ = "detalhe_votacao_secao"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    dt_geracao = Column(String(10), nullable=True)
    hh_geracao = Column(String(8), nullable=True)
    ano_eleicao = Column(Integer, nullable=True, unique=True)
    cd_tipo_eleicao = Column(Integer, nullable=True)
    nm_tipo_eleicao = Column(String(22), nullable=True)
    nr_turno = Column(Integer, nullable=True)
    cd_eleicao = Column(Integer, nullable=True)
    ds_eleicao = Column(String(38), nullable=True)
    dt_eleicao = Column(String(10), nullable=True)
    tp_abrangencia = Column(String(1), nullable=True)
    sg_uf = Column(String(2), nullable=True)
    sg_ue = Column(Integer, nullable=True)
    nm_ue = Column(String(25), nullable=True)
    cd_municipio = Column(Integer, nullable=True)
    nm_municipio = Column(String(25), nullable=True)
    nr_zona = Column(Integer, nullable=True)
    nr_secao = Column(Integer, nullable=True)
    cd_cargo = Column(Integer, nullable=True)
    ds_cargo = Column(String(8), nullable=True)
    qt_aptos = Column(Integer, nullable=True)
    qt_comparecimento = Column(Integer, nullable=True)
    qt_abstencoes = Column(Integer, nullable=True)
    qt_votos_nominais = Column(Integer, nullable=True)
    qt_votos_brancos = Column(Integer, nullable=True)
    qt_votos_nulos = Column(Integer, nullable=True)
    qt_votos_legenda = Column(Integer, nullable=True)
    qt_votos_anulados_apu_sep = Column(Integer, nullable=True)
    nr_local_votacao = Column(Integer, nullable=True)
    nm_local_votacao = Column(String(70), nullable=True)
    ds_local_votacao_endereco = Column(String(70), nullable=True)
    dt_recebimento_bu_hor_tse = Column(String(19), nullable=True)
    dt_prim_tot_parcial_hor_tse = Column(String(19), nullable=True)
    ds_origem_voto = Column(String(15), nullable=True)
    st_secao_instalada = Column(String(3), nullable=True)
    st_secao_anulada = Column(String(3), nullable=True)
    cd_modelo_urna = Column(Integer, nullable=True)
    ds_modelo_urna = Column(String(7), nullable=True)
