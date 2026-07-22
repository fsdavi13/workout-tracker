from datetime import date

from database.connection import conexao
from models.registro_alimentar import RegistroAlimentar


class RegistroAlimentarDAO:

    def criar(self, registro):
        comando = """
            INSERT INTO registros_alimentares (
                alimento_id,
                data,
                quantidade_gramas,
                refeicao
            )
            VALUES (?, ?, ?, ?)
        """

        with conexao() as con:
            cursor = con.execute(
                comando,
                (
                    registro.alimento_id,
                    registro.data.isoformat(),
                    registro.quantidade_gramas,
                    registro.refeicao
                )
            )

            registro.id = cursor.lastrowid

        return registro

    def buscar_por_id(self, id):
        comando = """
            SELECT *
            FROM registros_alimentares
            WHERE id = ?
        """

        with conexao() as con:
            resultado = con.execute(
                comando,
                (id,)
            ).fetchone()

        if resultado is None:
            return None

        return self._converter_linha_para_registro(resultado)

    def buscar_todos(self):
        comando = """
            SELECT *
            FROM registros_alimentares
            ORDER BY data DESC
        """

        with conexao() as con:
            resultados = con.execute(comando).fetchall()

        return [
            self._converter_linha_para_registro(linha)
            for linha in resultados
        ]

    def buscar_por_data(self, data_registro):
        comando = """
            SELECT *
            FROM registros_alimentares
            WHERE data = ?
            ORDER BY refeicao
        """

        with conexao() as con:
            resultados = con.execute(
                comando,
                (data_registro.isoformat(),)
            ).fetchall()

        return [
            self._converter_linha_para_registro(linha)
            for linha in resultados
        ]

    def atualizar(self, registro):
        comando = """
            UPDATE registros_alimentares
            SET
                alimento_id = ?,
                data = ?,
                quantidade_gramas = ?,
                refeicao = ?
            WHERE id = ?
        """

        with conexao() as con:
            con.execute(
                comando,
                (
                    registro.alimento_id,
                    registro.data.isoformat(),
                    registro.quantidade_gramas,
                    registro.refeicao,
                    registro.id
                )
            )

    def deletar(self, id):
        comando = """
            DELETE FROM registros_alimentares
            WHERE id = ?
        """

        with conexao() as con:
            con.execute(comando, (id,))

    def _converter_linha_para_registro(self, linha):
        return RegistroAlimentar(
            alimento_id=linha["alimento_id"],
            data=date.fromisoformat(linha["data"]),
            quantidade_gramas=linha["quantidade_gramas"],
            tipo_refeicao=linha["refeicao"],
            id=linha["id"]
        )