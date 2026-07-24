class DivisaoTreino:
    def __init__(
        self,
        nome,
        descricao=None,
        id=None,
    ):
        self.id = id
        self.nome = nome
        self.descricao = descricao

    def __str__(self):
        return self.nome