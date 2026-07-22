from backend.database.connection import conexao
from backend.models.porcao import Porcao


class PorcaoDAO:

    def criar(self, porcao):

        comando = """
            INSERT INTO porcoes
            (
                alimento_id,
                descricao,
                gramas
            )
            VALUES (?, ?, ?)
        """

        with conexao() as con:

            cursor = con.execute(
                comando,
                (
                    porcao.alimento_id,
                    porcao.descricao,
                    porcao.gramas
                )
            )

            porcao.id = cursor.lastrowid

        return porcao


    def buscar_por_id(self, id):

        comando = """
            SELECT *
            FROM porcoes
            WHERE id = ?
        """

        with conexao() as con:

            resultado = con.execute(
                comando,
                (id,)
            ).fetchone()

        if resultado is None:
            return None

        return Porcao(
            alimento_id=resultado["alimento_id"],
            descricao=resultado["descricao"],
            gramas=resultado["gramas"],
            id=resultado["id"]
        )


    def buscar_por_alimento(self, alimento_id):

        comando = """
            SELECT *
            FROM porcoes
            WHERE alimento_id = ?
            ORDER BY descricao
        """

        with conexao() as con:

            resultados = con.execute(
                comando,
                (alimento_id,)
            ).fetchall()

        porcoes = []

        for linha in resultados:

            porcoes.append(

                Porcao(
                    alimento_id=linha["alimento_id"],
                    descricao=linha["descricao"],
                    gramas=linha["gramas"],
                    id=linha["id"]
                )

            )

        return porcoes


    def buscar_todas(self):

        comando = """
            SELECT *
            FROM porcoes
            ORDER BY descricao
        """

        with conexao() as con:

            resultados = con.execute(comando).fetchall()

        porcoes = []

        for linha in resultados:

            porcoes.append(

                Porcao(
                    alimento_id=linha["alimento_id"],
                    descricao=linha["descricao"],
                    gramas=linha["gramas"],
                    id=linha["id"]
                )

            )

        return porcoes


    def atualizar(self, porcao):

        comando = """
            UPDATE porcoes
            SET
                descricao = ?,
                gramas = ?
            WHERE id = ?
        """

        with conexao() as con:

            con.execute(
                comando,
                (
                    porcao.descricao,
                    porcao.gramas,
                    porcao.id
                )
            )


    def deletar(self, id):

        comando = """
            DELETE FROM porcoes
            WHERE id = ?
        """

        with conexao() as con:

            con.execute(
                comando,
                (id,)
            )