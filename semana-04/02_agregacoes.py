"""Agregações SQL: COUNT, SUM, AVG, MIN, MAX, GROUP BY e HAVING."""

from banco_exemplo import abrir_banco_exemplo


def main():
    conexao = abrir_banco_exemplo()
    try:
        resumo = conexao.execute(
            """
            SELECT COUNT(*) AS total_produtos,
                   SUM(quantidade) AS unidades,
                   AVG(preco) AS preco_medio,
                   MIN(preco) AS menor_preco,
                   MAX(preco) AS maior_preco,
                   SUM(preco * quantidade) AS valor_estoque
            FROM produtos
            """
        ).fetchone()

        esgotados = conexao.execute(
            "SELECT COUNT(*) AS total FROM produtos WHERE quantidade = 0"
        ).fetchone()

        print("=== Resumo geral ===")
        print(f"Produtos cadastrados: {resumo['total_produtos']}")
        print(f"Unidades em estoque:  {resumo['unidades']}")
        print(f"Preço médio:          R$ {resumo['preco_medio']:.2f}")
        print(f"Menor preço:          R$ {resumo['menor_preco']:.2f}")
        print(f"Maior preço:          R$ {resumo['maior_preco']:.2f}")
        print(f"Valor do estoque:     R$ {resumo['valor_estoque']:.2f}")
        print(f"Produtos esgotados:   {esgotados['total']}")

        por_categoria = conexao.execute(
            """
            SELECT categoria,
                   COUNT(*) AS total_produtos,
                   SUM(quantidade) AS unidades,
                   ROUND(AVG(preco), 2) AS preco_medio,
                   SUM(preco * quantidade) AS valor_estoque
            FROM produtos
            GROUP BY categoria
            ORDER BY valor_estoque DESC
            """
        ).fetchall()

        print("\n=== Por categoria (maior valor em estoque primeiro) ===")
        print(
            f"{'Categoria':<14} {'Prod.':>5} {'Unid.':>6} "
            f"{'Preço médio':>12} {'Valor estoque':>14}"
        )
        for linha in por_categoria:
            print(
                f"{linha['categoria']:<14} {linha['total_produtos']:>5} "
                f"{linha['unidades']:>6} {linha['preco_medio']:>12.2f} "
                f"{linha['valor_estoque']:>14.2f}"
            )

        com_varios = conexao.execute(
            """
            SELECT categoria, COUNT(*) AS total_produtos
            FROM produtos
            GROUP BY categoria
            HAVING COUNT(*) > 2
            ORDER BY categoria
            """
        ).fetchall()

        print("\n=== Categorias com mais de 2 produtos ===")
        for linha in com_varios:
            print(f"{linha['categoria']}: {linha['total_produtos']} produtos")
    finally:
        conexao.close()


if __name__ == "__main__":
    main()