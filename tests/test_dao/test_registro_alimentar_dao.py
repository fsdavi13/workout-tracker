from datetime import date

from dao.alimento_dao import AlimentoDAO
from dao.registro_alimentar_dao import RegistroAlimentarDAO
from models.alimento import Alimento
from models.registro_alimentar import RegistroAlimentar


def test_criar_registro_alimentar():
    alimento_dao = AlimentoDAO()
    registro_dao = RegistroAlimentarDAO()

    alimento = Alimento(
        nome="Frango",
        calorias_por_100g=165,
        proteinas_g=31,
        carboidratos_g=0,
        gorduras_g=3.6,
        categoria="Carnes",
        fonte="Teste"
    )

    alimento = alimento_dao.criar(alimento)

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


def test_buscar_por_data():
    alimento_dao = AlimentoDAO()
    registro_dao = RegistroAlimentarDAO()

    alimento = Alimento(
        nome="Arroz",
        calorias_por_100g=128,
        proteinas_g=2.5,
        carboidratos_g=28.1,
        gorduras_g=0.2,
        categoria="Cereais e derivados",
        fonte="Teste"
    )

    alimento = alimento_dao.criar(alimento)

    data_registro = date.today()

    registro = RegistroAlimentar(
        alimento_id=alimento.id,
        data=data_registro,
        tipo_refeicao="Almoço",
        quantidade_gramas=150
    )

    registro_dao.criar(registro)

    registros = registro_dao.buscar_por_data(data_registro)

    assert len(registros) == 1
    assert registros[0].alimento_id == alimento.id
    assert registros[0].quantidade_gramas == 150