import os
import tempfile
import zipfile

import pandas as pd
from loguru import logger

from app.utils.http_client import HttpClient


class PackageExtractor(HttpClient):
    """Extrator simplificado para pacotes ZIP do TSE."""

    def __init__(self, timeout: float = 60.0):
        super().__init__(timeout=timeout)

    async def extract_csv_from_zip(self, url: str):
        logger.info(f"Baixando ZIP do TSE: {url}")

        content = await self.get_bytes(url)
        if not content:
            raise ValueError("Conteúdo vazio ao baixar o ZIP")

        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = os.path.join(tmpdir, "package.zip")
            with open(zip_path, "wb") as f:
                f.write(content)

            with zipfile.ZipFile(zip_path, "r") as zf:
                csv_names = [n for n in zf.namelist() if n.lower().endswith(".csv")]
                if not csv_names:
                    raise ValueError("Nenhum CSV encontrado no ZIP")
                csv_name = csv_names[0]

                zf.extract(csv_name, tmpdir)
                csv_path = os.path.join(tmpdir, csv_name)

            logger.info(f"CSV extraído: {csv_name}")

            df = pd.read_csv(csv_path, sep=";", encoding="latin1", low_memory=False)
            return df, os.path.basename(csv_name)
