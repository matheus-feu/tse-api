import httpx

from loguru import logger


class HttpClient:
    """
   Cliente HTTP assíncrono básico para ser reutilizado nos extractors.
   Garante timeout e tratamento de erros padronizados.
   """

    def __init__(self, timeout: float = 60.0):
        self.timeout = timeout
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self.timeout)
        return self._client

    async def get_bytes(self, url: str) -> bytes:
        """
        Faz um GET e retorna o conteúdo bruto (bytes).
        Lança httpx.HTTPStatusError se status != 2xx.
        """
        client = await self._get_client()
        logger.debug(f"HTTP GET (bytes): {url}")
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.content

    async def get_text(self, url: str, encoding: str | None = None) -> str:
        """
        Faz um GET e retorna o corpo como texto.
        """
        client = await self._get_client()
        logger.debug(f"HTTP GET (text): {url}")
        resp = await client.get(url)
        resp.raise_for_status()
        if encoding:
            resp.encoding = encoding
        return resp.text

    async def stream(self, method: str, url: str, **kwargs):
        """Wrapper para stream assíncrono (se você quiser manter o padrão stream)."""
        client = await self._get_client()
        logger.debug(f"HTTP {method} (stream): {url}")
        return client.stream(method, url, **kwargs)

    async def close(self) -> None:
        """
        Fecha o client subjacente, se existir.
        """
        if self._client is not None:
            await self._client.aclose()
            self._client = None
