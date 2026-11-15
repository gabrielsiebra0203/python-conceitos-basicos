"""Primeiro contato com banco de dados: SQLite com o módulo sqlite3."""

import sqlite3
from pathlib import Path

ARQUIVO_BANCO = Path(__file__).parent / "loja.db"


def criar_tabela(conexao):
    """Cria a tabela de produtos, se ela ainda não existir."""
    conexao.execute(
        """
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL,
            quantidade INTEGER NOT NULL DEFAULT 0
        )
        """
    )


def inserir_produto(conexao, nome, preco, quantidade):
    """Insere um produto na tabela."""
    conexao.execute(
        "INSERT INTO produtos (nome, preco, quantidade) VALUES (?, ?, ?)",
        (nome, preco, quantidade),
    )


def listar_produtos(conexao):
    """Devolve todos os produtos como uma lista de tuplas."""
    cursor = conexao.execute("SELECT id, nome, preco, quantidade FROM produtos")
    return cursor.fetchall()


def main():
    conexao = sqlite3.connect(ARQUIVO_BANCO)
    try:
        criar_tabela(conexao)

        if not listar_produtos(conexao):
            inserir_produto(conexao, "Teclado", 89.90, 15)
            inserir_produto(conexao, "Mouse", 45.50, 30)
            inserir_produto(conexao, "Monitor", 749.00, 8)
            inserir_produto(conexao, "Cabo HDMI", 19.90, 50)
            conexao.commit()
            print("Produtos de exemplo cadastrados.\n")

        print(f"{'ID':>3} | {'Produto':<12} | {'Preço':>10} | {'Qtd':>4}")
        print("-" * 38)
        for id_produto, nome, preco, quantidade in listar_produtos(conexao):
            print(f"{id_produto:>3} | {nome:<12} | R$ {preco:>7.2f} | {quantidade:>4}")
    finally:
        conexao.close()


if __name__ == "__main__":
    main()