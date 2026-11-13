"""Remove itens duplicados de uma lista usando set."""

numeros = [4, 2, 7, 2, 9, 4, 7, 1]

sem_duplicados = list(set(numeros))

print(f"Lista original: {numeros}")
print(f"Sem duplicados: {sem_duplicados}")
print(f"Removidos: {len(numeros) - len(sem_duplicados)} itens repetidos")