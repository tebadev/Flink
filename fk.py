from datetime import datetime
from flink import logger, manager, storage
import argparse as ap


def main():
  registro = logger.Registro("flinklog")
  almacen = storage.Almacen(".bookmarks.json", registro)
  flink = manager.manager(almacen, registro)

  parser = ap.ArgumentParser(
      prog="tk",
      description="Herramienta CLI para controlar mi motor de procesamiento.",
      epilog="Usa '%(prog)s [comando] --help' para más información sobre un comando.",
  )

  subparsers = parser.add_subparsers(
      dest="command", required=True, help="Acciones disponibles"
  )

  subparsers.add_parser(
      "show", help="Muestra los elementos guardados"
  )

  args = parser.parse_args()

  if args.command == "show":
    print(flink.mostrar_marcadores())


if __name__ == "__main__":
  main()