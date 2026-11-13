"""Filtra de uma lista apenas os números maiores que 10."""

numeros = [3, 15, 8, 22, 10, 11, 7, 30]
maiores = []

for numero in numeros:
    if numero > 10:
        maiores.append(numero)

print(f"Lista original: {numeros}")
print(f"Maiores que 10: {maiores}")