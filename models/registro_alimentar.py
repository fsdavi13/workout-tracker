class RegistroAlimentar:

    def __init__(
        self,
        alimento_id,
        data,
        quantidade_gramas,
        tipo_refeicao=None,
        refeicao=None,
        id=None
    ):
        self.id = id
        self.alimento_id = alimento_id
        self.data = data
        self.quantidade_gramas = quantidade_gramas

        if tipo_refeicao is not None:
            self.tipo_refeicao = tipo_refeicao
        else:
            self.tipo_refeicao = refeicao

        # Compatibilidade caso algum DAO ainda use "refeicao".
        self.refeicao = self.tipo_refeicao