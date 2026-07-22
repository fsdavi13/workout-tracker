from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


# Banco de dados
DATABASE_DIR = BASE_DIR / "database"
DATABASE_PATH = DATABASE_DIR / "workout_tracker.db"
SCHEMA_PATH = DATABASE_DIR / "schema.sql"

TEST_DATABASE_PATH = (
    BASE_DIR
    / "database"
    / "test_workout_tracker.db"
)

# Importadores
SEEDS_DIR = DATABASE_DIR / "seeds"
TACO_PATH = SEEDS_DIR / "taco.xlsx"


# Configurações da aplicação
APPEARANCE_MODE = "dark"
COLOR_THEME = "blue"


# Opções utilizadas futuramente nos Controllers/Views

TIPOS_REFEICAO = [
    "Cafe da manha",
    "Almoco",
    "Lanche",
    "Jantar",
    "Ceia",
]


GRUPOS_MUSCULARES = [
    "Peito",
    "Costas",
    "Ombro",
    "Biceps",
    "Triceps",
    "Pernas",
    "Abdomen",
]