from datetime import datetime
import validators
from tabulate import tabulate

class Flink:
    def __init__(self, storage, logger):
        self.storage = storage
        self.logger = logger

    def _generar_id(self, bookmarks):
        if not bookmarks:
            return 1
        return max(b["id"] for b in bookmarks) + 1

    def _generar_nombres(self, enlace):
        return enlace

    def agregar_marcador(self, enlace, nombre=None, etiquetas=None):
        if not validators.url(enlace):
            self.logger.registrar(f"Error: '{enlace}' no es una URL.")
            return "❌ Error: La URL ingresada no es válida."

        if not nombre:
            nombre = self._generar_nombres(enlace)
            self.logger.registrar(f"Aviso: No se indicó nombre, se usó el enlace para '{enlace}'.")

        datos = self.storage.cargar()
        nuevo_id = self._generar_id(datos["bookmarks"])

        nuevo_marcador = {
            "id": nuevo_id,
            "nombre": nombre,
            "enlace": enlace,
            "etiquetas": etiquetas,
            "fecha": datetime.now().strftime("%Y-%m-%dT%H:%M")
        }

        datos["bookmarks"].append(nuevo_marcador)
        self.storage.guardar(datos)

        self.logger.registrar(f"Se ha agregado el marcador ID {nuevo_id} a la lista.")
        return f"✨ Marcador '{nombre}' agregado con éxito."

    def eliminar_marcador(self, id_marcador):
        datos = self.storage.cargar()
        bookmarks = datos["bookmarks"]

        # Buscar el índice del marcador por su ID
        indice = next((i for i, b in enumerate(bookmarks) if b["id"] == id_marcador), None)

        if indice is not None:
            borrado = bookmarks.pop(indice)
            self.storage.guardar(datos)
            self.logger.registrar(f"Se ha borrado el elemento ID '{id_marcador}'")
            return f"🗑️ Se ha borrado el marcador '{borrado['nombre']}'."

        self.logger.registrar(f"Advertencia: No se pudo borrar el ID '{id_marcador}' porque no existe.")
        return f"⚠️ Advertencia: No existe un marcador con el ID '{id_marcador}'."

    def mostrar_marcadores(self):
        datos = self.storage.cargar()
        if not datos["bookmarks"]:
            return "No hay marcadores guardados."

        return tabulate(datos["bookmarks"], tablefmt="grid")