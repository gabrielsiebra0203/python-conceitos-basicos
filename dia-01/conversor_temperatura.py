"""Converte uma temperatura de Celsius para Fahrenheit."""

celsius = float(input("Temperatura em Celsius: "))
fahrenheit = celsius * 9 / 5 + 32

print(f"{celsius:.1f} °C = {fahrenheit:.1f} °F")

if celsius <= 0:
    sensacao = "congelando"
elif celsius < 15:
    sensacao = "frio"
elif celsius <= 25:
    sensacao = "agradável"
elif celsius < 35:
    sensacao = "quente"
else:
    sensacao = "muito quente"

print(f"Sensação: {sensacao}.")
