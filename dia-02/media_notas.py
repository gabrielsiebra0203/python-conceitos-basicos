"""Calcula a média das notas digitadas pelo usuário."""

notas = []

while True:
    entrada = input("Digite uma nota (ou 'fim' para encerrar): ")
    if entrada == "fim":
        break
    notas.append(float(entrada))

if len(notas) > 0:
    media = sum(notas) / len(notas)
    print(f"Você digitou {len(notas)} notas.")
    print(f"Média: {media:.2f}")
else:
    print("Nenhuma nota foi digitada.")