from datetime import date

from dao.corrida_dao import CorridaDAO
from models.corrida import Corrida


def test_criar_corrida():
    corrida_dao = CorridaDAO()

    corrida = Corrida(
        data=date.today(),
        distancia_km=5,
        pace="06:00"
    )

    corrida_criada = corrida_dao.criar(corrida)

    assert corrida_criada.id is not None
    assert corrida_criada.distancia_km == 5
    assert corrida_criada.pace == "06:00"


def test_buscar_corridas():
    corrida_dao = CorridaDAO()

    corrida = Corrida(
        data=date.today(),
        distancia_km=3,
        pace="07:00"
    )

    corrida_dao.criar(corrida)

    corridas = corrida_dao.buscar_todas()

    assert len(corridas) == 1
    assert corridas[0].distancia_km == 3
    assert corridas[0].pace == "07:00"