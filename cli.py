from datetime import datetime
import json
import os
import tabulate
import validators


class Logger:
    """Se encarga exclusivamente de registrar los eventos y mensajes."""

    def __init__(self, ruta_logs):
        self.ruta_logs = ruta_logs

    def registrar(self, mensaje):
        with open(self.ruta_logs, "a", encoding="utf-8") as archivo:
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            archivo.write(f"[{fecha}] {mensaje}\n")
            return mensaje


class Storage:
    """Se encarga de la lectura, escritura y validación del archivo JSON."""

    def __init__(self, ruta_json, logger):
        self.ruta_json = ruta_json
        self.logger = logger
        self._verificar_archivo()

    def _verificar_archivo(self):
        if not os.path.exists(self.ruta_json):
            self.guardar({"bookmarks": []})
            self.logger.registrar(
                f"Advertencia: el archivo '{self.ruta_json}' no existe. Se ha generado uno nuevo."
            )
            return

        try:
            with open(self.ruta_json, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
                if not isinstance(datos, dict) or "bookmarks" not in datos:
                    raise ValueError
        except (json.JSONDecodeError, ValueError):
            self.guardar({"bookmarks": []})
            self.logger.registrar(
                f"Advertencia: El archivo '{self.ruta_json}' esta corrupto y se ha generado nuevamente."
            )

    def cargar(self):
        with open(self.ruta_json, "r", encoding="utf-8") as archivo:
            return json.load(archivo)

    def guardar(self, datos):
        with open(self.ruta_json, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)

    def generar_id(self, datos):
        ids = [marcador["id"] for marcador in datos["bookmarks"]]
        if not ids:
            return 1
        return max(ids) + 1


class FlinkManager:
    """Coordina la lógica de negocio de los marcadores usando Storage y Logger."""

    def __init__(self, ruta_json="bookmarks.json", ruta_logs="app.log"):
        self.logger = Logger(ruta_logs)
        self.storage = Storage(ruta_json, self.logger)

    def agregar_marcador(self, enlace, nombre=None, etiquetas=None):
        if not validators.url(enlace):
            return self.logger.registrar(f"Error: '{enlace}' no es una URL.")

        if not nombre:
            nombre = enlace

        datos = self.storage.cargar()
        nuevo_id = self.storage.generar_id(datos)

        nuevo_marcador = {
            "id": nuevo_id,
            "nombre": nombre,
            "enlace": enlace,
            "etiquetas": etiquetas,
            "fecha": datetime.now().strftime("%Y-%m-%dT%H:%M"),
        }

        datos["bookmarks"].append(nuevo_marcador)
        self.storage.guardar(datos)

        return self.logger.registrar(f"Se ha agregado '{nuevo_marcador}' a la lista.")

    def eliminar_marcador(self, id_marcador):
        datos = self.storage.cargar()
        bookmarks = datos["bookmarks"]

        # Buscar el marcador por ID
        for i, marcador in enumerate(bookmarks):
            if marcador["id"] == id_marcador:
                borrado = bookmarks.pop(i)
                self.storage.guardar(datos)
                return self.logger.registrar(
                    f"Se ha borrado el elemento '{borrado}'"
                )

        return self.logger.registrar(
            f"Advertencia: No se pudo borrar el ID '{id_marcador}' porque no existe."
        )

    def mostrar_marcadores(self):
        datos = self.storage.cargar()
        if not datos["bookmarks"]:
            return "No hay marcadores guardados."
        return tabulate.tabulate(datos["bookmarks"], tablefmt="grid")