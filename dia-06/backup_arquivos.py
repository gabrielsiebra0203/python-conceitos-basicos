"""Copia um arquivo para a pasta 'backups', com data e hora no nome."""

import os
import shutil
from datetime import datetime
from pathlib import Path


def fazer_backup(origem, pasta_backup):
    """Copia o arquivo de origem para a pasta de backup e devolve o novo caminho."""
    origem = Path(origem)
    pasta_backup = Path(pasta_backup)
    pasta_backup.mkdir(exist_ok=True)

    carimbo = datetime.now().strftime("%Y%m%d_%H%M%S")
    destino = pasta_backup / f"{origem.stem}_{carimbo}{origem.suffix}"

    shutil.copy2(origem, destino)
    return destino


def main():
    print(f"Pasta atual: {os.getcwd()}")
    origem = input("Arquivo para copiar: ")

    try:
        destino = fazer_backup(origem, "backups")
    except FileNotFoundError:
        print("Arquivo não encontrado.")
    else:
        print(f"Backup criado em: {destino}")


if __name__ == "__main__":
    main()