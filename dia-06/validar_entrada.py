"""Funções que pedem números ao usuário e repetem até a entrada ser válida."""


def ler_inteiro(mensagem):
    """Pede um número inteiro até o usuário digitar um valor válido."""
    while True:
        texto = input(mensagem)
        try:
            return int(texto)
        except ValueError:
            print("Valor inválido. Digite apenas números inteiros, como 42.")


def ler_decimal(mensagem):
    """Pede um número decimal, aceitando vírgula ou ponto."""
    while True:
        texto = input(mensagem).replace(",", ".")
        try:
            return float(texto)
        except ValueError:
            print("Valor inválido. Digite um número, como 7.5 ou 7,5.")


def main():
    idade = ler_inteiro("Sua idade: ")
    nota = ler_decimal("Sua nota: ")
    print(f"Idade: {idade} anos | Nota: {nota:.1f}")


if __name__ == "__main__":
    main()