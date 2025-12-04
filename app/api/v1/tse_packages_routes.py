from uuid import UUID

from fastapi import APIRouter, Depends, BackgroundTasks, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.repository.log_repository import ETLLogRepository
from app.schemas.etl_schemas import ETLResponse
from app.schemas.tse_package_schemas import TSEPackageCreate
from app.services.etl.orchestrators.packages_orchestrator import PackageOrchestrator

router = APIRouter(prefix="/etl/tse-packages")


@router.post(
    "/ingest",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=ETLResponse,
    summary="Ingestão de pacote TSE (RAW)",
)
async def ingest_tse_raw(
        payload: TSEPackageCreate,
        background_tasks: BackgroundTasks,
        db_session: AsyncSession = Depends(get_db_session),
):
    """
    Dispara a ingestão de um pacote TSE (ZIP) em background.

    Este endpoint:
    - Baixa o arquivo ZIP informado em `url`
    - Lê o primeiro CSV encontrado dentro do ZIP
    - Insere TODAS as linhas do CSV na tabela `tse_packages`, em formato genérico (`raw_data` JSON)
    - Registra o processo em um log de ETL e devolve o `log_id` para acompanhamento

    A operação de ingestão roda em segundo plano; esta rota retorna imediatamente.

    Corpo da requisição (JSON):
    - url: URL HTTPS do pacote ZIP do TSE
    - package_type: identificador lógico do tipo de pacote (ex: "votacao_candidato_munzona")
    """

    etl_repo = ETLLogRepository(db_session)
    log = await etl_repo.create_log(
        process_name=f"tse_raw_ingest:{payload.dataset}"
    )

    async def _run(url: str, package_type: str, log_id: UUID):
        orchestrator = PackageOrchestrator(db_session=db_session, log_id=log_id)
        await orchestrator.run(url=url, package_type=package_type)

    background_tasks.add_task(
        _run,
        str(payload.url),
        payload.package_type,
        log.id,
    )

    return ETLResponse(
        status="accepted",
        mensagem="Ingest RAW iniciado",
        log_id=str(log.id),
        detalhes={
            "dataset": payload.dataset,
            "source_url": str(payload.url),
        }
    )
