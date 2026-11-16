"""Chave estrangeira: o banco protege a ligação entre as tabelas."""

import sqlite3

from banco_relacional import abrir_banco_exemplo

INSERT_PRODUTO = (
    "INSERT INTO produtos (nome, categoria_id, preco, quantidade) VALUES (?, ?, ?, ?)"
)


def tentar(descricao, conexao, sql, parametros=()):
    """Executa um comando e mostra se o banco aceitou ou recusou."""
    try:
        with conexao:
            cursor = conexao.execute(sql, parametros)
        print(f"ACEITO   | {descricao} ({cursor.rowcount} linha(s))")
    except sqlite3.IntegrityError as erro:
        print(f"RECUSADO | {descricao}")
        print(f"           Motivo: {erro}")


def main():
    conexao = abrir_banco_exemplo()
    try:
        print("=== Chaves estrangeiras LIGADAS ===")
        tentar(
            "Produto com categoria inexistente (id 999)",
            conexao,
            INSERT_PRODUTO,
            ("Produto Fantasma", 999, 10.0, 1),
        )
        tentar(
            "Apagar categoria que tem produtos (Cabos)",
            conexao,
            "DELETE FROM categorias WHERE nome = ?",
            ("Cabos",),
        )
        tentar(
            "Apagar categoria sem produtos (Games)",
            conexao,
            "DELETE FROM categorias WHERE nome = ?",
            ("Games",),
        )
        tentar(
            "Produto em categoria que existe (id 1)",
            conexao,
            INSERT_PRODUTO,
            ("Teclado Sem Fio", 1, 149.90, 7),
        )

        print("\n=== Chaves estrangeiras DESLIGADAS ===")
        conexao.execute("PRAGMA foreign_keys = OFF")
        tentar(
            "Produto com categoria inexistente (id 999)",
            conexao,
            INSERT_PRODUTO,
            ("Produto Fantasma", 999, 10.0, 1),
        )

        orfaos = conexao.execute(
            """
            SELECT p.nome, p.categoria_id
            FROM produtos AS p
            LEFT JOIN categorias AS c ON c.id = p.categoria_id
            WHERE c.id IS NULL
            """
        ).fetchall()
        for orfao in orfaos:
            print(f"Produto órfão: {orfao['nome']} (categoria_id = {orfao['categoria_id']})")
    finally:
        conexao.close()


if __name__ == "__main__":
    main()