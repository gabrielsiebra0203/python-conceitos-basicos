"""JOIN: juntando produtos e categorias com INNER JOIN e LEFT JOIN."""

from banco_relacional import abrir_banco_exemplo


def formatar(valor):
    """Formata um valor para exibição: decimais com 2 casas, o resto como texto."""
    if isinstance(valor, float):
        return f"{valor:.2f}"
    return str(valor)


def mostrar(titulo, conexao, sql):
    """Executa uma consulta e mostra o SQL e o resultado."""
    linhas = conexao.execute(sql).fetchall()

    print(f"\n=== {titulo} ===")
    print(f"SQL: {' '.join(sql.split())}")
    print(f"Resultado: {len(linhas)} linha(s)")
    for linha in linhas:
        print("  " + " | ".join(formatar(linha[coluna]) for coluna in linha.keys()))


def main():
    conexao = abrir_banco_exemplo()
    try:
        mostrar(
            "1. Produtos com o nome da categoria (INNER JOIN)",
            conexao,
            """
            SELECT p.nome AS produto, c.nome AS categoria, p.preco
            FROM produtos AS p
            INNER JOIN categorias AS c ON c.id = p.categoria_id
            ORDER BY c.nome, p.nome
            """,
        )

        mostrar(
            "2. Só os produtos da categoria Cabos",
            conexao,
            """
            SELECT p.nome AS produto, p.preco, p.quantidade
            FROM produtos AS p
            INNER JOIN categorias AS c ON c.id = p.categoria_id
            WHERE c.nome = 'Cabos'
            """,
        )

        mostrar(
            "3. Total por categoria (INNER JOIN)",
            conexao,
            """
            SELECT c.nome AS categoria,
                   COUNT(*) AS produtos,
                   SUM(p.preco * p.quantidade) AS valor_estoque
            FROM categorias AS c
            INNER JOIN produtos AS p ON p.categoria_id = c.id
            GROUP BY c.id, c.nome
            ORDER BY valor_estoque DESC
            """,
        )

        mostrar(
            "4. Total por categoria (LEFT JOIN)",
            conexao,
            """
            SELECT c.nome AS categoria,
                   COUNT(p.id) AS produtos,
                   COALESCE(SUM(p.preco * p.quantidade), 0) AS valor_estoque
            FROM categorias AS c
            LEFT JOIN produtos AS p ON p.categoria_id = c.id
            GROUP BY c.id, c.nome
            ORDER BY valor_estoque DESC
            """,
        )

        mostrar(
            "5. Categorias sem nenhum produto",
            conexao,
            """
            SELECT c.nome AS categoria
            FROM categorias AS c
            LEFT JOIN produtos AS p ON p.categoria_id = c.id
            WHERE p.id IS NULL
            """,
        )

        mostrar(
            "6. Os 3 produtos mais caros e suas categorias",
            conexao,
            """
            SELECT p.nome AS produto, c.nome AS categoria, p.preco
            FROM produtos AS p
            INNER JOIN categorias AS c ON c.id = p.categoria_id
            ORDER BY p.preco DESC
            LIMIT 3
            """,
        )
    finally:
        conexao.close()


if __name__ == "__main__":
    main()