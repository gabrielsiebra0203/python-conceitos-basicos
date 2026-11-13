"""FizzBuzz refatorado com funções e valor padrão."""


def fizzbuzz(numero):
    """Devolve Fizz, Buzz, FizzBuzz ou o próprio número."""
    if numero % 15 == 0:
        return "FizzBuzz"
    elif numero % 3 == 0:
        return "Fizz"
    elif numero % 5 == 0:
        return "Buzz"
    else:
        return numero


def gerar_fizzbuzz(limite=100):
    """Devolve a lista de resultados do FizzBuzz de 1 até o limite."""
    resultados = []
    for numero in range(1, limite + 1):
        resultados.append(fizzbuzz(numero))
    return resultados


def main():
    for resultado in gerar_fizzbuzz():
        print(resultado)


if __name__ == "__main__":
    main()