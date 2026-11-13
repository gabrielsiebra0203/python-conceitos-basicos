"""Verificador de par ou ímpar usando função."""


def eh_par(numero):
    """Devolve True se o número for par, e False se for ímpar."""
    return numero % 2 == 0


def main():
    numero = int(input("Digite um número inteiro: "))

    if eh_par(numero):
        print(f"{numero} é par.")
    else:
        print(f"{numero} é ímpar.")


if __name__ == "__main__":
    main()