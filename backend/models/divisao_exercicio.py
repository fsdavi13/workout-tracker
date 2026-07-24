class DivisaoExercicio:
    def __init__(
        self,
        divisao_id,
        exercicio_id,
        ordem,
        id=None,
        exercicio=None,
    ):
        self.id = id
        self.divisao_id = divisao_id
        self.exercicio_id = exercicio_id
        self.ordem = ordem
        self.exercicio = exercicio