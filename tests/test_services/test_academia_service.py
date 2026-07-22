from datetime import date

import pytest

from backend.database.config import DATABASE_PATH
from backend.database.connection import inicializar_banco
from backend.services.academia_service import AcademiaService


def test_cadastrar_exercicio():

    service = AcademiaService()

    exercicio = service.cadastrar_exercicio(
        "Supino Reto",
        "Peito"
    )

    assert exercicio.id is not None
    assert exercicio.nome == "Supino Reto"
    assert exercicio.grupo_muscular == "Peito"


def test_nao_cadastrar_exercicio_sem_nome():

    service = AcademiaService()

    with pytest.raises(ValueError):
        service.cadastrar_exercicio(
            "",
            "Peito"
        )


def test_registrar_serie():

    service = AcademiaService()

    exercicio = service.cadastrar_exercicio(
        "Supino Reto",
        "Peito"
    )

    serie = service.registrar_serie(
        exercicio_id=exercicio.id,
        data=date.today(),
        peso=30,
        repeticoes=10,
        observacoes="Boa execução"
    )

    assert serie.id is not None
    assert serie.exercicio_id == exercicio.id
    assert serie.calcular_volume() == 300


def test_nao_registrar_serie_com_repeticoes_invalidas():

    service = AcademiaService()

    exercicio = service.cadastrar_exercicio(
        "Supino Reto",
        "Peito"
    )

    with pytest.raises(ValueError):
        service.registrar_serie(
            exercicio_id=exercicio.id,
            data=date.today(),
            peso=30,
            repeticoes=0
        )


def test_calcular_volume_total_exercicio():

    service = AcademiaService()

    exercicio = service.cadastrar_exercicio(
        "Supino Reto",
        "Peito"
    )

    service.registrar_serie(
        exercicio.id,
        date.today(),
        30,
        10
    )

    service.registrar_serie(
        exercicio.id,
        date.today(),
        30,
        8
    )

    volume_total = service.calcular_volume_total_exercicio(
        exercicio.id
    )

    assert volume_total == 540


def test_buscar_maior_carga():

    service = AcademiaService()

    exercicio = service.cadastrar_exercicio(
        "Agachamento Livre",
        "Pernas"
    )

    service.registrar_serie(
        exercicio.id,
        date.today(),
        60,
        10
    )

    service.registrar_serie(
        exercicio.id,
        date.today(),
        80,
        6
    )

    service.registrar_serie(
        exercicio.id,
        date.today(),
        70,
        8
    )

    maior_carga = service.buscar_maior_carga(
        exercicio.id
    )

    assert maior_carga == 80


def test_buscar_maior_volume_serie():

    service = AcademiaService()

    exercicio = service.cadastrar_exercicio(
        "Leg Press",
        "Pernas"
    )

    service.registrar_serie(
        exercicio.id,
        date.today(),
        100,
        10
    )

    service.registrar_serie(
        exercicio.id,
        date.today(),
        140,
        6
    )

    melhor_serie = service.buscar_maior_volume_serie(
        exercicio.id
    )

    assert melhor_serie.peso == 100
    assert melhor_serie.repeticoes == 10
    assert melhor_serie.calcular_volume() == 1000


def test_calcular_volume_por_data():

    service = AcademiaService()

    supino = service.cadastrar_exercicio(
        "Supino Reto",
        "Peito"
    )

    triceps = service.cadastrar_exercicio(
        "Tríceps Corda",
        "Tríceps"
    )

    data_treino = date.today()

    service.registrar_serie(
        supino.id,
        data_treino,
        30,
        10
    )

    service.registrar_serie(
        triceps.id,
        data_treino,
        20,
        12
    )

    volume = service.calcular_volume_por_data(
        data_treino
    )

    assert volume == 540