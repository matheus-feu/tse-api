from abc import ABC
from typing import List, Dict, Any

import pandas as pd
from loguru import logger


class BaseTransformer(ABC):
    """
    Transformer base para normalizar DataFrames do TSE.
    Basta especializar COLUMN_MAPPING e TYPE_MAPPING na subclasse.
    """
    COLUMN_MAPPING: List[str] = []
    TYPE_MAPPING: Dict[str, str] = {}

    @classmethod
    def _is_valid_value(cls, v) -> bool:
        if v is None:
            return False
        if isinstance(v, str) and v.strip() == "":
            return False
        if isinstance(v, float) and pd.isna(v):
            return False
        if hasattr(v, '__class__') and v.__class__.__name__ == 'NaTType':
            return False
        try:
            if pd.isna(v):
                return False
        except (TypeError, ValueError):
            pass
        return True

    def transform(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Método abstrato para transformar dados."""
        logger.info(f"Transformando DataFrame para {self.__class__.__name__}")

        df.columns = df.columns.str.lower()
        cols = [col for col in self.COLUMN_MAPPING if col in df.columns]
        df_filtered = df[cols].copy()

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

        cleaned_records = [
            {k: v for k, v in rec.items() if self._is_valid_value(v)} for rec in records
        ]

        logger.info(f"Transformados {len(cleaned_records)} registros")
        return cleaned_records
