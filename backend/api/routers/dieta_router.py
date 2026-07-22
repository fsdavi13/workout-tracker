from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from backend.api.dependencies import obter_dieta_service
from backend.api.schemas.dieta_schema import (
    AlimentoResposta,
    DietaEntrada,
    DietaResposta,
    MacrosAlimentoResposta,
    RegistroAlimentarResposta,
)
from backend.services.dieta_service import DietaService

router = APIRouter(
    prefix="/dieta",
    tags=["Dieta"],
)

DietaServiceDependencia = Annotated[
    DietaService,
    Depends(obter_dieta_service),
]


def converter_alimento(alimento) -> AlimentoResposta:
    return AlimentoResposta(
        id=alimento.id,
        nome=alimento.nome,
        calorias_por_100g=alimento.calorias_por_100g,
        proteinas_g=alimento.proteinas_g,
        carboidratos_g=alimento.carboidratos_g,
        gorduras_g=alimento.gorduras_g,
        categoria=alimento.categoria,
        fonte=alimento.fonte,
    )


def converter_registro(registro) -> RegistroAlimentarResposta:
    return RegistroAlimentarResposta(
        id=registro.id,
        alimento_id=registro.alimento_id,
        data=registro.data,
        quantidade_gramas=registro.quantidade_gramas,
        tipo_refeicao=registro.tipo_refeicao,
    )


@router.get(
    "/alimentos",
    response_model=list[AlimentoResposta],
)
def buscar_alimentos(
    service: DietaServiceDependencia,
    termo: str = Query(min_length=1),
):
    try:
        alimentos = service.buscar_alimentos_por_nome(termo)
        return [converter_alimento(alimento) for alimento in alimentos]
    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(erro),
        ) from erro


@router.get(
    "/alimentos/{alimento_id}",
    response_model=AlimentoResposta,
)
def buscar_alimento(
    alimento_id: int,
    service: DietaServiceDependencia,
):
    try:
        alimento = service.buscar_alimento_por_id(alimento_id)
        return converter_alimento(alimento)
    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(erro),
        ) from erro


@router.get(
    "/alimentos/{alimento_id}/macros",
    response_model=MacrosAlimentoResposta,
)
def calcular_macros(
    alimento_id: int,
    service: DietaServiceDependencia,
    quantidade_gramas: float = Query(gt=0),
):
    try:
        return service.calcular_macros_alimento(
            alimento_id=alimento_id,
            quantidade_gramas=quantidade_gramas,
        )
    except ValueError as erro:
        mensagem = str(erro)

        codigo = (
            status.HTTP_404_NOT_FOUND
            if mensagem == "Alimento não encontrado."
            else status.HTTP_400_BAD_REQUEST
        )

        raise HTTPException(
            status_code=codigo,
            detail=mensagem,
        ) from erro


@router.post(
    "",
    response_model=DietaResposta,
    status_code=status.HTTP_201_CREATED,
)
def salvar_dieta(
    dados: DietaEntrada,
    service: DietaServiceDependencia,
):
    try:
        itens = [
            {
                "alimento_id": item.alimento_id,
                "quantidade_gramas": item.quantidade_gramas,
            }
            for item in dados.itens
        ]

        return service.salvar_dieta(
            itens=itens,
            data_registro=dados.data,
            tipo_refeicao=dados.tipo_refeicao,
        )
    except ValueError as erro:
        mensagem = str(erro)

        codigo = (
            status.HTTP_404_NOT_FOUND
            if mensagem == "Alimento não encontrado."
            else status.HTTP_400_BAD_REQUEST
        )

        raise HTTPException(
            status_code=codigo,
            detail=mensagem,
        ) from erro


@router.get(
    "/registros",
    response_model=list[RegistroAlimentarResposta],
)
def listar_registros(
    service: DietaServiceDependencia,
):
    registros = service.listar_registros()

    return [
        converter_registro(registro)
        for registro in registros
    ]


@router.get(
    "/registros/por-data",
    response_model=list[RegistroAlimentarResposta],
)
def buscar_registros_por_data(
    service: DietaServiceDependencia,
    data_registro: date = Query(alias="data"),
):
    registros = service.buscar_registros_por_data(data_registro)

    return [
        converter_registro(registro)
        for registro in registros
    ]


@router.delete(
    "/registros/{registro_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def excluir_registro(
    registro_id: int,
    service: DietaServiceDependencia,
):
    try:
        service.excluir_registro(registro_id)
    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(erro),
        ) from erro