from datetime import date

from pydantic import BaseModel, Field


class AlimentoResposta(BaseModel):
    id: int
    nome: str
    calorias_por_100g: float | None
    proteinas_g: float | None
    carboidratos_g: float | None
    gorduras_g: float | None
    categoria: str
    fonte: str | None = None


class ItemDietaEntrada(BaseModel):
    alimento_id: int = Field(gt=0)
    quantidade_gramas: float = Field(gt=0)


class DietaEntrada(BaseModel):
    itens: list[ItemDietaEntrada]
    data: date | None = None
    tipo_refeicao: str = "Dieta"


class MacrosAlimentoResposta(BaseModel):
    alimento_id: int
    nome: str
    quantidade_gramas: float
    calorias: float
    proteinas_g: float
    carboidratos_g: float
    gorduras_g: float


class ItemDietaResposta(MacrosAlimentoResposta):
    registro_id: int


class TotaisNutricionaisResposta(BaseModel):
    calorias: float
    proteinas_g: float
    carboidratos_g: float
    gorduras_g: float


class DietaResposta(BaseModel):
    data: date
    tipo_refeicao: str
    itens: list[ItemDietaResposta]
    totais: TotaisNutricionaisResposta


class RegistroAlimentarResposta(BaseModel):
    id: int
    alimento_id: int
    data: date
    quantidade_gramas: float
    tipo_refeicao: str