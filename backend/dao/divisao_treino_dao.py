from backend.database.connection import conexao
from backend.models.divisao_treino import DivisaoTreino


class DivisaoTreinoDAO:
    def criar(self, divisao):
        comando = """
            INSERT INTO divisoes_treino (
                nome,
                descricao
            )
            VALUES (?, ?)
        """

        with conexao() as con:
            cursor = con.execute(
                comando,
                (
                    divisao.nome,
                    divisao.descricao,
                ),
            )

            divisao.id = cursor.lastrowid

        return divisao

    def buscar_por_id(self, divisao_id):
        comando = """
            SELECT *
            FROM divisoes_treino
            WHERE id = ?
        """

        with conexao() as con:
            resultado = con.execute(
                comando,
                (divisao_id,),
            ).fetchone()

        if resultado is None:
            return None

        return DivisaoTreino(
            id=resultado["id"],
            nome=resultado["nome"],
            descricao=resultado["descricao"],
        )

    def buscar_todas(self):
        comando = """
            SELECT *
            FROM divisoes_treino
            ORDER BY id
        """

        divisoes = []

        with conexao() as con:
            resultados = con.execute(comando).fetchall()

        for resultado in resultados:
            divisoes.append(
                DivisaoTreino(
                    id=resultado["id"],
                    nome=resultado["nome"],
                    descricao=resultado["descricao"],
                )
            )

        return divisoes

    def atualizar(self, divisao):
        comando = """
            UPDATE divisoes_treino
            SET nome = ?,
                descricao = ?
            WHERE id = ?
        """

        with conexao() as con:
            con.execute(
                comando,
                (
                    divisao.nome,
                    divisao.descricao,
                    divisao.id,
                ),
            )

        return divisao

    def deletar(self, divisao_id):
        comando = """
            DELETE FROM divisoes_treino
            WHERE id = ?
        """

        with conexao() as con:
            con.execute(
                comando,
                (divisao_id,),
            )