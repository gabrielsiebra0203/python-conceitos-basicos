"""Agenda de contatos que salva e carrega os dados em um arquivo JSON."""

import json
from pathlib import Path

ARQUIVO = Path(__file__).parent / "agenda.json"


def carregar_agenda():
    """Lê o JSON e devolve um dicionário {nome: telefone}."""
    if not ARQUIVO.exists():
        return {}
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except json.JSONDecodeError:
        print("O arquivo da agenda está corrompido. Começando com uma agenda vazia.")
        return {}


def salvar_agenda(agenda):
    """Grava o dicionário no arquivo JSON."""
    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(agenda, arquivo, ensure_ascii=False, indent=2)


def main():
    agenda = carregar_agenda()

    while True:
        print("\n1 - Adicionar contato")
        print("2 - Buscar contato")
        print("3 - Listar contatos")
        print("4 - Remover contato")
        print("0 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            telefone = input("Telefone: ")
            agenda[nome] = telefone
            salvar_agenda(agenda)
            print(f"{nome} foi salvo.")
        elif opcao == "2":
            nome = input("Nome para buscar: ")
            if nome in agenda:
                print(f"{nome}: {agenda[nome]}")
            else:
                print("Contato não encontrado.")
        elif opcao == "3":
            if len(agenda) == 0:
                print("A agenda está vazia.")
            else:
                for nome, telefone in agenda.items():
                    print(f"{nome}: {telefone}")
        elif opcao == "4":
            nome = input("Nome para remover: ")
            if nome in agenda:
                del agenda[nome]
                salvar_agenda(agenda)
                print(f"{nome} foi removido.")
            else:
                print("Contato não encontrado.")
        elif opcao == "0":
            print("Até logo!")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()