"""Conversor de temperatura refatorado com funções."""


def celsius_para_fahrenheit(celsius):
    """Converte uma temperatura de Celsius para Fahrenheit."""
    return celsius * 9 / 5 + 32


def classificar_sensacao(celsius):
    """Devolve a sensação térmica para uma temperatura em Celsius."""
    if celsius <= 0:
        return "congelando"
    elif celsius < 15:
        return "frio"
    elif celsius <= 25:
        return "agradável"
    elif celsius < 35:
        return "quente"
    else:
        return "muito quente"


def main():
    celsius = float(input("Temperatura em Celsius: "))
    fahrenheit = celsius_para_fahrenheit(celsius)
    sensacao = classificar_sensacao(celsius)

    print(f"{celsius:.1f} °C = {fahrenheit:.1f} °F")
    print(f"Sensação: {sensacao}.")


if __name__ == "__main__":
    main()