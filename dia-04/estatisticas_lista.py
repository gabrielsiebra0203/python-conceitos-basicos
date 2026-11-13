"""Calcula mínimo, máximo e média de uma lista de números."""


def calcular_estatisticas(numeros):
    """Recebe uma lista de números e devolve (mínimo, máximo, média)."""
    minimo = min(numeros)
    maximo = max(numeros)
    media = sum(numeros) / len(numeros)
    return minimo, maximo, media


def main():
    numeros = [7, 3, 9, 1, 5]
    minimo, maximo, media = calcular_estatisticas(numeros)

    print(f"Lista: {numeros}")
    print(f"Mínimo: {minimo}")
    print(f"Máximo: {maximo}")
    print(f"Média: {media:.2f}")


if __name__ == "__main__":
    main()