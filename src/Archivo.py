from dataclasses import dataclass, field


@dataclass
class Archivo:
    nombre: str
    bloques: list[int] = field(default_factory=list)

    @property
    def tamano(self) -> int:
        # El tamaño depende de cuantos bloques tiene asignados
        return len(self.bloques)

    @property
    def extensiones(self) -> list[tuple[int, int]]:
        # Agrupamos los bloques consecutivos en extensiones
        if not self.bloques:
            return []

        ordenados = sorted(self.bloques)
        resultado = []
        inicio = ordenados[0]
        cantidad = 1

        for bloque in ordenados[1:]:
            if bloque == inicio + cantidad:
                cantidad += 1
            else:
                resultado.append((inicio, cantidad))
                inicio = bloque
                cantidad = 1

        resultado.append((inicio, cantidad))
        return resultado
