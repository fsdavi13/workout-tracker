from backend.dao.alimento_dao import AlimentoDAO
from backend.models.alimento import Alimento


def criar_alimento_teste(nome="Banana"):
    return Alimento(
        nome=nome,
        calorias_por_100g=89,
        proteinas_g=1.1,
        carboidratos_g=22.8,
        gorduras_g=0.3,
        categoria="Frutas",
        fonte="Teste"
    )


def test_criar_alimento():
    alimento_dao = AlimentoDAO()

    alimento = criar_alimento_teste()

    alimento_criado = alimento_dao.criar(alimento)

    assert alimento_criado.id is not None
    assert alimento_criado.nome == "Banana"
    assert alimento_criado.calorias_por_100g == 89
    assert alimento_criado.fonte == "Teste"


def test_buscar_todos_alimentos():
    alimento_dao = AlimentoDAO()

    alimento = criar_alimento_teste(nome="Arroz")
    alimento.categoria = "Cereais e derivados"
    alimento.fonte = "TACO"

    alimento_criado = alimento_dao.criar(alimento)

    alimentos = alimento_dao.buscar_todos()

    assert len(alimentos) == 1
    assert alimentos[0].id == alimento_criado.id
    assert alimentos[0].nome == "Arroz"
    assert alimentos[0].categoria == "Cereais e derivados"
    assert alimentos[0].fonte == "TACO"


def test_buscar_alimento_por_id():
    alimento_dao = AlimentoDAO()

    alimento_criado = alimento_dao.criar(
        criar_alimento_teste()
    )

    alimento_encontrado = alimento_dao.buscar_por_id(
        alimento_criado.id
    )

    assert alimento_encontrado is not None
    assert alimento_encontrado.id == alimento_criado.id
    assert alimento_encontrado.nome == "Banana"
    assert alimento_encontrado.fonte == "Teste"


def test_buscar_alimento_por_nome():
    alimento_dao = AlimentoDAO()

    alimento_dao.criar(
        criar_alimento_teste(nome="Banana-prata")
    )

    alimento_dao.criar(
        criar_alimento_teste(nome="Maçã")
    )

    alimentos = alimento_dao.buscar_por_nome("banana")

    assert len(alimentos) == 1
    assert alimentos[0].id is not None
    assert alimentos[0].nome == "Banana-prata"
    assert alimentos[0].fonte == "Teste"


def test_atualizar_alimento():
    alimento_dao = AlimentoDAO()

    alimento = alimento_dao.criar(
        criar_alimento_teste()
    )

    alimento.nome = "Banana madura"
    alimento.calorias_por_100g = 92
    alimento.fonte = "Cadastro manual"

    alimento_dao.atualizar(alimento)

    alimento_atualizado = alimento_dao.buscar_por_id(
        alimento.id
    )

    assert alimento_atualizado.nome == "Banana madura"
    assert alimento_atualizado.calorias_por_100g == 92
    assert alimento_atualizado.fonte == "Cadastro manual"


def test_deletar_alimento():
    alimento_dao = AlimentoDAO()

    alimento = alimento_dao.criar(
        criar_alimento_teste()
    )

    alimento_dao.deletar(alimento.id)

    assert alimento_dao.buscar_por_id(alimento.id) is None