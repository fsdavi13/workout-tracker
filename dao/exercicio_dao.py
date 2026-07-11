from models.exercicio import Exercicio
from database.connection import conexao


class ExercicioDAO:


    def criar(self, exercicio):
        comando = """
            INSERT INTO exercicios (nome, grupo_muscular)
            VALUES (?, ?)
        """
        with conexao() as con:
            cursor = con.execute(comando, (exercicio.nome, exercicio.grupo_muscular))
            exercicio.id = cursor.lastrowid

        return exercicio

    def buscar_por_id(self, id):
        comando = "SELECT * FROM exercicios WHERE id = ?"

        with conexao() as con:

            resultado = con.execute(comando, (id,)).fetchone()

        if resultado:
            return Exercicio(
                resultado["nome"],
                resultado["grupo_muscular"],
                resultado["id"]
            )

        return None

    def buscar_todos(self):
        comando = """SELECT * FROM exercicios ORDER BY nome"""
        exercicios = []

        with conexao() as con:
            resultados = con.execute(comando).fetchall()

        for linha in resultados:
            exercicio = Exercicio(
                linha["nome"],
                linha["grupo_muscular"],
                linha["id"]
            )
            exercicios.append(exercicio)

        return exercicios

    def atualizar(self, exercicio):
        comando = """
            UPDATE exercicios
            SET nome = ?, grupo_muscular = ?
            WHERE id = ?
        """
        with conexao() as con:
            con.execute(comando, (exercicio.nome, exercicio.grupo_muscular, exercicio.id))

    def deletar(self, id):
        comando = """DELETE FROM exercicios WHERE id = ?"""
        with conexao() as con:
            con.execute(comando, (id,))