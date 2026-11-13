"""Lê um arquivo de texto e conta linhas e palavras."""

from pathlib import Path

caminho = Path(__file__).parent / "exemplo.txt"

with open(caminho, "r", encoding="utf-8") as arquivo:
    conteudo = arquivo.read()

linhas = conteudo.splitlines()
palavras = conteudo.split()

print(f"Linhas: {len(linhas)}")
print(f"Palavras: {len(palavras)}")