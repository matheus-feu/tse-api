import uuid

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class ETLLog(Base):
    """Modelo de banco de dados para logs de processos ETL (Extract, Transform, Load)."""

    __tablename__ = "etl_log"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    process_name = Column(String(100), nullable=False, index=True)
    status = Column(String(50), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)

    records_processed = Column(Integer, nullable=True)
    error_message = Column(String(500), nullable=True)

    def __repr__(self):
        return f"<ETLLog(process_name={self.process_name}, status={self.status}, start_time={self.start_time}, end_time={self.end_time})>"

    def to_dict(self):
        return {
            "id": str(self.id),
            "process_name": self.process_name,
            "status": self.status,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "records_processed": self.records_processed,
            "error_message": self.error_message,
        }
