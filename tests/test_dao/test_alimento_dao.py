from dao.alimento_dao import AlimentoDAO
from models.alimento import Alimento


def test_criar_alimento():
    alimento_dao = AlimentoDAO()

    alimento = Alimento(
        nome="Banana",
        calorias_por_100g=89,
        proteinas_g=1.1,
        carboidratos_g=22.8,
        gorduras_g=0.3,
        categoria="Frutas",
        fonte="Teste"
    )

    alimento_criado = alimento_dao.criar(alimento)

    assert alimento_criado.id is not None
    assert alimento_criado.nome == "Banana"
    assert alimento_criado.calorias_por_100g == 89
    assert alimento_criado.fonte == "Teste"


def test_buscar_alimentos():
    alimento_dao = AlimentoDAO()

    alimento = Alimento(
        nome="Arroz",
        calorias_por_100g=128,
        proteinas_g=2.5,
        carboidratos_g=28.1,
        gorduras_g=0.2,
        categoria="Cereais e derivados",
        fonte="Teste"
    )

    alimento_dao.criar(alimento)

    alimentos = alimento_dao.buscar_todos()

    assert len(alimentos) == 1
    assert alimentos[0].nome == "Arroz"
    assert alimentos[0].categoria == "Cereais e derivados"