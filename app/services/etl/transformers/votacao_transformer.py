from typing import List, Dict

import pandas as pd
from loguru import logger


class VotationCandidateTransformer:
    """Transforma dados de votação por candidato."""

    @classmethod
    def transform_dataframe(cls, df: pd.DataFrame) -> List[Dict]:
        """
        Transforma DataFrame em dicionários prontos para carga.

        Aplica:
        - Limpeza de linhas vazias
        - Renomeação de colunas
        - Conversão de tipos
        - Padronização de strings
        - Validação de dados obrigatórios
        - Criação de campos derivados
        """
        logger.info("Transformando DataFrame de votação por candidato")

        df = df.dropna(how='all')

        len_before = len(df)
        df = df.drop_duplicates()
        if len(df) < len_before:
            logger.info(f"Removidos {len_before - len(df)} registros duplicados")

        numeric_cols = [
            'nr_turno', 'ano_eleicao', 'cd_eleicao', 'cd_municipio',
            'nr_zona', 'nr_candidato', 'nr_partido',
            'qt_votos_nominais', 'qt_votos_nominais_validos'
        ]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

        if 'dt_eleicao' in df.columns:
            df['dt_eleicao'] = pd.to_datetime(
                df['dt_eleicao'],
                format='%d/%m/%Y',
                errors='coerce'
            )

        df['dt_eleicao'] = df['dt_eleicao'].dt.strftime('%Y-%m-%d')
        df['dt_eleicao'] = df['dt_eleicao'].replace({'NaT': None})

        string_cols = [
            'sg_uf', 'sg_partido', 'nm_candidato', 'nm_partido',
            'nm_municipio', 'ds_cargo', 'ds_situacao_totalizacao'
        ]

        for col in string_cols:
            if col in df.columns:
                # Remove espaços e coloca em maiúsculas
                df[col] = df[col].str.upper().str.strip()

            # Uppercase for state codes
            if col.startswith('sg_'):
                df[col] = df[col].str.upper()

            # Remove valores vazios
            df[col] = df[col].replace(['', 'nan', 'None', 'NaN'], None)

        required_cols = ['ano_eleicao', 'sg_uf', 'cd_municipio', 'nr_zona']
        for col in required_cols:
            if col in df.columns:
                before = len(df)
                if col in numeric_cols:
                    df = df[df[col] > 0]
                else:
                    df = df[df[col].notna()]

                if len(df) < before:
                    logger.info(f"Removidos {before - len(df)} registros com {col} inválido")

        # Campos derivados
        df['zona_eleitoral_id'] = (
                df['sg_uf'].astype(str) + '-' +
                df['cd_municipio'].astype(str) + '-' +
                df['nr_zona'].astype(str)
        )

        # Preparação para o enriquecimento
        df['endereco_zona'] = None
        df['bairro_zona'] = None
        df['cep_zona'] = None
        df['telefone_zona'] = None

        records = df.to_dict('records')
        logger.info(f"✅ Transformação concluída: {len(records)} registros válidos")

        if records:
            logger.debug(
                f"  ↳ UFs: {df['sg_uf'].nunique()} | "
                f"Municípios: {df['cd_municipio'].nunique()} | "
                f"Zonas: {df['nr_zona'].nunique()}"
            )

        return records


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

    def transform_dataframe(self, df: pd.DataFrame) -> List[Dict]:
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

        # Adiciona campos de localização
        df['zona_eleitoral_id'] = df.apply(
            lambda r: f"{r.get('sg_uf', '')}-{r.get('cd_municipio', 0)}-{r.get('nr_zona', 0)}", axis=1
        )
        df['endereco_zona'] = None
        df['bairro_zona'] = None
        df['cep_zona'] = None
        df['telefone_zona'] = None

        logger.info(f"Transformados {len(df)} registros")
        return df.to_dict('records')
