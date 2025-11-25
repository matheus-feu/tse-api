import uuid

from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, status
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.repository.log_repository import ETLLogRepository
from app.schemas.etl_schemas import ETLResponse, ETLRequest, ETLLogResponse
from app.services.etl.etl_orchestrator import ETLOrchestrator
from app.services.etl.etl_process_config import PROCESS_CONFIG

router = APIRouter()


@router.get("/etl/logs/{log_id}", response_model=ETLLogResponse)
async def get_status_job(log_id: str, db: AsyncSession = Depends(get_db_session)):
    """
    Consulta o status do job ETL pelo log_id retornado ao iniciar o processo ETL.
    """
    repo = ETLLogRepository(db)
    log = await repo.find_by_id(log_id)

    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Log '{log_id}' não encontrado"
        )

    return ETLLogResponse.from_orm(log)


@router.post("/etl/execute", response_model=ETLResponse)
async def execute_etl(
        request: ETLRequest,
        background_tasks: BackgroundTasks,
        db: AsyncSession = Depends(get_db_session)
):
    """
    Inicia um processo ETL (Extract, Transform, Load) assíncrono, em background, para dados do TSE.

    Este endpoint dispara a execução de um pipeline ETL para ingestão, transformação e carregamento dos dados eleitorais do TSE.
    O tipo de dado processado depende do valor do campo `tipo` enviado na requisição (`candidato`, `partido`, etc).

    - Gera e persiste logs detalhados da execução.
    - O processo roda em segundo plano; a resposta retorna imediatamente com o status e o `log_id` do job.
    - O status e o progresso podem ser acompanhados por endpoints de consulta com o `log_id`.

    **Parâmetros:**
    - **request:** Especificação do ETL (`ano`, `uf`, `tipo`, etc).

    **Retorno:**
    - Indica que o ETL foi iniciado
    - Retorna o `log_id` para consulta do status do job.

    ---
    Exemplos de uso:
    ```
    POST /etl/execute
    {
        "tipo": "candidato",
        "ano": 2024,
        "uf": "SP"
    }
    ```

    """
    log_repo = ETLLogRepository(db)
    process_name = f"etl_{request.tipo}_{request.ano}_{request.uf}"
    log = await log_repo.create_log(process_name=process_name)

    async def run_etl_background_task(log_id: uuid.UUID):
        """Wrapper para executar ETL e fazer cleanup."""
        orchestrator = ETLOrchestrator(db_session=db)
        try:
            process_info = PROCESS_CONFIG.get(request.tipo)
            if not process_info:
                raise ValueError(f"Tipo inválido: {request.tipo}")

            func = getattr(orchestrator, process_info["func"])
            extra_args = process_info.get("extra_args", {})

            result_log_id = await func(
                year=request.ano,
                uf=request.uf,
                log_id=log_id,
                **extra_args
            )
            logger.info(f"✅ ETL concluído: {result_log_id}")
        finally:
            await orchestrator.extractor.close()

    background_tasks.add_task(run_etl_background_task, log.id)

    return ETLResponse(
        status="INICIADO",
        mensagem=f"ETL {request.tipo} iniciado para {request.ano}/{request.uf}",
        log_id=str(log.id),
        detalhes={
            "ano": request.ano,
            "uf": request.uf,
            "tipo": request.tipo,
        }
    )
