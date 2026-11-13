"""Agenda de contatos que salva e carrega os dados em um arquivo CSV."""

import csv
from pathlib import Path

ARQUIVO = Path(__file__).parent / "agenda.csv"


def carregar_agenda():
    """Lê o CSV e devolve um dicionário {nome: telefone}."""
    agenda = {}
    if not ARQUIVO.exists():
        return agenda
    with open(ARQUIVO, "r", newline="", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            agenda[linha["nome"]] = linha["telefone"]
    return agenda


def salvar_agenda(agenda):
    """Grava o dicionário {nome: telefone} no CSV."""
    with open(ARQUIVO, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(["nome", "telefone"])
        for nome, telefone in agenda.items():
            escritor.writerow([nome, telefone])


def main():
    agenda = carregar_agenda()

    while True:
        print("\n1 - Adicionar contato")
        print("2 - Listar contatos")
        print("0 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            telefone = input("Telefone: ")
            agenda[nome] = telefone
            salvar_agenda(agenda)
            print(f"{nome} foi salvo.")
        elif opcao == "2":
            if len(agenda) == 0:
                print("A agenda está vazia.")
            else:
                for nome, telefone in agenda.items():
                    print(f"{nome}: {telefone}")
        elif opcao == "0":
            print("Até logo!")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()