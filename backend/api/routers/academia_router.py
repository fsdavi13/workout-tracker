from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from backend.api.dependencies import obter_academia_service
from backend.api.schemas.academia_schema import (
    ExercicioEntrada,
    ExercicioResposta,
    SerieEntrada,
    SerieResposta,
)
from backend.services.academia_service import AcademiaService

router = APIRouter(
    prefix="/academia",
    tags=["Academia"],
)

AcademiaServiceDependencia = Annotated[
    AcademiaService,
    Depends(obter_academia_service),
]


def converter_exercicio(exercicio) -> ExercicioResposta:
    return ExercicioResposta(
        id=exercicio.id,
        nome=exercicio.nome,
        grupo_muscular=exercicio.grupo_muscular,
    )


def converter_serie(serie) -> SerieResposta:
    return SerieResposta(
        id=serie.id,
        exercicio_id=serie.exercicio_id,
        data=serie.data,
        peso=serie.peso,
        repeticoes=serie.repeticoes,
        observacoes=serie.observacoes,
        volume=serie.calcular_volume(),
    )


@router.post(
    "/exercicios",
    response_model=ExercicioResposta,
    status_code=status.HTTP_201_CREATED,
)
def cadastrar_exercicio(
    dados: ExercicioEntrada,
    service: AcademiaServiceDependencia,
):
    try:
        exercicio = service.cadastrar_exercicio(
            nome=dados.nome,
            grupo_muscular=dados.grupo_muscular,
        )
        return converter_exercicio(exercicio)
    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(erro),
        ) from erro


@router.get(
    "/exercicios",
    response_model=list[ExercicioResposta],
)
def listar_exercicios(
    service: AcademiaServiceDependencia,
):
    exercicios = service.listar_exercicios()

    return [
        converter_exercicio(exercicio)
        for exercicio in exercicios
    ]


@router.get(
    "/exercicios/{exercicio_id}",
    response_model=ExercicioResposta,
)
def buscar_exercicio(
    exercicio_id: int,
    service: AcademiaServiceDependencia,
):
    try:
        exercicio = service.buscar_exercicio_por_id(exercicio_id)
        return converter_exercicio(exercicio)
    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(erro),
        ) from erro


@router.put(
    "/exercicios/{exercicio_id}",
    response_model=ExercicioResposta,
)
def atualizar_exercicio(
    exercicio_id: int,
    dados: ExercicioEntrada,
    service: AcademiaServiceDependencia,
):
    try:
        exercicio = service.atualizar_exercicio(
            exercicio_id=exercicio_id,
            nome=dados.nome,
            grupo_muscular=dados.grupo_muscular,
        )
        return converter_exercicio(exercicio)
    except ValueError as erro:
        mensagem = str(erro)

        codigo = (
            status.HTTP_404_NOT_FOUND
            if mensagem == "Exercício não encontrado."
            else status.HTTP_400_BAD_REQUEST
        )

        raise HTTPException(
            status_code=codigo,
            detail=mensagem,
        ) from erro


@router.delete(
    "/exercicios/{exercicio_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def excluir_exercicio(
    exercicio_id: int,
    service: AcademiaServiceDependencia,
):
    try:
        service.excluir_exercicio(exercicio_id)
    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(erro),
        ) from erro


@router.post(
    "/series",
    response_model=SerieResposta,
    status_code=status.HTTP_201_CREATED,
)
def registrar_serie(
    dados: SerieEntrada,
    service: AcademiaServiceDependencia,
):
    try:
        serie = service.registrar_serie(
            exercicio_id=dados.exercicio_id,
            data=dados.data,
            peso=dados.peso,
            repeticoes=dados.repeticoes,
            observacoes=dados.observacoes,
        )
        return converter_serie(serie)
    except ValueError as erro:
        mensagem = str(erro)

        codigo = (
            status.HTTP_404_NOT_FOUND
            if mensagem == "Exercício não encontrado."
            else status.HTTP_400_BAD_REQUEST
        )

        raise HTTPException(
            status_code=codigo,
            detail=mensagem,
        ) from erro


@router.get(
    "/series",
    response_model=list[SerieResposta],
)
def listar_series(
    service: AcademiaServiceDependencia,
):
    series = service.listar_series()

    return [
        converter_serie(serie)
        for serie in series
    ]


@router.get(
    "/exercicios/{exercicio_id}/series",
    response_model=list[SerieResposta],
)
def listar_series_por_exercicio(
    exercicio_id: int,
    service: AcademiaServiceDependencia,
):
    try:
        series = service.buscar_series_por_exercicio(exercicio_id)

        return [
            converter_serie(serie)
            for serie in series
        ]
    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(erro),
        ) from erro


@router.delete(
    "/series/{serie_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def excluir_serie(
    serie_id: int,
    service: AcademiaServiceDependencia,
):
    try:
        service.excluir_serie(serie_id)
    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(erro),
        ) from erro