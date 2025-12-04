import io
import zipfile
from typing import AsyncGenerator, Optional

import httpx
import pandas as pd
from loguru import logger

from app.utils.http_client import HttpClient


class VotationExtractor(HttpClient):
    """Extrator simplificado usando CDN direta do TSE."""

    CDN_TSE_BASE_URL = "https://cdn.tse.jus.br/estatistica/sead/odsele"

    def __init__(self, timeout: float = 60.0):
        super().__init__(timeout=timeout)

    async def extract_csv_from_tse(
            self,
            process_type: str,
            year: int,
            uf: Optional[str] = None
    ) -> AsyncGenerator[pd.DataFrame, None]:
        """
        Extrai votação por candidato usando CDN direta do TSE.

        Args:
            process_type: Tipo de processo (ex: 'votacao_candidato_munzona' ou 'votacao_partido_munzona')
            year: Ano da eleição (ex: 2024)
            uf: Sigla da UF para filtrar (opcional)

        Yields:
            DataFrame com dados de votação
        """
        zip_url = f"{self.CDN_TSE_BASE_URL}/{process_type}/{process_type}_{year}.zip"
        if uf:
            expected_csv = f"{process_type}_{year}_{uf.upper()}.csv"
        else:
            expected_csv = f"{process_type}_{year}_BRASIL.csv"
        logger.info(f"Baixando... url: {zip_url} | csv: {expected_csv}")

        try:
            async for df in self._download_and_extract_csv(
                    url=zip_url,
                    expected_csv=expected_csv
            ):
                logger.info(f"✅ CSV extraído: {len(df):,} registros")
                yield df
        except ValueError as e:
            logger.error(f"❌ Erro na extração: {e}")
            raise

    async def _download_and_extract_csv(
            self,
            url: str,
            expected_csv: str,
            encoding: str = 'latin-1',
            sep: str = ';'
    ) -> AsyncGenerator[pd.DataFrame, None]:
        """
            Baixa um ZIP via HTTP e extrai APENAS o CSV especificado.

            Args:
                url: URL do arquivo ZIP
                expected_csv: Nome exato do CSV a extrair (ex: 'votacao_candidato_munzona_2024_BRASIL.csv')
                encoding: Encoding do CSV (padrão: 'latin-1' para TSE)
                sep: Separador do CSV (padrão: ';')

            Yields:
                DataFrame do CSV extraído

            Raises:
                HTTPStatusError: Se URL não existir (404, etc)
                ValueError: Se CSV não for encontrado no ZIP
            """
        logger.info(f"Baixando arquivo de {url}")

        try:
            async with await self.stream("GET", url) as response:
                response.raise_for_status()
                content = await response.aread()

            logger.info(f"✅ ZIP baixado: {len(content) / 1024 / 1024:.2f} MB")

            with zipfile.ZipFile(io.BytesIO(content)) as z:
                csv_files = [f for f in z.namelist() if f.endswith('.csv')]
                logger.debug(f"📂 CSVs no ZIP: {csv_files}")

                # Verifica se CSV esperado existe
                if expected_csv not in z.namelist():
                    logger.warning(f"⚠️  CSV '{expected_csv}' não encontrado")
                    logger.info(f"CSVs disponíveis: {csv_files}")

                    # Fallback: usa primeiro CSV se houver
                    if csv_files:
                        expected_csv = csv_files[0]
                        logger.info(f"📝 Usando CSV alternativo: {expected_csv}")
                    else:
                        raise ValueError(
                            f"Nenhum CSV encontrado no ZIP de {url}. "
                            f"Arquivos no ZIP: {z.namelist()}"
                        )

                with z.open(expected_csv) as f:
                    df = pd.read_csv(f, encoding=encoding, sep=sep, dtype=str, low_memory=False)

                logger.info(f"✅ CSV lido: {len(df):,} linhas, {len(df.columns)} colunas")
                yield df

        except httpx.HTTPStatusError as e:
            logger.error(f"❌ Erro HTTP {e.response.status_code}: {url}")
            raise ValueError(f"Arquivo não encontrado na CDN: {url} (HTTP {e.response.status_code})")

        except zipfile.BadZipFile:
            logger.error(f"❌ Arquivo baixado não é um ZIP válido: {url}")
            raise ValueError(f"Arquivo corrompido ou não é ZIP: {url}")

        except Exception as e:
            logger.error(f"❌ Erro ao processar ZIP: {e}", exc_info=True)
            raise
