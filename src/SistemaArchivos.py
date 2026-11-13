
from src.Disco import Disco
from src.Archivo import Archivo


class SistemaArchivos:
    def __init__(self, capacidad: int, cluster_kb: int = 4):
        if capacidad <= 0 or cluster_kb <= 0:
            raise ValueError("La configuracion debe ser mayor a cero")

        self.disco = Disco(capacidad)
        self.cluster_kb = cluster_kb

        # Guardamos los archivos por su nombre
        self._archivos: dict[str, Archivo] = {}

    def crear_archivo(self, nombre: str, tamano: int) -> Archivo:
        nombre = nombre.strip()

        if not nombre:
            raise ValueError("El nombre no puede estar vacio")

        if nombre in self._archivos:
            raise ValueError("Ya existe un archivo con ese nombre")

        if tamano <= 0:
            raise ValueError("El tamaño debe ser mayor a cero")

        # Reservamos los bloques antes de registrar el archivo
        bloques = self.disco.reservar_bloques(tamano)
        archivo = Archivo(nombre, bloques)
        self._archivos[nombre] = archivo

        return archivo

    def eliminar_archivo(self, nombre: str) -> None:
        if nombre not in self._archivos:
            raise ValueError("El archivo no existe")

        archivo = self._archivos[nombre]

        # Al eliminarlo recuperamos el espacio que ocupaba
        self.disco.liberar_bloques(archivo.bloques)
        del self._archivos[nombre]

    def modificar_tamano(self, nombre: str, nuevo_tamano: int) -> None:
        if nombre not in self._archivos:
            raise ValueError("El archivo no existe")

        if nuevo_tamano <= 0:
            raise ValueError("El tamaño debe ser mayor a cero")

        archivo = self._archivos[nombre]
        diferencia = nuevo_tamano - archivo.tamano

        if diferencia > 0:
            # Si crece, necesita reservar mas bloques
            nuevos = self.disco.reservar_bloques(diferencia)
            archivo.bloques.extend(nuevos)

        elif diferencia < 0:
            # Si se achica, devolvemos los bloques sobrantes
            sobrantes = archivo.bloques[nuevo_tamano:]
            self.disco.liberar_bloques(sobrantes)
            archivo.bloques = archivo.bloques[:nuevo_tamano]

    def buscar_archivo(self, nombre: str) -> Archivo:
        if nombre not in self._archivos:
            raise ValueError("El archivo no existe")

        return self._archivos[nombre]

    def listar_archivos(self) -> list[Archivo]:
        return list(self._archivos.values())

    def mapa_disco(self) -> list[str | None]:
        # Cada posicion representa un bloque del disco
        mapa = [None] * self.disco.capacidad_total

        for archivo in self._archivos.values():
            for posicion in archivo.bloques:
                mapa[posicion] = archivo.nombre

        return mapa

    def consultar_mft(self) -> list[dict]:
        # Representacion sencilla de los registros de la MFT
        registros = []

        for numero, archivo in enumerate(self._archivos.values(), start=1):
            registros.append({
                "registro": numero,
                "nombre": archivo.nombre,
                "tamano": archivo.tamano,
                "extensiones": archivo.extensiones
            })

        return registros

    def obtener_metricas(self) -> dict:
        total = self.disco.capacidad_total
        libres = self.disco.bloques_disponibles()
        ocupados = total - libres

        mapa = self.mapa_disco()
        grupos_libres = 0
        anterior_ocupado = True

        # Contamos cuantos grupos separados de espacio libre hay
        for bloque in mapa:
            libre = bloque is None

            if libre and anterior_ocupado:
                grupos_libres += 1

            anterior_ocupado = not libre

        extensiones = sum(
            len(archivo.extensiones)
            for archivo in self._archivos.values()
        )

        return {
            "total": total,
            "ocupados": ocupados,
            "libres": libres,
            "porcentaje": round(ocupados * 100 / total, 2),
            "archivos": len(self._archivos),
            "extensiones": extensiones,
            "grupos_libres": grupos_libres,
            "capacidad_kb": total * self.cluster_kb
        }
