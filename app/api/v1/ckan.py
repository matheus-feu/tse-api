from typing import Optional

from fastapi import APIRouter, HTTPException, Path, Query, status
from loguru import logger

from app.services.ckan.ckan_client import CKANTSEClient

router = APIRouter(prefix="/ckan")

client = CKANTSEClient()


@router.get("/packages", summary="Listar todos os packages")
async def list_all_packages():
    """
    Lista todos os packages (datasets) disponíveis no CKAN do TSE.

    Retorna uma lista com os IDs de todos os datasets publicados.
    """
    try:
        packages = await client.list_all_packages()

        return {
            "success": True,
            "total": len(packages),
            "packages": packages
        }
    except Exception as e:
        logger.error(f"❌ Erro ao listar packages: {e}")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Erro ao listar packages: {str(e)}")


@router.get("/packages/{package_id}", summary="Detalhes de um package")
async def get_package_details(
        package_id: str = Path(..., description="ID ou nome do package")
):
    """
    Retorna detalhes completos de um package específico.

    Inclui metadados, recursos (arquivos), tags, e informações da organização.

    - **package_id**: ID ou nome do package (ex: 'votacao-candidato-munzona-2024')
    """
    try:
        logger.info(f"🔍 Buscando package '{package_id}'")
        package = await client.get_package_details(package_id)

        return {
            "success": True,
            "package": package
        }
    except Exception as e:
        logger.error(f"❌ Erro ao buscar package '{package_id}': {e}")
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Package não encontrado: {str(e)}")


@router.get("/resources/{resource_id}", summary="Detalhes de um resource")
async def get_resource_details(resource_id: str = Path(..., description="ID do resource (arquivo)")):
    """
    Retorna detalhes de um resource (arquivo/URL) específico.

    Inclui URL de download, formato, tamanho, e metadados.

    - **resource_id**: ID único do resource
    """
    try:
        resource = await client.get_resource_data(resource_id)

        return {
            "success": True,
            "resource": resource
        }
    except Exception as e:
        logger.error(f"❌ Erro ao buscar resource '{resource_id}': {e}")
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Resource não encontrado: {str(e)}")


@router.get("/packages/{package_id}/urls", summary="URLs de download de um package")
async def get_package_urls(package_id: str = Path(...)):
    """
    Lista todas as URLs de download de um package específico.

    Retorna nome, URL, formato, tamanho e metadados de cada arquivo.
    """
    try:
        urls = await client.get_package_download_urls(package_id)

        return {
            "success": True,
            "package_id": package_id,
            "total_files": len(urls),
            "urls": urls
        }
    except Exception as e:
        logger.error(f"❌ Erro: {e}")
        raise HTTPException(404, str(e))
