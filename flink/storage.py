import json
import os

class StorageJSON:
    def __init__(self, ruta_json, logger):
        self.ruta_json = ruta_json
        self.logger = logger
        self._verificar_archivo()

    def _verificar_archivo(self):
        if not os.path.exists(self.ruta_json):
            self.guardar({"bookmarks": []})
            self.logger.registrar(f"Advertencia: el archivo '{self.ruta_json}' no existe. Se ha generado uno nuevo.")
            return

        try:
            with open(self.ruta_json, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
                if not isinstance(datos, dict) or "bookmarks" not in datos:
                    raise ValueError
        except (json.JSONDecodeError, ValueError):
            self.guardar({"bookmarks": []})
            self.logger.registrar(f"Advertencia: El archivo '{self.ruta_json}' esta corrupto y se ha generado nuevamente.")

    def cargar(self):
        with open(self.ruta_json, "r", encoding="utf-8") as archivo:
            return json.load(archivo)

    def guardar(self, datos):
        with open(self.ruta_json, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)