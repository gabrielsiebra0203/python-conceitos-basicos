"""Variáveis, tipos, input/print e if/elif/else."""

nome = "Ana"
idade = 17
altura = 1.65
estudante = True

print("Variáveis")
print("nome =", nome)
print("idade =", idade)
print("altura =", altura)
print("estudante =", estudante)

print()
print("Tipos")
print("nome:", type(nome).__name__)
print("idade:", type(idade).__name__)
print("altura:", type(altura).__name__)
print("estudante:", type(estudante).__name__)

print()
print("input e print")
nome = input("Qual é o seu nome? ")
idade = int(input("Quantos anos você tem? "))
altura = float(input("Qual é a sua altura em metros? "))

resposta = input("Você estuda? (s/n) ").strip().lower()
estudante = resposta == "s"

print(f"Olá, {nome}. Você tem {idade} anos e mede {altura:.2f} m.")

print()
print("if / elif / else")
if idade < 12:
    faixa = "criança"
elif idade < 18:
    faixa = "adolescente"
elif idade < 60:
    faixa = "adulto"
else:
    faixa = "pessoa idosa"

if estudante:
    situacao = "estuda"
else:
    situacao = "não estuda"

print(f"{nome} é {faixa} e {situacao}.")
