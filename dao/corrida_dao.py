from datetime import date

from database.connection import conexao
from models.corrida import Corrida


class CorridaDAO:


    def criar(self, corrida):
        comando = """INSERT INTO corridas (data, distancia_km, pace_segundos, observacoes) VALUES (?, ?, ?, ?)"""

        with conexao() as con:

            cursor = con.execute(comando, (corrida.data.isoformat(), corrida.distancia_km, corrida.pace_segundos, corrida.observacoes))
            corrida.id = cursor.lastrowid

        return corrida

    def buscar_por_id(self, id):
        comando = """SELECT * FROM corridas WHERE id = ?"""

        with conexao() as con:
            resultado = con.execute(comando, (id,)).fetchone()

        if resultado:
            return Corrida(
                date.fromisoformat(resultado["data"]),
                resultado["distancia_km"],
                resultado["pace_segundos"],
                resultado["observacoes"],
                resultado["id"]
            )

        return None

    def buscar_todas(self):
        comando = """SELECT * FROM corridas ORDER BY data DESC"""
        corridas = []

        with conexao() as con:
            resultados = con.execute(comando).fetchall()

        for linha in resultados:
            corrida = Corrida(
                date.fromisoformat(linha["data"]),
                linha["distancia_km"],
                linha["pace_segundos"],
                linha["observacoes"],
                linha["id"]
            )
            corridas.append(corrida)

        return corridas

    def atualizar(self, corrida):
        comando = """UPDATE corridas SET data = ?, distancia_km = ?, pace_segundos = ?, observacoes = ? WHERE id = ?"""

        with conexao() as con:
            con.execute(comando, (corrida.data.isoformat(), corrida.distancia_km, corrida.pace_segundos, corrida.observacoes, corrida.id))

    def deletar(self, id):
        comando = """DELETE FROM corridas WHERE id = ?"""

        with conexao() as con:
            con.execute(comando, (id,))