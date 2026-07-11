from datetime import date

from database.connection import conexao
from models.registro_alimentar import RegistroAlimentar


class RegistroAlimentarDAO:


    def criar(self, registro):

        comando = """
            INSERT INTO registros_alimentares
            (
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


        if resultado:

            return RegistroAlimentar(
                resultado["alimento_id"],
                date.fromisoformat(resultado["data"]),
                resultado["quantidade_gramas"],
                resultado["refeicao"],
                resultado["id"]
            )


        return None



    def buscar_todos(self):

        comando = """
            SELECT *
            FROM registros_alimentares
            ORDER BY data DESC
        """


        registros = []


        with conexao() as con:

            resultados = con.execute(
                comando
            ).fetchall()


        for linha in resultados:

            registro = RegistroAlimentar(
                linha["alimento_id"],
                date.fromisoformat(linha["data"]),
                linha["quantidade_gramas"],
                linha["refeicao"],
                linha["id"]
            )

            registros.append(registro)


        return registros



    def buscar_por_data(self, data):

        comando = """
            SELECT *
            FROM registros_alimentares
            WHERE data = ?
            ORDER BY refeicao
        """


        registros = []


        with conexao() as con:

            resultados = con.execute(
                comando,
                (data.isoformat(),)
            ).fetchall()


        for linha in resultados:

            registro = RegistroAlimentar(
                linha["alimento_id"],
                date.fromisoformat(linha["data"]),
                linha["quantidade_gramas"],
                linha["refeicao"],
                linha["id"]
            )

            registros.append(registro)


        return registros



    def atualizar(self, registro):

        comando = """
            UPDATE registros_alimentares
            SET alimento_id = ?,
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

            con.execute(
                comando,
                (id,)
            )