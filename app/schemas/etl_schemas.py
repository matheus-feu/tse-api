from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator, ConfigDict


class UFEnum(str, Enum):
    """Unidades Federativas do Brasil."""
    AC = "AC"
    AL = "AL"
    AP = "AP"
    AM = "AM"
    BA = "BA"
    CE = "CE"
    DF = "DF"
    ES = "ES"
    GO = "GO"
    MA = "MA"
    MT = "MT"
    MS = "MS"
    MG = "MG"
    PA = "PA"
    PB = "PB"
    PR = "PR"
    PE = "PE"
    PI = "PI"
    RJ = "RJ"
    RN = "RN"
    RS = "RS"
    RO = "RO"
    RR = "RR"
    SC = "SC"
    SP = "SP"
    SE = "SE"
    TO = "TO"


class TipoETLEnum(str, Enum):
    """Tipos de ETL disponíveis."""
    CANDIDATO = "candidato"
    PARTIDO = "partido"


class ETLRequest(BaseModel):
    """Schema para requisição de ETL."""
    ano: int = Field(..., ge=1994, le=datetime.now().year + 1, description="Ano da eleição")
    uf: Optional[UFEnum] = Field(None, description="UF brasileira (ex: SP, RJ)")
    tipo: TipoETLEnum = Field(
        TipoETLEnum.CANDIDATO,
        description="Tipo de ETL: candidato ou partido"
    )

    @field_validator('ano')
    @classmethod
    def validate_election_year(cls, v: int) -> int:
        """Valida se é ano de eleição (par)."""
        if v % 2 != 0:
            raise ValueError(
                f"Ano {v} é inválido. Eleições ocorrem apenas em anos pares."
            )

        VALID_ELECTION_YEARS = {
            1994, 1996, 1998, 2000, 2002, 2004, 2006, 2008,
            2010, 2012, 2014, 2016, 2018, 2020, 2022, 2024, 2026
        }

        if v not in VALID_ELECTION_YEARS:
            raise ValueError(
                f"Ano {v} não possui dados disponíveis no TSE. "
                f"Anos válidos: {sorted(VALID_ELECTION_YEARS)}"
            )

        return v


class ETLResponse(BaseModel):
    """Response de ETL."""
    status: str
    mensagem: str
    log_id: str
    detalhes: Optional[dict] = None


class ETLLogResponse(BaseModel):
    """Schema de resposta para log de ETL."""

    id: UUID
    process_name: str
    status: str
    inicio: Optional[str] = None
    fim: Optional[str] = None
    duracao: Optional[str] = None
    registros_processados: int = 0
    erro: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

    @staticmethod
    def format_datetime(dt: Optional[datetime]) -> Optional[str]:
        """Formata datetime para padrão brasileiro."""
        if not dt:
            return None
        return dt.strftime("%d/%m/%Y às %H:%M:%S")

    @staticmethod
    def calculate_duration(start: Optional[datetime], end: Optional[datetime]) -> Optional[str]:
        """Calcula duração formatada."""
        if not start or not end:
            return None

        delta = end - start
        total_seconds = int(delta.total_seconds())

        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        if hours > 0:
            return f"{hours}h {minutes}min {seconds}s"
        elif minutes > 0:
            return f"{minutes}min {seconds}s"
        else:
            return f"{seconds}s"
