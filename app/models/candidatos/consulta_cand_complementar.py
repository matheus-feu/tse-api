import uuid

from sqlalchemy import Column, Integer, Text, DateTime, String
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class ConsultaCandComplementar(Base):
    __tablename__ = "consulta_cand_complementar"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    dt_geracao = Column(String(10), nullable=True)
    hh_geracao = Column(String(8), nullable=True)
    ano_eleicao = Column(Integer, nullable=True, unique=True)
    cd_eleicao = Column(Integer, nullable=True)
    sq_candidato = Column(Integer, nullable=True)
    cd_detalhe_situacao_cand = Column(Integer, nullable=True)
    ds_detalhe_situacao_cand = Column(String(3), nullable=True)
    cd_nacionalidade = Column(Integer, nullable=True)
    ds_nacionalidade = Column(String(25), nullable=True)
    cd_municipio_nascimento = Column(Integer, nullable=True)
    nm_municipio_nascimento = Column(String(28), nullable=True)
    nr_idade_data_posse = Column(Integer, nullable=True)
    st_quilombola = Column(String(1), nullable=True)
    cd_etnia_indigena = Column(Integer, nullable=True)
    ds_etnia_indigena = Column(String(20), nullable=True)
    vr_despesa_max_campanha = Column(Text, nullable=True)
    st_reeleicao = Column(String(1), nullable=True)
    st_declarar_bens = Column(String(1), nullable=True)
    nr_protocolo_candidatura = Column(Integer, nullable=True)
    nr_processo = Column(Integer, nullable=True)
    cd_situacao_candidato_pleito = Column(Integer, nullable=True)
    ds_situacao_candidato_pleito = Column(String(3), nullable=True)
    cd_situacao_candidato_urna = Column(Integer, nullable=True)
    ds_situacao_candidato_urna = Column(String(3), nullable=True)
    st_candidato_inserido_urna = Column(String(3), nullable=True)
    nm_tipo_destinacao_votos = Column(String(18), nullable=True)
    cd_situacao_candidato_tot = Column(Integer, nullable=True)
    ds_situacao_candidato_tot = Column(String(22), nullable=True)
    st_prest_contas = Column(String(1), nullable=True)
    st_substituido = Column(String(1), nullable=True)
    sq_substituido = Column(Integer, nullable=True)
    sq_ordem_suplencia = Column(Integer, nullable=True)
    dt_aceite_candidatura = Column(DateTime(timezone=True), nullable=True)
    cd_situacao_julgamento = Column(Integer, nullable=True)
    ds_situacao_julgamento = Column(String(43), nullable=True)
    cd_situacao_julgamento_pleito = Column(Integer, nullable=True)
    ds_situacao_julgamento_pleito = Column(String(22), nullable=True)
    cd_situacao_julgamento_urna = Column(Integer, nullable=True)
    ds_situacao_julgamento_urna = Column(String(22), nullable=True)
    cd_situacao_cassacao = Column(Integer, nullable=True)
    ds_situacao_cassacao = Column(String(7), nullable=True)
    cd_situacao_cassacao_midia = Column(Integer, nullable=True)
    ds_situacao_cassacao_midia = Column(String(5), nullable=True)
    cd_situacao_diploma = Column(Integer, nullable=True)
    ds_situacao_diploma = Column(String(5), nullable=True)
