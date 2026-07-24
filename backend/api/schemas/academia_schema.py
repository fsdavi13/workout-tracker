from datetime import date

from pydantic import BaseModel, Field


class ExercicioEntrada(BaseModel):
    nome: str
    grupo_muscular: str


class ExercicioResposta(ExercicioEntrada):
    id: int


class SerieEntrada(BaseModel):
    exercicio_id: int
    data: date
    peso: float = Field(ge=0)
    repeticoes: int = Field(gt=0)
    observacoes: str | None = None


class SerieResposta(SerieEntrada):
    id: int
    volume: float


class DivisaoEntrada(BaseModel):
    nome: str = Field(min_length=1, max_length=50)
    descricao: str | None = Field(
        default=None,
        max_length=150,
    )


class ExercicioDivisaoEntrada(BaseModel):
    exercicio_id: int = Field(gt=0)


class ExercicioDivisaoResposta(BaseModel):
    id: int
    exercicio_id: int
    nome: str
    grupo_muscular: str
    ordem: int


class DivisaoResposta(DivisaoEntrada):
    id: int


class DivisaoDetalhadaResposta(DivisaoResposta):
    exercicios: list[ExercicioDivisaoResposta]