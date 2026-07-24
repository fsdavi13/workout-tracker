from backend.database.connection import conexao
from backend.models.divisao_exercicio import (
    DivisaoExercicio,
)
from backend.models.exercicio import Exercicio


class DivisaoExercicioDAO:
    def criar(self, associacao):
        comando = """
            INSERT INTO divisao_exercicios (
                divisao_id,
                exercicio_id,
                ordem
            )
            VALUES (?, ?, ?)
        """

        with conexao() as con:
            cursor = con.execute(
                comando,
                (
                    associacao.divisao_id,
                    associacao.exercicio_id,
                    associacao.ordem,
                ),
            )

            associacao.id = cursor.lastrowid

        return associacao

    def buscar_por_divisao_e_exercicio(
        self,
        divisao_id,
        exercicio_id,
    ):
        comando = """
            SELECT *
            FROM divisao_exercicios
            WHERE divisao_id = ?
              AND exercicio_id = ?
        """

        with conexao() as con:
            resultado = con.execute(
                comando,
                (
                    divisao_id,
                    exercicio_id,
                ),
            ).fetchone()

        if resultado is None:
            return None

        return DivisaoExercicio(
            id=resultado["id"],
            divisao_id=resultado["divisao_id"],
            exercicio_id=resultado["exercicio_id"],
            ordem=resultado["ordem"],
        )

    def buscar_por_divisao(self, divisao_id):
        comando = """
            SELECT
                de.id AS associacao_id,
                de.divisao_id,
                de.exercicio_id,
                de.ordem,
                e.nome,
                e.grupo_muscular
            FROM divisao_exercicios AS de
            INNER JOIN exercicios AS e
                ON e.id = de.exercicio_id
            WHERE de.divisao_id = ?
            ORDER BY de.ordem
        """

        associacoes = []

        with conexao() as con:
            resultados = con.execute(
                comando,
                (divisao_id,),
            ).fetchall()

        for resultado in resultados:
            exercicio = Exercicio(
                id=resultado["exercicio_id"],
                nome=resultado["nome"],
                grupo_muscular=resultado[
                    "grupo_muscular"
                ],
            )

            associacoes.append(
                DivisaoExercicio(
                    id=resultado["associacao_id"],
                    divisao_id=resultado["divisao_id"],
                    exercicio_id=resultado[
                        "exercicio_id"
                    ],
                    ordem=resultado["ordem"],
                    exercicio=exercicio,
                )
            )

        return associacoes

    def buscar_proxima_ordem(self, divisao_id):
        comando = """
            SELECT COALESCE(MAX(ordem), 0) + 1
            AS proxima_ordem
            FROM divisao_exercicios
            WHERE divisao_id = ?
        """

        with conexao() as con:
            resultado = con.execute(
                comando,
                (divisao_id,),
            ).fetchone()

        return resultado["proxima_ordem"]

    def deletar(self, associacao_id):
        comando = """
            DELETE FROM divisao_exercicios
            WHERE id = ?
        """

        with conexao() as con:
            con.execute(
                comando,
                (associacao_id,),
            )

    def deletar_por_divisao_e_exercicio(
        self,
        divisao_id,
        exercicio_id,
    ):
        comando = """
            DELETE FROM divisao_exercicios
            WHERE divisao_id = ?
              AND exercicio_id = ?
        """

        with conexao() as con:
            con.execute(
                comando,
                (
                    divisao_id,
                    exercicio_id,
                ),
            )

    def atualizar_ordem(
        self,
        associacao_id,
        ordem,
    ):
        comando = """
            UPDATE divisao_exercicios
            SET ordem = ?
            WHERE id = ?
        """

        with conexao() as con:
            con.execute(
                comando,
                (
                    ordem,
                    associacao_id,
                ),
            )