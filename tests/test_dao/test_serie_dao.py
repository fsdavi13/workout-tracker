from datetime import date

from backend.dao.exercicio_dao import ExercicioDAO
from backend.dao.serie_dao import SerieDAO
from backend.models.exercicio import Exercicio
from backend.models.serie import Serie


def test_criar_serie():
    exercicio_dao = ExercicioDAO()
    serie_dao = SerieDAO()

    exercicio = Exercicio(
        nome="Supino Reto",
        grupo_muscular="Peito"
    )

    exercicio = exercicio_dao.criar(exercicio)

    serie = Serie(
        exercicio_id=exercicio.id,
        data=date.today(),
        peso=30,
        repeticoes=10,
        observacoes="Boa execução"
    )

    serie_criada = serie_dao.criar(serie)

    assert serie_criada.id is not None
    assert serie_criada.exercicio_id == exercicio.id
    assert serie_criada.peso == 30
    assert serie_criada.repeticoes == 10


def test_buscar_series_por_exercicio():
    exercicio_dao = ExercicioDAO()
    serie_dao = SerieDAO()

    exercicio = Exercicio(
        nome="Agachamento Livre",
        grupo_muscular="Pernas"
    )

    exercicio = exercicio_dao.criar(exercicio)

    serie = Serie(
        exercicio_id=exercicio.id,
        data=date.today(),
        peso=80,
        repeticoes=8
    )

    serie_dao.criar(serie)

    series = serie_dao.buscar_por_exercicio(exercicio.id)

    assert len(series) == 1
    assert series[0].exercicio_id == exercicio.id
    assert series[0].peso == 80
    assert series[0].repeticoes == 8