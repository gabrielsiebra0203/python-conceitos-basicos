"""Mini-cadastro: pede nome e idade e responde com uma mensagem personalizada."""

nome = input("Qual é o seu nome? ")
idade = int(input("Quantos anos você tem? "))

print(f"Olá, {nome}!")

if idade < 18:
    print("Você é menor de idade.")
elif idade < 60:
    print("Você é adulto.")
else:
    print("Você é idoso.")

print(f"Daqui a 10 anos você terá {idade + 10} anos.")