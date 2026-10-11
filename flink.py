import json
import os
import validators
from tabulate import tabulate
from datetime import datetime


class Flink:
    def __init__(self, json, logs):
        self.json = json
        self.logs = logs
        self.diccionario = {"bookmarks": []}
        self._verificar_archivo()
        self.ids = []


    def registro(self, mensaje):
        with open(self.logs, "a", encoding="utf-8") as archivo:
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            archivo.write(f"[{fecha}] {mensaje}\n")
            return mensaje


    def _verificar_archivo(self):
        if not os.path.exists(self.json):
            self._guardar_diccionario()
            return self.registro(f"Advertencia: el archivo '{self.json}' no existe. Se ha generado uno nuevo.")

        try:
            with open(self.json, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)

                if not isinstance(datos, dict) or "bookmarks" not in datos:
                    raise ValueError
        except (json.JSONDecodeError, ValueError):
            self._guardar_diccionario()
            return self.registro(f"Advertencia: El archivo '{self.json}' esta corructo y se ha generado nuevamente.")


    def _cargar_diccionario(self):
        with open (self.json, "r", encoding="utf-8") as archivo:
            self.diccionario = json.load(archivo)

        self.ids = []
        for marcador in self.diccionario["bookmarks"]:
            self.ids.append(marcador["id"])


    def _guardar_diccionario(self):
        with open (self.json, "w", encoding="utf-8") as archivo:
            json.dump(self.diccionario, archivo, indent=4, ensure_ascii=False)


    def _generar_id(self):
        if not self.ids:
            return 1
        return max(self.ids) + 1


    def _generar_nombres(self, enlace):
        return enlace


    def agregar_marcador(self, enlace, nombre=None, etiquetas=None):
        self._cargar_diccionario()

        if not validators.url(enlace):
            return self.registro(f"Error: '{enlace}' no es una URL.")

        if not nombre:
            nombre = self._generar_nombres(enlace)

        self.diccionario["bookmarks"].append(
            {
                "id": self._generar_id(),
                "nombre": nombre,
                "enlace": enlace,
                "etiquetas": etiquetas,
                "fecha": datetime.now().strftime("%Y-%m-%dT%H:%M")
            }
        )

        self._guardar_diccionario()
        return self.registro(f"Se ha agregado '{self.diccionario['bookmarks'][-1]}' a la lista.")


    def eliminar_marcador(self, id):
        self._cargar_diccionario()

        if id in self.ids:
            marcador_borrado = self.diccionario["bookmarks"].pop(self.ids.index(id))
            self._guardar_diccionario()
            return self.registro(f"Se ha borrado el elemento '{marcador_borrado}'")

        return self.registro(f"Advertencia: No se pudo borrar el iD '{id}' por que no existe.")


    def mostrar_marcadores(self):
        self._cargar_diccionario()

        tabla = tabulate(
            self.diccionario["bookmarks"],
            tablefmt="grid"
        )

        return tabla
