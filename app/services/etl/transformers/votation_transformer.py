from typing import List, Dict

import pandas as pd
from loguru import logger


class VotationCandidateTransformer:
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
        'nr_candidato',
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

    @classmethod
    def _is_valid_value(cls, v) -> bool:
        """Verifica se valor é válido para inserção no banco."""

        # Nulo
        if v is None:
            return False

        # String vazia
        if isinstance(v, str) and v.strip() == "":
            return False

        # Float NaN
        if isinstance(v, float) and pd.isna(v):
            return False

        # NaT (Not a Time)
        if hasattr(v, '__class__') and v.__class__.__name__ == 'NaTType':
            return False

        # Pandas NA (genérico)
        try:
            if pd.isna(v):
                return False
        except (TypeError, ValueError):
            pass

        return True

    def transform_dataframe_in_dict(self, df: pd.DataFrame) -> List[Dict]:
        """
        Transforma DataFrame em lista de dicionários com tipos corretos.

        Fluxo:
        1. Normaliza nomes das colunas para minúsculas
        2. Filtra colunas válidas
        3. Converte tipos (int, date, etc)
        4. Remove linhas vazias e duplicatas
        5. Converte para dicionários
        6. Remove campos nulos
        """
        logger.info("Transformando DataFrame de votação por candidato")

        df.columns = df.columns.str.lower()

        available_columns = [col for col in self.COLUMN_MAPPING if col in df.columns]
        df_filtered = df[available_columns].copy()

        for col, dtype in self.TYPE_MAPPING.items():
            if col not in df_filtered.columns:
                continue

            if dtype == 'int':
                df_filtered[col] = pd.to_numeric(df_filtered[col], errors='coerce')
                df_filtered[col] = df_filtered[col].fillna(0).astype(int)

            elif dtype == 'date':
                df_filtered[col] = pd.to_datetime(df_filtered[col], errors='coerce')
                df_filtered = df_filtered[df_filtered[col].notna()]
                df_filtered[col] = df_filtered[col].dt.date

        df_filtered = df_filtered.dropna(how='all').drop_duplicates()
        records = df_filtered.to_dict(orient='records')

        cleaned_records = []
        for record in records:
            cleaned_record = {
                k: v for k, v in record.items()
                if self._is_valid_value(v)
            }
            cleaned_records.append(cleaned_record)

        logger.info(f"Transformados {len(cleaned_records)} registros")
        return cleaned_records


class VotationPartyTransformer:
    """
        Transforma
        dados
        de
        votação
        por
        partido.
        """

    COLUMN_MAPPING = {
        'NR_TURNO': 'nr_turno', 'ANO_ELEICAO': 'ano_eleicao',
        'CD_ELEICAO': 'cd_eleicao', 'DS_ELEICAO': 'ds_eleicao',
        'DT_ELEICAO': 'dt_eleicao', 'SG_UF': 'sg_uf',
        'SG_UE': 'sg_ue', 'NM_UE': 'nm_ue',
        'CD_MUNICIPIO': 'cd_municipio', 'NM_MUNICIPIO': 'nm_municipio',
        'NR_ZONA': 'nr_zona', 'CD_CARGO': 'cd_cargo', 'DS_CARGO': 'ds_cargo',
        'NR_PARTIDO': 'nr_partido', 'SG_PARTIDO': 'sg_partido',
        'NM_PARTIDO': 'nm_partido',
        'QT_VOTOS_NOMINAIS': 'qt_votos_nominais',
        'QT_VOTOS_NOMINAIS_VALIDOS': 'qt_votos_nominais_validos',
        'QT_VOTOS_NOMINAIS_ANULADOS': 'qt_votos_nominais_anulados'
    }

    def transform_dataframe_in_dict(self, df: pd.DataFrame) -> List[Dict]:
        """
        Transforma
        DataFrame
        em
        dicionários.
        """
        df = df.dropna(how='all')
        df = df.rename(columns=self.COLUMN_MAPPING)

        # Converte tipos numéricos
        for col in ['nr_turno', 'ano_eleicao', 'cd_eleicao', 'cd_municipio',
                    'nr_zona', 'cd_cargo', 'nr_partido',
                    'qt_votos_nominais', 'qt_votos_nominais_validos',
                    'qt_votos_nominais_anulados']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

        # Converte data
        if 'dt_eleicao' in df.columns:
            df['dt_eleicao'] = pd.to_datetime(df['dt_eleicao'], format='%d/%m/%Y', errors='coerce')
            df['dt_eleicao'] = df['dt_eleicao'].dt.strftime('%Y-%m-%d')

        # Limpa strings
        for col in ['sg_uf', 'sg_partido']:
            if col in df.columns:
                df[col] = df[col].str.upper().str.strip()

        logger.info(f"Transformados {len(df)} registros")
        return df.to_dict('records')
