"""Conta quantas vezes cada palavra aparece em um texto."""

texto = input("Digite um texto: ")
palavras = texto.lower().split()

contagem = {}

for palavra in palavras:
    if palavra in contagem:
        contagem[palavra] += 1
    else:
        contagem[palavra] = 1

for palavra, quantidade in contagem.items():
    print(f"{palavra}: {quantidade}")