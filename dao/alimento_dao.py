from database.connection import conexao
from models.alimento import Alimento


class AlimentoDAO:


    def criar(self, alimento):

        comando = """
            INSERT INTO alimentos
            (
                nome,
                calorias_por_100g,
                proteinas_g,
                carboidratos_g,
                gorduras_g,
                categoria
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """


        with conexao() as con:

            cursor = con.execute(
                comando,
                (
                    alimento.nome,
                    alimento.calorias_por_100g,
                    alimento.proteinas_g,
                    alimento.carboidratos_g,
                    alimento.gorduras_g,
                    alimento.categoria
                )
            )

            alimento.id = cursor.lastrowid


        return alimento



    def buscar_por_id(self, id):

        comando = """
            SELECT *
            FROM alimentos
            WHERE id = ?
        """


        with conexao() as con:

            resultado = con.execute(
                comando,
                (id,)
            ).fetchone()


        if resultado:

            return Alimento(
                resultado["nome"],
                resultado["calorias_por_100g"],
                resultado["proteinas_g"],
                resultado["carboidratos_g"],
                resultado["gorduras_g"],
                resultado["categoria"],
                resultado["id"]
            )


        return None



    def buscar_por_nome(self, nome):

        comando = """
            SELECT *
            FROM alimentos
            WHERE nome LIKE ?
        """


        with conexao() as con:

            resultados = con.execute(
                comando,
                (f"%{nome}%",)
            ).fetchall()


        alimentos = []


        for linha in resultados:

            alimento = Alimento(
                linha["nome"],
                linha["calorias_por_100g"],
                linha["proteinas_g"],
                linha["carboidratos_g"],
                linha["gorduras_g"],
                linha["categoria"],
                linha["id"]
            )

            alimentos.append(alimento)


        return alimentos



    def buscar_todos(self):

        comando = """
            SELECT *
            FROM alimentos
            ORDER BY nome
        """


        alimentos = []


        with conexao() as con:

            resultados = con.execute(
                comando
            ).fetchall()



        for linha in resultados:

            alimento = Alimento(
                linha["nome"],
                linha["calorias_por_100g"],
                linha["proteinas_g"],
                linha["carboidratos_g"],
                linha["gorduras_g"],
                linha["categoria"],
                linha["id"]
            )

            alimentos.append(alimento)


        return alimentos



    def atualizar(self, alimento):

        comando = """UPDATE alimentos SET nome = ?,
                calorias_por_100g = ?,
                proteinas_g = ?,
                carboidratos_g = ?,
                gorduras_g = ?,
                categoria = ?
            WHERE id = ?
        """

        with conexao() as con:

            con.execute(
                comando,
                (
                    alimento.nome,
                    alimento.calorias_por_100g,
                    alimento.proteinas_g,
                    alimento.carboidratos_g,
                    alimento.gorduras_g,
                    alimento.categoria,
                    alimento.id
                )
            )



    def deletar(self, id):
        comando = """DELETE FROM alimentos WHERE id = ?"""

        with conexao() as con:

            con.execute(
                comando,
                (id,)
            )