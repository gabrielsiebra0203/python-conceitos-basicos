 """Agenda de contatos usando dicionário."""

agenda = {}

while True:
    print("\n1 - Adicionar contato")
    print("2 - Buscar contato")
    print("3 - Listar contatos")
    print("0 - Sair")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        nome = input("Nome: ")
        telefone = input("Telefone: ")
        agenda[nome] = telefone
        print(f"{nome} foi adicionado.")
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
    elif opcao == "0":
        print("Até logo!")
        break
    else:
        print("Opção inválida.")