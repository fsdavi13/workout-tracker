from datetime import date

from backend.dao.alimento_dao import AlimentoDAO
from backend.dao.registro_alimentar_dao import RegistroAlimentarDAO
from backend.models.registro_alimentar import RegistroAlimentar


class DietaService:

    def __init__(self):
        self.alimento_dao = AlimentoDAO()
        self.registro_alimentar_dao = RegistroAlimentarDAO()

    def buscar_alimentos_por_nome(self, termo):
        """
        Busca alimentos para o campo de sugestões da interface.

        O usuário digita parte do nome, mas deverá selecionar um
        alimento existente. O registro será feito pelo alimento_id.
        """
        if not isinstance(termo, str):
            raise ValueError("O termo de busca deve ser um texto.")

        termo = termo.strip()

        if not termo:
            return []

        return self.alimento_dao.buscar_por_nome(termo)

    def buscar_alimento_por_id(self, alimento_id):
        alimento = self.alimento_dao.buscar_por_id(alimento_id)

        if alimento is None:
            raise ValueError("Alimento não encontrado.")

        return alimento

    def calcular_macros_alimento(
        self,
        alimento_id,
        quantidade_gramas
    ):
        alimento = self.buscar_alimento_por_id(alimento_id)

        quantidade_gramas = self._validar_quantidade(
            quantidade_gramas
        )

        fator = quantidade_gramas / 100

        return {
            "alimento_id": alimento.id,
            "nome": alimento.nome,
            "quantidade_gramas": quantidade_gramas,
            "calorias": self._calcular_valor(
                alimento.calorias_por_100g,
                fator
            ),
            "proteinas_g": self._calcular_valor(
                alimento.proteinas_g,
                fator
            ),
            "carboidratos_g": self._calcular_valor(
                alimento.carboidratos_g,
                fator
            ),
            "gorduras_g": self._calcular_valor(
                alimento.gorduras_g,
                fator
            )
        }

    def salvar_dieta(
        self,
        itens,
        data_registro=None,
        tipo_refeicao="Dieta"
    ):
        """
        Salva uma dieta completa e retorna seu relatório nutricional.

        Exemplo de itens:

        [
            {
                "alimento_id": 1,
                "quantidade_gramas": 200
            },
            {
                "alimento_id": 5,
                "quantidade_gramas": 150
            }
        ]
        """
        itens = self._validar_itens(itens)
        data_registro = self._normalizar_data(data_registro)
        tipo_refeicao = self._validar_tipo_refeicao(
            tipo_refeicao
        )

        # Todos os itens são validados e calculados antes da gravação.
        # Assim, um item inválido não deixa uma dieta parcialmente salva.
        itens_calculados = []

        for item in itens:
            item_calculado = self.calcular_macros_alimento(
                alimento_id=item["alimento_id"],
                quantidade_gramas=item["quantidade_gramas"]
            )

            itens_calculados.append(item_calculado)

        registros_salvos = []

        for item in itens_calculados:
            registro = RegistroAlimentar(
                alimento_id=item["alimento_id"],
                data=data_registro,
                quantidade_gramas=item["quantidade_gramas"],
                tipo_refeicao=tipo_refeicao
            )

            registro_salvo = (
                self.registro_alimentar_dao.criar(registro)
            )

            registros_salvos.append(registro_salvo)

        relatorio_itens = []

        for item, registro in zip(
            itens_calculados,
            registros_salvos
        ):
            item_relatorio = item.copy()
            item_relatorio["registro_id"] = registro.id

            relatorio_itens.append(item_relatorio)

        return {
            "data": data_registro,
            "tipo_refeicao": tipo_refeicao,
            "itens": relatorio_itens,
            "totais": self._calcular_totais(
                relatorio_itens
            )
        }

    def listar_registros(self):
        return self.registro_alimentar_dao.buscar_todos()

    def buscar_registros_por_data(self, data_registro):
        data_registro = self._normalizar_data(
            data_registro
        )

        return self.registro_alimentar_dao.buscar_por_data(
            data_registro
        )

    def excluir_registro(self, registro_id):
        registro = self.registro_alimentar_dao.buscar_por_id(
            registro_id
        )

        if registro is None:
            raise ValueError(
                "Registro alimentar não encontrado."
            )

        self.registro_alimentar_dao.deletar(registro_id)

    def _validar_itens(self, itens):
        if not isinstance(itens, list) or not itens:
            raise ValueError(
                "A dieta deve possuir pelo menos um alimento."
            )

        for item in itens:
            if not isinstance(item, dict):
                raise ValueError(
                    "Cada item da dieta deve ser válido."
                )

            if "alimento_id" not in item:
                raise ValueError(
                    "O alimento do item é obrigatório."
                )

            if "quantidade_gramas" not in item:
                raise ValueError(
                    "A quantidade do item é obrigatória."
                )

        return itens

    def _validar_quantidade(self, quantidade_gramas):
        if (
            not isinstance(quantidade_gramas, (int, float))
            or isinstance(quantidade_gramas, bool)
        ):
            raise ValueError(
                "A quantidade em gramas deve ser numérica."
            )

        if quantidade_gramas <= 0:
            raise ValueError(
                "A quantidade em gramas deve ser maior que zero."
            )

        return quantidade_gramas

    def _normalizar_data(self, data_registro):
        if data_registro is None:
            return date.today()

        if not isinstance(data_registro, date):
            raise ValueError(
                "A data do registro é inválida."
            )

        return data_registro

    def _validar_tipo_refeicao(self, tipo_refeicao):
        if not isinstance(tipo_refeicao, str):
            raise ValueError(
                "O tipo da refeição é obrigatório."
            )

        tipo_refeicao = tipo_refeicao.strip()

        if not tipo_refeicao:
            raise ValueError(
                "O tipo da refeição é obrigatório."
            )

        return tipo_refeicao

    def _calcular_valor(self, valor_por_100g, fator):
        if valor_por_100g is None:
            return 0

        return round(valor_por_100g * fator, 2)

    def _calcular_totais(self, itens):
        totais = {
            "calorias": 0,
            "proteinas_g": 0,
            "carboidratos_g": 0,
            "gorduras_g": 0
        }

        for item in itens:
            totais["calorias"] += item["calorias"]
            totais["proteinas_g"] += item["proteinas_g"]
            totais["carboidratos_g"] += item[
                "carboidratos_g"
            ]
            totais["gorduras_g"] += item["gorduras_g"]

        for nutriente in totais:
            totais[nutriente] = round(
                totais[nutriente],
                2
            )

        return totais