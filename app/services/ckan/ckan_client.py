from typing import List, Dict

from ckanapi import RemoteCKAN
from loguru import logger


class CKANTSEClient:
    """Cliente para API do CKAN do TSE usando ckanapi."""

    def __init__(self):
        self.ckan = RemoteCKAN('https://dadosabertos.tse.jus.br/')
        self.organization = 'tribunal-superior-eleitoral'

    async def list_all_packages(self) -> List[str]:
        """
        Lista todos os packages (datasets) disponíveis no CKAN do TSE.
        Returns:
            Lista de IDs dos packages
        """
        try:
            packages = self.ckan.action.package_list()
            return packages
        except Exception as e:
            logger.error(f"Erro ao listar pacotes: {e}")
            raise

    async def get_package_details(self, package_id: str) -> Dict:
        """
        Busca detalhes completos de um package.

        Args:
            package_id: ID ou nome do package

        Returns:
            Dicionário com metadados do package
        """
        try:
            if not package_id:
                raise ValueError("O package_id não pode ser vazio.")

            package_id = package_id.strip()
            logger.debug(f"Executando package_show para: '{package_id}'")
            package = self.ckan.action.package_show(id=package_id)
            return package

        except ValueError as ve:
            logger.error(f"❌ Erro de validação: {ve}")
            raise
        except Exception as e:
            logger.error(f"❌ Erro de validação: {e}")
            raise

    async def get_package_resources(self, package_id: str) -> List[Dict]:
        """
        Lista todos os resources (arquivos) de um package.

        Args:
            package_id: ID ou nome do package

        Returns:
            Lista de resources com metadados
        """
        try:
            package = await self.get_package_details(package_id)
            resources = package.get('resources', [])
            return resources

        except Exception as e:
            logger.error(f"❌ Erro ao buscar resources: {e}")
            raise

    async def get_resource_data(self, resource_id: str) -> Dict:
        """
        Busca detalhes de um resource (arquivo/URL) específico.
        Args:
            resource_id: ID do resource
        Returns:
            Dicionário com metadados do resource
        """
        try:
            resource = self.ckan.action.resource_show(id=resource_id)
            logger.debug(f"✅ Resource '{resource_id}' carregado")
            return resource
        except Exception as e:
            logger.error(f"Erro ao carregar resource '{resource_id}': {e}")
            raise

    async def get_package_download_urls(self, package_id: str) -> List[Dict]:
        """
        Lista todas as URLs de download de um package.

        Args:
            package_id: ID ou nome do package

        Returns:
            Lista com URLs, nomes e metadados dos arquivos
        """
        try:
            resources = await self.get_package_resources(package_id)
            urls = []
            for resource in resources:
                urls.append({
                    'name': resource.get('name', 'Sem nome'),
                    'state': resource.get('state', ''),
                    'url': resource.get('url', ''),
                    'format': resource.get('format', 'unknown').upper(),
                    'created': resource.get('created', ''),
                    'description': resource.get('description', ''),
                    'resource_id': resource.get('id', ''),
                    'package_id': resource.get('package_id', ''),
                    'mimetype': resource.get('mimetype', '')
                })
            return urls

        except Exception as e:
            logger.error(f"❌ Erro ao extrair URLs: {e}", exc_info=True)
            raise
