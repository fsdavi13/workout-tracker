from dao.exercicio_dao import ExercicioDAO
from models.exercicio import Exercicio


def test_criar_exercicio():
    exercicio_dao = ExercicioDAO()

    exercicio = Exercicio(
        nome="Supino Reto",
        grupo_muscular="Peito"
    )

    exercicio_criado = exercicio_dao.criar(exercicio)

    assert exercicio_criado.id is not None
    assert exercicio_criado.nome == "Supino Reto"
    assert exercicio_criado.grupo_muscular == "Peito"


def test_buscar_exercicios():
    exercicio_dao = ExercicioDAO()

    exercicio = Exercicio(
        nome="Agachamento Livre",
        grupo_muscular="Pernas"
    )

    exercicio_dao.criar(exercicio)

    exercicios = exercicio_dao.buscar_todos()

    assert len(exercicios) == 1
    assert exercicios[0].nome == "Agachamento Livre"
    assert exercicios[0].grupo_muscular == "Pernas"