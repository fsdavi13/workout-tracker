class Corrida:

    def __init__(
        self,
        data,
        distancia_km,
        pace=None,
        pace_segundos=None,
        observacoes=None,
        id=None
    ):
        self.id = id
        self.data = data
        self.distancia_km = distancia_km
        self.observacoes = observacoes

        if isinstance(pace, str):
            self.pace = pace
            self.pace_segundos = self.converter_pace_para_segundos(pace)

        elif isinstance(pace, int):
            self.pace_segundos = pace
            self.pace = self.converter_segundos_para_pace(pace)

        else:
            self.pace_segundos = pace_segundos
            self.pace = self.converter_segundos_para_pace(pace_segundos)

    def converter_pace_para_segundos(self, pace):
        partes = pace.split(":")

        minutos = int(partes[0])
        segundos = int(partes[1])

        return minutos * 60 + segundos

    def converter_segundos_para_pace(self, pace_segundos):
        if pace_segundos is None:
            return None

        minutos = pace_segundos // 60
        segundos = pace_segundos % 60

        return f"{minutos:02d}:{segundos:02d}"

    def calcular_tempo_segundos(self):
        if self.pace_segundos is None:
            return None

        return int(
            self.pace_segundos * self.distancia_km
        )