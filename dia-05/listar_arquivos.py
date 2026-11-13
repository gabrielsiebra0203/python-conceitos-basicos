"""Lista os arquivos e pastas de um diretório."""

from pathlib import Path

entrada = input("Caminho da pasta (ENTER para a pasta atual): ")
pasta = Path(entrada or ".")

if not pasta.is_dir():
    print("Essa pasta não existe.")
else:
    for item in sorted(pasta.iterdir()):
        tipo = "[pasta]  " if item.is_dir() else "[arquivo]"
        print(f"{tipo} {item.name}")