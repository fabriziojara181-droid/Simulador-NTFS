class Disco:
    def __init__(self, capacidad_total: int):
        # Guardamos la cantidad total de bloques que va a tener el disco
        self.capacidad_total = capacidad_total
        self._bloques = [False] * capacidad_total

    def bloques_disponibles(self) -> int:
        # Contamos cuantos bloques siguen libres
        return self._bloques.count(False)