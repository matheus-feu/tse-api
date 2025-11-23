from datetime import datetime
from typing import Optional, Dict, List

import httpx
import xmltodict
from loguru import logger

from app.core.config import settings


class LocalizationService:
    """
    Serviço para buscar endereços de zonas eleitorais via API TRE-SP.

    API Endpoint: https://apps.tre-sp.jus.br/api-gateway/zonaEleitoral/1.0
    Formato: GET /{numeroZona}/localVotacao/{ano}/{mes}
    Retorno: XML (convertido para JSON)
    """

    def __init__(
            self,
            api_base_url: str = settings.LOCALIZATION_API_URL,
            timeout: int = 30,
            bearer_token: Optional[str] = None
    ):
        """
        Inicializa o serviço de localização.

        Args:
            api_base_url: URL base da API TRE-SP
            timeout: Timeout das requisições em segundos
            bearer_token: Token de autorização (opcional, API não exige)
        """
        self.api_base_url = api_base_url
        self.timeout = timeout
        self.bearer_token = bearer_token

        headers = {
            'accept': 'text/xml',
            'User-Agent': 'CKAN-TSE-API/1.0'
        }
        if bearer_token:
            headers['Authorization'] = f'Bearer {bearer_token}'

        self.client = httpx.AsyncClient(base_url=self.api_base_url, headers=headers, timeout=self.timeout, verify=False)

        self.cache = {}

        logger.info(f"🌍 LocalizationService inicializado: {api_base_url}")

    async def enrich_localization(self, record: Dict) -> Dict:
        """
        Enriquece UM registro com dados de localização.

        Args:
            record: Dicionário com dados do registro
                   Deve conter: ano_eleicao, nr_zona, cd_municipio, sg_uf

        Returns:
            Dicionário atualizado com campos de localização preenchidos
        """
        try:
            year = record.get('ano_eleicao')
            number_zone = record.get('nr_zona')
            code_municipality = record.get('cd_municipio')
            sg_uf = record.get('sg_uf')

            if not all([year, number_zone, code_municipality, sg_uf]):
                logger.debug(f"Dados insuficientes para localização: {record}")
                return record

            month = self._calculate_election_month(year)

            cache_key = f"{sg_uf}_{number_zone}_{year}_{month}"
            if cache_key in self.cache:
                logger.debug(f"📦 Cache hit: {cache_key}")
                localization_data = self.cache[cache_key]
            else:
                logger.debug(f"🌐 Buscando localização: {cache_key}")
                localization = await self._search_localization_api(number_zone, year, month)

                if localization:
                    self.cache[cache_key] = localization

            if localization:
                record['endereco_zona'] = localization.get('endereco')
                record['bairro_zona'] = localization.get('bairro')
                record['cep_zona'] = localization.get('cep')
                record['telefone_zona'] = localization.get('telefone')
                logger.debug(f"✅ Registro enriquecido: {cache_key}")
            else:
                logger.debug(f"⚠️ Localização não encontrada: {cache_key}")

                return record

        except Exception as e:
            logger.error(f"Erro ao enriquecer localização: {e}")
            return record

    async def enrich_lotes(self, records: List[Dict]) -> List[Dict]:
        """
         Enriquece LOTE de registros com dados de localização.

         Args:
             records: Lista de dicionários com dados dos registros

         Returns:
             Lista de dicionários enriquecidos
         """
        logger.info(f"🌍 Enriquecendo lote de {len(records)} registros...")

        beginning = datetime.now()

        enriched_records: List[Dict] = []

        for idx, record in enumerate(records):
            enriched = await self.enrich_localization(record)
            enriched_records.append(enriched)

            if (idx + 1) % 1000 == 0:
                elapsed = (datetime.now() - beginning).total_seconds()
                logger.info(f"  ⏱️ {idx + 1} registros processados em {elapsed:.2f}s")

        return enriched_records

    async def _search_localization_api(self, number_zone: int, year: int, month: int) -> Optional[Dict]:
        """
        Busca dados de localização via API TRE-SP.

        Args:
            number_zone: Número da zona eleitoral
            year: Ano da eleição
            month: Mês da eleição
        Returns:
            Dicionário com dados de localização ou None se não encontrado
        """
        try:
            url = f"{self.api_base_url}/{number_zone}/localVotacao/{year}/{month:02d}"

            logger.debug(f"🔗 Requisição GET: {url}")

            response = await self.client.get(url)
            if response.status_code == 200:
                xml_text = response.text
                data = self._xml_to_json(xml_text)
                return self.extract_data_from_response(data)

            elif response.status_code == 404:
                logger.warning(f"Localização não encontrada: Zona {number_zone}, {year}/{month:02d}")
                return None
            else:
                logger.error(f"Erro na API TRE-SP: {response.status_code} - {response.text}")
                return None

        except httpx.TimeoutException:
            logger.warning(f"⏱️ Timeout ao buscar localização: zona {number_zone}, {year}/{month:02d}")
            return None
        except Exception as e:
            logger.error(f"❌ Erro ao buscar localização: {e}")
            return None

    @classmethod
    def _xml_to_json(cls, xml_text: str) -> Dict:
        """Converte XML para JSON."""
        try:
            data = xmltodict.parse(xml_text)
            return data
        except Exception as e:
            logger.error(f"Erro ao converter XML para JSON: {e}")
            return {}

    def extract_data_from_response(self, data: Dict) -> Optional[Dict]:
        """Extrai dados relevantes da resposta JSON."""
        try:
            root = data.get('resposta', {})
            if not root:
                return None

            items = root.get('item', {})
            if isinstance(items, dict):
                items = [items]

            if not items:
                return None

            first_local = items[0]

            local_name = first_local.get('nome', '').strip()
            indicator = first_local.get('indicador', '').strip()

            zone_info = first_local.get('zona', {})
            zone_name = zone_info.get('nome', '').strip()
            capital_area = zone_info.get('areaCapital', '').strip()
            zone_number = zone_info.get('numero', '').strip()
            zone_region = zone_info.get('regiao', '').strip()

            code = first_local.get('codigo', {})
            local_code = code.get('local', '').strip()
            municipality_code = code.get('municipio', '').strip()

            address = f"{local_name} - {zone_name}"

            area_map = {
                'N': 'Norte',
                'S': 'Sul',
                'L': 'Leste',
                'O': 'Oeste',
                'C': 'Centro'
            }

            neighborhood = area_map.get(capital_area, capital_area)
            logger.debug(f"✅ Dados extraídos: {local_name} ({zone_number})")

            return {
                'endereco': address,
                'bairro': neighborhood,
                'zona_eleitoral_numero': zone_number,
                'zona_nome': zone_name,
                'municipio_codigo': municipality_code,
                'local_codigo': local_code,
                'status': 'ativo' if indicator == "1" else 'inativo',
                'regiao_zona': zone_region,
            }

        except Exception as e:
            logger.error(f"Erro ao extrair dados da resposta: {e}")
            return None

    def _calculate_election_month(self, year: int) -> int:
        """
        Calcula o mês da eleição com base no ano.

        Args:
            year: Ano da eleição

        Returns:
            Mês da eleição (int)
        """
        if year % 4 == 0:
            return 10
        else:
            return 11

    def clean_cache(self):
        """Limpa o cache de localizações."""
        self.cache.clear()
        logger.info("🧹 Cache de localizações limpo")

    async def close(self):
        """Fecha cliente HTTP."""
        await self.client.aclose()
        logger.info(f"🔒 LocalizationService fechado (cache: {len(self.cache)} entradas)")
