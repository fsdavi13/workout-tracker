import sqlite3
from contextlib import contextmanager

import config


# Mantém compatibilidade com testes antigos.
DATABASE_PATH = config.TEST_DATABASE_PATH


@contextmanager
def conexao():
    con = sqlite3.connect(config.DATABASE_PATH)

    # Permite acessar resultados como linha["nome"].
    con.row_factory = sqlite3.Row

    try:
        yield con
        con.commit()

    except Exception:
        con.rollback()
        raise

    finally:
        con.close()


def inicializar_banco():
    with open(
        config.SCHEMA_PATH,
        "r",
        encoding="utf-8"
    ) as arquivo:
        schema = arquivo.read()

    with conexao() as con:
        con.executescript(schema)