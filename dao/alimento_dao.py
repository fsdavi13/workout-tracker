from database.connection import conexao
from models.alimento import Alimento


class AlimentoDAO:

    def criar(self, alimento):
        comando = """
            INSERT INTO alimentos (
                nome,
                calorias_por_100g,
                proteinas_g,
                carboidratos_g,
                gorduras_g,
                categoria,
                fonte
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
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
                    alimento.categoria,
                    alimento.fonte
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

        if resultado is None:
            return None

        return self._converter_linha_para_alimento(resultado)

    def buscar_por_nome(self, nome):
        comando = """
            SELECT *
            FROM alimentos
            WHERE nome LIKE ?
            ORDER BY nome
        """

        with conexao() as con:
            resultados = con.execute(
                comando,
                (f"%{nome}%",)
            ).fetchall()

        return [
            self._converter_linha_para_alimento(linha)
            for linha in resultados
        ]

    def buscar_todos(self):
        comando = """
            SELECT *
            FROM alimentos
            ORDER BY nome
        """

        with conexao() as con:
            resultados = con.execute(comando).fetchall()

        return [
            self._converter_linha_para_alimento(linha)
            for linha in resultados
        ]

    def atualizar(self, alimento):
        comando = """
            UPDATE alimentos
            SET
                nome = ?,
                calorias_por_100g = ?,
                proteinas_g = ?,
                carboidratos_g = ?,
                gorduras_g = ?,
                categoria = ?,
                fonte = ?
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
                    alimento.fonte,
                    alimento.id
                )
            )

    def deletar(self, id):
        comando = """
            DELETE FROM alimentos
            WHERE id = ?
        """

        with conexao() as con:
            con.execute(comando, (id,))

    def _converter_linha_para_alimento(self, linha):
        return Alimento(
            nome=linha["nome"],
            calorias_por_100g=linha["calorias_por_100g"],
            proteinas_g=linha["proteinas_g"],
            carboidratos_g=linha["carboidratos_g"],
            gorduras_g=linha["gorduras_g"],
            categoria=linha["categoria"],
            fonte=linha["fonte"],
            id=linha["id"]
        )