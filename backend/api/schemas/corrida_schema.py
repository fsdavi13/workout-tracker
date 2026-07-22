from datetime import date

from pydantic import BaseModel, Field


class CorridaEntrada(BaseModel):
    data: date
    distancia_km: float = Field(gt=0)
    pace: str
    observacoes: str | None = None


class CorridaResposta(CorridaEntrada):
    id: int
    pace_segundos: int
    tempo_total_segundos: int