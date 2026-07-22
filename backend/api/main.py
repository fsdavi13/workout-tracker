from fastapi import FastAPI

app = FastAPI(
    title="Evolv API",
    description="API para gerenciamento de treinos, corridas e alimentação.",
    version="1.0.0",
)


@app.get("/health")
def verificar_saude() -> dict[str, str]:
    return {"status": "ok"}