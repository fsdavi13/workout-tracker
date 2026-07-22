from backend.dao.exercicio_dao import ExercicioDAO
from backend.dao.serie_dao import SerieDAO
from backend.models.exercicio import Exercicio
from backend.models.serie import Serie


class AcademiaService:

    def __init__(self):
        self.exercicio_dao = ExercicioDAO()
        self.serie_dao = SerieDAO()

    def cadastrar_exercicio(self, nome, grupo_muscular):
        nome = nome.strip()
        grupo_muscular = grupo_muscular.strip()

        if not nome:
            raise ValueError("O nome do exercício é obrigatório.")

        if not grupo_muscular:
            raise ValueError("O grupo muscular é obrigatório.")

        exercicio = Exercicio(
            nome=nome,
            grupo_muscular=grupo_muscular
        )

        return self.exercicio_dao.criar(exercicio)

    def listar_exercicios(self):
        return self.exercicio_dao.buscar_todos()

    def buscar_exercicio_por_id(self, exercicio_id):
        exercicio = self.exercicio_dao.buscar_por_id(exercicio_id)

        if exercicio is None:
            raise ValueError("Exercício não encontrado.")

        return exercicio

    def atualizar_exercicio(
        self,
        exercicio_id,
        nome,
        grupo_muscular
    ):
        exercicio = self.buscar_exercicio_por_id(exercicio_id)

        nome = nome.strip()
        grupo_muscular = grupo_muscular.strip()

        if not nome:
            raise ValueError("O nome do exercício é obrigatório.")

        if not grupo_muscular:
            raise ValueError("O grupo muscular é obrigatório.")

        exercicio.nome = nome
        exercicio.grupo_muscular = grupo_muscular

        self.exercicio_dao.atualizar(exercicio)

        return exercicio

    def excluir_exercicio(self, exercicio_id):
        self.buscar_exercicio_por_id(exercicio_id)

        self.exercicio_dao.deletar(exercicio_id)

    def registrar_serie(
        self,
        exercicio_id,
        data,
        peso,
        repeticoes,
        observacoes=None
    ):
        self.buscar_exercicio_por_id(exercicio_id)

        if peso < 0:
            raise ValueError("O peso não pode ser negativo.")

        if repeticoes <= 0:
            raise ValueError(
                "A quantidade de repetições deve ser maior que zero."
            )

        if observacoes is not None:
            observacoes = observacoes.strip()

            if not observacoes:
                observacoes = None

        serie = Serie(
            exercicio_id=exercicio_id,
            data=data,
            peso=peso,
            repeticoes=repeticoes,
            observacoes=observacoes
        )

        return self.serie_dao.criar(serie)

    def listar_series(self):
        return self.serie_dao.buscar_todas()

    def buscar_series_por_exercicio(self, exercicio_id):
        self.buscar_exercicio_por_id(exercicio_id)

        return self.serie_dao.buscar_por_exercicio(exercicio_id)

    def calcular_volume_total_exercicio(self, exercicio_id):
        series = self.buscar_series_por_exercicio(exercicio_id)

        volume_total = 0

        for serie in series:
            volume_total += serie.calcular_volume()

        return volume_total

    def buscar_maior_carga(self, exercicio_id):
        series = self.buscar_series_por_exercicio(exercicio_id)

        if not series:
            return None

        maior_carga = series[0].peso

        for serie in series:
            if serie.peso > maior_carga:
                maior_carga = serie.peso

        return maior_carga

    def buscar_maior_volume_serie(self, exercicio_id):
        series = self.buscar_series_por_exercicio(exercicio_id)

        if not series:
            return None

        melhor_serie = series[0]

        for serie in series:
            if (
                serie.calcular_volume()
                > melhor_serie.calcular_volume()
            ):
                melhor_serie = serie

        return melhor_serie

    def calcular_volume_por_data(self, data):
        series = self.serie_dao.buscar_todas()

        volume_total = 0

        for serie in series:
            if serie.data == data:
                volume_total += serie.calcular_volume()

        return volume_total

    def contar_series_por_data(self, data):
        series = self.serie_dao.buscar_todas()

        quantidade = 0

        for serie in series:
            if serie.data == data:
                quantidade += 1

        return quantidade

    def excluir_serie(self, serie_id):
        serie = self.serie_dao.buscar_por_id(serie_id)

        if serie is None:
            raise ValueError("Série não encontrada.")

        self.serie_dao.deletar(serie_id)