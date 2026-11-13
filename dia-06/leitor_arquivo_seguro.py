"""Lê um arquivo de texto e avisa se algo der errado, sem travar."""


def ler_arquivo(caminho):
    """Devolve o conteúdo do arquivo, ou None se não for possível ler."""
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            return arquivo.read()
    except FileNotFoundError:
        print(f"Arquivo '{caminho}' não encontrado.")
    except (PermissionError, IsADirectoryError):
        print(f"Não foi possível ler '{caminho}': sem permissão ou é uma pasta.")
    except UnicodeDecodeError:
        print(f"'{caminho}' não é um arquivo de texto UTF-8 válido.")
    return None


def main():
    caminho = input("Caminho do arquivo: ")
    conteudo = ler_arquivo(caminho)

    if conteudo is not None:
        print(f"Arquivo lido com sucesso: {len(conteudo)} caracteres.")


if __name__ == "__main__":
    main()