from app.services.etl.transformers.base_transformer import BaseTransformer


class VotationCandidateTransformer(BaseTransformer):
    """Transforma dados de votação por candidato."""

    COLUMN_MAPPING = [
        'nr_turno',
        'ano_eleicao',
        'cd_eleicao',
        'dt_eleicao',
        'sg_uf',
        'sg_ue',
        'nm_ue',
        'cd_municipio',
        'nm_municipio',
        'nr_zona',
        'ds_cargo',
        'nm_candidato',
        'nr_partido',
        'sg_partido',
        'nm_partido',
        'qt_votos_nominais',
        'qt_votos_nominais_validos',
    ]

    TYPE_MAPPING = {
        'nr_turno': 'int',
        'ano_eleicao': 'int',
        'cd_eleicao': 'int',
        'cd_municipio': 'int',
        'nr_zona': 'int',
        'nr_candidato': 'int',
        'nr_partido': 'int',
        'qt_votos_nominais': 'int',
        'qt_votos_nominais_validos': 'int',
        'dt_eleicao': 'date',
    }


class VotationPartyTransformer(BaseTransformer):
    """Transforma dados de votação por partido."""

    COLUMN_MAPPING = [
        'ano_eleicao',
        'nr_turno',
        'cd_eleicao',
        'ds_eleicao',
        'dt_eleicao',
        'sg_uf',
        'sg_ue',
        'nm_ue',
        'cd_municipio',
        'nm_municipio',
        'nr_zona',
        'ds_cargo',
        'nr_partido',
        'sg_partido',
        'nm_partido',
        'qt_votos_legenda_validos',
        'qt_votos_nom_convr_leg_validos',
        'qt_total_votos_leg_validos',
        'qt_votos_nominais_validos',
        'qt_votos_legenda_anul_subjud',
        'qt_votos_nominais_anul_subjud',
        'qt_votos_legenda_anulados',
        'qt_votos_nominais_anulados',
    ]

    TYPE_MAPPING = {
        'ano_eleicao': 'int',
        'nr_turno': 'int',
        'cd_eleicao': 'int',
        'cd_municipio': 'int',
        'nr_zona': 'int',
        'cd_cargo': 'int',
        'nr_partido': 'int',
        'qt_votos_legenda_validos': 'int',
        'qt_votos_nom_convr_leg_validos': 'int',
        'qt_total_votos_leg_validos': 'int',
        'qt_votos_nominais_validos': 'int',
        'qt_votos_legenda_anul_subjud': 'int',
        'qt_votos_nominais_anul_subjud': 'int',
        'qt_votos_legenda_anulados': 'int',
        'qt_votos_nominais_anulados': 'int',
        'dt_eleicao': 'date',
    }
