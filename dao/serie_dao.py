from datetime import date

from database.connection import conexao
from models.serie import Serie


class SerieDAO:

    
    def criar(self, serie):

        comando = "INSERT INTO series (exercicio_id, data, peso, repeticoes, observacoes) VALUES (?, ?, ?, ?, ?)"

        with conexao() as con:
            cursor = con.execute(comando, (serie.exercicio_id, serie.data.isoformat(), serie.peso, serie.repeticoes, serie.observacoes))
            serie.id = cursor.lastrowid

        return serie

    def buscar_por_id(self, id):
        comando = "SELECT * FROM series WHERE id = ?"
        
        with conexao() as con:
            resultado = con.execute(comando, (id,)).fetchone()

        if resultado:

            return Serie(
                resultado["exercicio_id"],
                date.fromisoformat(resultado["data"]),
                resultado["peso"],
                resultado["repeticoes"],
                resultado["observacoes"],
                resultado["id"]
            )
    
    def buscar_todas(self):
        comando = """SELECT * FROM series ORDER BY data DESC"""
        
        series = []

        with conexao() as con:
            resultados = con.execute(comando).fetchall()

        for linha in resultados:
            serie = Serie(
                linha["exercicio_id"],
                date.fromisoformat(linha["data"]),
                linha["peso"],
                linha["repeticoes"],
                linha["observacoes"],
                linha["id"]
            )

            series.append(serie)

        return series

    def buscar_por_exercicio(self, exercicio_id):
        comando = "SELECT * FROM series WHERE exercicio_id = ? ORDER BY data DESC"
        
        series = []
        
        with conexao() as con:
            resultados = con.execute(comando, (exercicio_id,)).fetchall()

        for linha in resultados:
            serie = Serie(
                linha["exercicio_id"],
                date.fromisoformat(linha["data"]),
                linha["peso"],
                linha["repeticoes"],
                linha["observacoes"],
                linha["id"]
            )

            series.append(serie)

        return series

    def atualizar(self, serie):
        comando = """UPDATE series SET exercicio_id = ?, data = ?, peso = ?, repeticoes = ?, observacoes = ? WHERE id = ?"""

        with conexao() as con:
            con.execute(comando, (serie.exercicio_id, serie.data.isoformat(), serie.peso, serie.repeticoes, serie.observacoes, serie.id))

    def deletar(self, id):
        comando = "DELETE FROM series WHERE id = ?"

        with conexao() as con:
            con.execute(comando, (id,))