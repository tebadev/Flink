import validators
from datetime import datetime
from tabulate import tabulate

class manager:
    def __init__(self, almacen, registro):
        self.almacen = almacen
        self.registro = registro


    def _generar_id(self):
        if not self.almacen.ids:
            return 1
        return max(self.almacen.ids) + 1


    def _generar_nombres(self, enlace):
        return enlace


    def agregar_marcador(self, enlace, nombre=None, etiquetas=None):
        self.almacen._cargar_diccionario()

        if not validators.url(enlace):
            return self.registro.registrar(f"Error: '{enlace}' no es una URL.")

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

        self.almacen._guardar_diccionario()
        return self.registro.registro(f"Se ha agregado '{self.diccionario['bookmarks'][-1]}' a la lista.")


    def eliminar_marcador(self, id):
        self.almacen._cargar_diccionario()

        if id in self.almacen.ids:
            marcador_borrado = self.almacen.diccionario["bookmarks"].pop(self.ids.index(id))
            self.almacenn._guardar_diccionario()
            return self.registro.registrar(f"Se ha borrado el elemento '{marcador_borrado}'")

        return self.registro.registrar(f"Advertencia: No se pudo borrar el iD '{id}' por que no existe.")


    def mostrar_marcadores(self):
        self.almacen._cargar_diccionario()

        tabla = tabulate(
            self.almacen.diccionario["bookmarks"],
            tablefmt="grid"
        )

        return tabla
