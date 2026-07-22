from datetime import date

from backend.dao.alimento_dao import AlimentoDAO
from backend.dao.registro_alimentar_dao import RegistroAlimentarDAO
from backend.models.alimento import Alimento
from backend.models.registro_alimentar import RegistroAlimentar


def criar_alimento_teste(nome="Frango"):
    return Alimento(
        nome=nome,
        calorias_por_100g=165,
        proteinas_g=31,
        carboidratos_g=0,
        gorduras_g=3.6,
        categoria="Carnes",
        fonte="Teste"
    )


def test_criar_registro_alimentar():
    alimento_dao = AlimentoDAO()
    registro_dao = RegistroAlimentarDAO()

    alimento = alimento_dao.criar(
        criar_alimento_teste()
    )

    registro = RegistroAlimentar(
        alimento_id=alimento.id,
        data=date.today(),
        tipo_refeicao="Almoço",
        quantidade_gramas=200
    )

    registro_criado = registro_dao.criar(registro)

    assert registro_criado.id is not None
    assert registro_criado.alimento_id == alimento.id
    assert registro_criado.quantidade_gramas == 200
    assert registro_criado.tipo_refeicao == "Almoço"
    assert registro_criado.refeicao == "Almoço"


def test_buscar_registro_por_id():
    alimento_dao = AlimentoDAO()
    registro_dao = RegistroAlimentarDAO()

    alimento = alimento_dao.criar(
        criar_alimento_teste()
    )

    registro_criado = registro_dao.criar(
        RegistroAlimentar(
            alimento_id=alimento.id,
            data=date.today(),
            tipo_refeicao="Jantar",
            quantidade_gramas=180
        )
    )

    registro_encontrado = registro_dao.buscar_por_id(
        registro_criado.id
    )

    assert registro_encontrado is not None
    assert registro_encontrado.id == registro_criado.id
    assert registro_encontrado.alimento_id == alimento.id
    assert registro_encontrado.data == date.today()
    assert registro_encontrado.quantidade_gramas == 180
    assert registro_encontrado.tipo_refeicao == "Jantar"
    assert registro_encontrado.refeicao == "Jantar"


def test_buscar_por_data():
    alimento_dao = AlimentoDAO()
    registro_dao = RegistroAlimentarDAO()

    alimento = alimento_dao.criar(
        criar_alimento_teste(nome="Arroz")
    )

    data_registro = date.today()

    registro_criado = registro_dao.criar(
        RegistroAlimentar(
            alimento_id=alimento.id,
            data=data_registro,
            tipo_refeicao="Almoço",
            quantidade_gramas=150
        )
    )

    registros = registro_dao.buscar_por_data(data_registro)

    assert len(registros) == 1
    assert registros[0].id == registro_criado.id
    assert registros[0].alimento_id == alimento.id
    assert registros[0].quantidade_gramas == 150
    assert registros[0].tipo_refeicao == "Almoço"


def test_atualizar_registro_alimentar():
    alimento_dao = AlimentoDAO()
    registro_dao = RegistroAlimentarDAO()

    alimento = alimento_dao.criar(
        criar_alimento_teste()
    )

    registro = registro_dao.criar(
        RegistroAlimentar(
            alimento_id=alimento.id,
            data=date.today(),
            tipo_refeicao="Almoço",
            quantidade_gramas=200
        )
    )

    registro.quantidade_gramas = 250
    registro.tipo_refeicao = "Jantar"
    registro.refeicao = "Jantar"

    registro_dao.atualizar(registro)

    registro_atualizado = registro_dao.buscar_por_id(
        registro.id
    )

    assert registro_atualizado.quantidade_gramas == 250
    assert registro_atualizado.tipo_refeicao == "Jantar"


def test_deletar_registro_alimentar():
    alimento_dao = AlimentoDAO()
    registro_dao = RegistroAlimentarDAO()

    alimento = alimento_dao.criar(
        criar_alimento_teste()
    )

    registro = registro_dao.criar(
        RegistroAlimentar(
            alimento_id=alimento.id,
            data=date.today(),
            tipo_refeicao="Lanche",
            quantidade_gramas=100
        )
    )

    registro_dao.deletar(registro.id)

    assert registro_dao.buscar_por_id(registro.id) is None