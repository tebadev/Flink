from datetime import datetime

class Logger:
    def __init__(self, ruta_log):
        self.ruta_log = ruta_log

    def registro(self, mensaje):
        with open(self.logs, "a", encoding="utf-8") as archivo:
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            archivo.write(f"[{fecha}] {mensaje}\n")
