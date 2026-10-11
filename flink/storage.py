import os
import json

class Almacen:
    def __init__(self, ruta_json, registro):
        self.ruta_json = ruta_json
        self.registro = registro
        self.diccionario = {}
        self.ids = []


    def _verificar_archivo(self):
        if not os.path.exists(self.ruta_json):
            self._guardar_diccionario()
            return self.registro.registrar(f"Advertencia: el archivo '{self.json}' no existe. Se ha generado uno nuevo.")

        try:
            with open(self.ruta_json, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)

                if not isinstance(datos, dict) or "bookmarks" not in datos:
                    raise ValueError
        except (json.JSONDecodeError, ValueError):
            self._guardar_diccionario()
            return self.registro.registrar(f"Advertencia: El archivo '{self.json}' esta corructo y se ha generado nuevamente.")


    def _cargar_diccionario(self):
        with open (self.ruta_json, "r", encoding="utf-8") as archivo:
            self.diccionario = json.load(archivo)

        self.ids = []
        for marcador in self.diccionario["bookmarks"]:
            self.ids.append(marcador["id"])


    def _guardar_diccionario(self):
        with open (self.ruta_json, "w", encoding="utf-8") as archivo:
            json.dump(self.diccionario, archivo, indent=4, ensure_ascii=False)