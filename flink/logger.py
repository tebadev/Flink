from datetime import datetime

class Registro:
    def __init__(self, ruta_log):
        self.ruta_log = ruta_log

    def registrar(self, mensaje):
        with open(self.ruta_log, "a", encoding="utf-8") as archivo:
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            archivo.write(f"[{fecha}] {mensaje}\n")
            return mensaje