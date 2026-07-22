import pytest

import config
from database.connection import inicializar_banco


@pytest.fixture(autouse=True)
def usar_banco_de_testes():
    banco_original = config.DATABASE_PATH

    config.DATABASE_PATH = config.TEST_DATABASE_PATH

    if config.TEST_DATABASE_PATH.exists():
        config.TEST_DATABASE_PATH.unlink()

    inicializar_banco()

    yield

    if config.TEST_DATABASE_PATH.exists():
        config.TEST_DATABASE_PATH.unlink()

    config.DATABASE_PATH = banco_original