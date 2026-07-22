from datetime import date

import pytest

from backend.dao.alimento_dao import AlimentoDAO
from backend.models.alimento import Alimento
from backend.services.dieta_service import DietaService


def criar_alimento(
    nome,
    calorias,
    proteinas,
    carboidratos,
    gorduras
):
    alimento_dao = AlimentoDAO()

    alimento = Alimento(
        nome=nome,
        calorias_por_100g=calorias,
        proteinas_g=proteinas,
        carboidratos_g=carboidratos,
        gorduras_g=gorduras,
        categoria="Teste",
        fonte="Teste"
    )

    return alimento_dao.criar(alimento)


def test_buscar_alimentos_por_nome():
    criar_alimento(
        nome="Banana-prata",
        calorias=98,
        proteinas=1.3,
        carboidratos=26,
        gorduras=0.1
    )

    criar_alimento(
        nome="Arroz integral",
        calorias=124,
        proteinas=2.6,
        carboidratos=25.8,
        gorduras=1
    )

    service = DietaService()

    resultados = service.buscar_alimentos_por_nome(
        "banana"
    )

    assert len(resultados) == 1
    assert resultados[0].nome == "Banana-prata"


def test_buscar_alimentos_com_termo_vazio():
    service = DietaService()

    assert service.buscar_alimentos_por_nome("   ") == []


def test_buscar_alimentos_com_termo_invalido():
    service = DietaService()

    with pytest.raises(
        ValueError,
        match="O termo de busca deve ser um texto."
    ):
        service.buscar_alimentos_por_nome(123)


def test_calcular_macros_alimento():
    alimento = criar_alimento(
        nome="Banana",
        calorias=90,
        proteinas=1,
        carboidratos=23,
        gorduras=0.3
    )

    service = DietaService()

    resultado = service.calcular_macros_alimento(
        alimento_id=alimento.id,
        quantidade_gramas=150
    )

    assert resultado["alimento_id"] == alimento.id
    assert resultado["nome"] == "Banana"
    assert resultado["quantidade_gramas"] == 150
    assert resultado["calorias"] == 135
    assert resultado["proteinas_g"] == 1.5
    assert resultado["carboidratos_g"] == 34.5
    assert resultado["gorduras_g"] == 0.45


def test_calcular_macros_com_quantidade_invalida():
    alimento = criar_alimento(
        nome="Banana",
        calorias=90,
        proteinas=1,
        carboidratos=23,
        gorduras=0.3
    )

    service = DietaService()

    with pytest.raises(
        ValueError,
        match=(
            "A quantidade em gramas deve ser maior que zero."
        )
    ):
        service.calcular_macros_alimento(
            alimento_id=alimento.id,
            quantidade_gramas=0
        )


def test_calcular_macros_de_alimento_inexistente():
    service = DietaService()

    with pytest.raises(
        ValueError,
        match="Alimento não encontrado."
    ):
        service.calcular_macros_alimento(
            alimento_id=999,
            quantidade_gramas=100
        )


def test_salvar_dieta():
    frango = criar_alimento(
        nome="Frango grelhado",
        calorias=165,
        proteinas=31,
        carboidratos=0,
        gorduras=3.6
    )

    arroz = criar_alimento(
        nome="Arroz cozido",
        calorias=130,
        proteinas=2.7,
        carboidratos=28,
        gorduras=0.3
    )

    service = DietaService()

    relatorio = service.salvar_dieta(
        itens=[
            {
                "alimento_id": frango.id,
                "quantidade_gramas": 200
            },
            {
                "alimento_id": arroz.id,
                "quantidade_gramas": 150
            }
        ],
        data_registro=date.today(),
        tipo_refeicao="Almoço"
    )

    assert relatorio["data"] == date.today()
    assert relatorio["tipo_refeicao"] == "Almoço"
    assert len(relatorio["itens"]) == 2

    assert relatorio["itens"][0]["registro_id"] is not None
    assert relatorio["itens"][1]["registro_id"] is not None

    assert relatorio["totais"]["calorias"] == 525
    assert relatorio["totais"]["proteinas_g"] == 66.05
    assert relatorio["totais"]["carboidratos_g"] == 42
    assert relatorio["totais"]["gorduras_g"] == 7.65


def test_salvar_dieta_com_data_atual_por_padrao():
    banana = criar_alimento(
        nome="Banana",
        calorias=90,
        proteinas=1,
        carboidratos=23,
        gorduras=0.3
    )

    service = DietaService()

    relatorio = service.salvar_dieta(
        itens=[
            {
                "alimento_id": banana.id,
                "quantidade_gramas": 100
            }
        ]
    )

    assert relatorio["data"] == date.today()
    assert relatorio["tipo_refeicao"] == "Dieta"


def test_nao_salvar_dieta_vazia():
    service = DietaService()

    with pytest.raises(
        ValueError,
        match=(
            "A dieta deve possuir pelo menos um alimento."
        )
    ):
        service.salvar_dieta([])


def test_nao_salvar_dieta_com_item_sem_alimento():
    service = DietaService()

    with pytest.raises(
        ValueError,
        match="O alimento do item é obrigatório."
    ):
        service.salvar_dieta(
            [
                {
                    "quantidade_gramas": 100
                }
            ]
        )


def test_nao_salvar_dieta_com_item_sem_quantidade():
    service = DietaService()

    with pytest.raises(
        ValueError,
        match="A quantidade do item é obrigatória."
    ):
        service.salvar_dieta(
            [
                {
                    "alimento_id": 1
                }
            ]
        )


def test_nao_salvar_parcialmente_dieta_invalida():
    banana = criar_alimento(
        nome="Banana",
        calorias=90,
        proteinas=1,
        carboidratos=23,
        gorduras=0.3
    )

    service = DietaService()

    with pytest.raises(
        ValueError,
        match="Alimento não encontrado."
    ):
        service.salvar_dieta(
            [
                {
                    "alimento_id": banana.id,
                    "quantidade_gramas": 100
                },
                {
                    "alimento_id": 999,
                    "quantidade_gramas": 200
                }
            ]
        )

    registros = service.listar_registros()

    assert registros == []


def test_buscar_registros_por_data():
    banana = criar_alimento(
        nome="Banana",
        calorias=90,
        proteinas=1,
        carboidratos=23,
        gorduras=0.3
    )

    service = DietaService()

    service.salvar_dieta(
        itens=[
            {
                "alimento_id": banana.id,
                "quantidade_gramas": 100
            }
        ],
        data_registro=date.today()
    )

    registros = service.buscar_registros_por_data(
        date.today()
    )

    assert len(registros) == 1
    assert registros[0].alimento_id == banana.id
    assert registros[0].quantidade_gramas == 100


def test_excluir_registro():
    banana = criar_alimento(
        nome="Banana",
        calorias=90,
        proteinas=1,
        carboidratos=23,
        gorduras=0.3
    )

    service = DietaService()

    relatorio = service.salvar_dieta(
        itens=[
            {
                "alimento_id": banana.id,
                "quantidade_gramas": 100
            }
        ]
    )

    registro_id = relatorio["itens"][0]["registro_id"]

    service.excluir_registro(registro_id)

    assert service.listar_registros() == []


def test_excluir_registro_inexistente():
    service = DietaService()

    with pytest.raises(
        ValueError,
        match="Registro alimentar não encontrado."
    ):
        service.excluir_registro(999)