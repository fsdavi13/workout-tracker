from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from backend.api.dependencies import obter_corrida_service
from backend.api.schemas.corrida_schema import (
    CorridaEntrada,
    CorridaResposta,
)
from backend.services.corrida_service import CorridaService

router = APIRouter(
    prefix="/corridas",
    tags=["Corridas"],
)

CorridaServiceDependencia = Annotated[
    CorridaService,
    Depends(obter_corrida_service),
]


def converter_corrida(corrida) -> CorridaResposta:
    return CorridaResposta(
        id=corrida.id,
        data=corrida.data,
        distancia_km=corrida.distancia_km,
        pace=corrida.pace,
        pace_segundos=corrida.pace_segundos,
        observacoes=corrida.observacoes,
        tempo_total_segundos=corrida.calcular_tempo_segundos(),
    )


@router.post(
    "",
    response_model=CorridaResposta,
    status_code=status.HTTP_201_CREATED,
)
def registrar_corrida(
    dados: CorridaEntrada,
    service: CorridaServiceDependencia,
):
    try:
        corrida = service.registrar_corrida(
            data=dados.data,
            distancia_km=dados.distancia_km,
            pace=dados.pace,
            observacoes=dados.observacoes,
        )
        return converter_corrida(corrida)
    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(erro),
        ) from erro


@router.get(
    "",
    response_model=list[CorridaResposta],
)
def listar_corridas(
    service: CorridaServiceDependencia,
):
    corridas = service.listar_corridas()
    return [converter_corrida(corrida) for corrida in corridas]


@router.get(
    "/{corrida_id}",
    response_model=CorridaResposta,
)
def buscar_corrida(
    corrida_id: int,
    service: CorridaServiceDependencia,
):
    try:
        corrida = service.buscar_corrida_por_id(corrida_id)
        return converter_corrida(corrida)
    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(erro),
        ) from erro


@router.put(
    "/{corrida_id}",
    response_model=CorridaResposta,
)
def atualizar_corrida(
    corrida_id: int,
    dados: CorridaEntrada,
    service: CorridaServiceDependencia,
):
    try:
        corrida = service.atualizar_corrida(
            corrida_id=corrida_id,
            data=dados.data,
            distancia_km=dados.distancia_km,
            pace=dados.pace,
            observacoes=dados.observacoes,
        )
        return converter_corrida(corrida)
    except ValueError as erro:
        mensagem = str(erro)
        codigo = (
            status.HTTP_404_NOT_FOUND
            if mensagem == "Corrida não encontrada."
            else status.HTTP_400_BAD_REQUEST
        )

        raise HTTPException(
            status_code=codigo,
            detail=mensagem,
        ) from erro


@router.delete(
    "/{corrida_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def excluir_corrida(
    corrida_id: int,
    service: CorridaServiceDependencia,
):
    try:
        service.excluir_corrida(corrida_id)
    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(erro),
        ) from erro