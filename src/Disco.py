class Disco:
    def __init__(self, capacidad_total: int):
        # Guardamos la capacidad y creamos todos los bloques libres
        self.capacidad_total = capacidad_total
        self._bloques = [False] * capacidad_total

    def bloques_disponibles(self) -> int:
        # Contamos cuantos bloques siguen libres
        return self._bloques.count(False)

    def reservar_bloques(self, cantidad: int) -> list[int]:
        # Buscamos bloques libres hasta completar la cantidad solicitada
        disponibles = []

        for posicion, ocupado in enumerate(self._bloques):
            if not ocupado and len(disponibles) < cantidad:
                disponibles.append(posicion)

        # Comprobamos que haya espacio suficiente antes de ocuparlo
        if len(disponibles) < cantidad:
            raise ValueError("No hay espacio suficiente en el disco")

        # Marcamos como ocupados los bloques seleccionados
        for posicion in disponibles:
            self._bloques[posicion] = True

        return disponibles
