"""UPDATE e DELETE: alterando e removendo linhas, e desfazendo com rollback."""

from banco_exemplo import abrir_banco_exemplo

CONSULTA_CABOS = "SELECT nome, preco, quantidade FROM produtos WHERE categoria = 'Cabos'"
CONSULTA_PRIMEIROS = "SELECT nome, preco, quantidade FROM produtos ORDER BY id LIMIT 3"


def mostrar(conexao, titulo, sql):
    """Mostra o resultado de um SELECT com nome, preço e quantidade."""
    print(f"\n--- {titulo} ---")
    for linha in conexao.execute(sql).fetchall():
        print(f"  {linha['nome']:<18} R$ {linha['preco']:>8.2f} {linha['quantidade']:>4} un.")


def main():
    conexao = abrir_banco_exemplo()
    try:
        # 1. UPDATE com WHERE: altera só o produto indicado
        cursor = conexao.execute(
            "UPDATE produtos SET preco = ? WHERE nome = ?", (259.90, "Teclado Mecânico")
        )
        print(f"1. Novo preço do teclado: {cursor.rowcount} linha(s) alterada(s)")

        # 2. UPDATE com cálculo: reajuste de 10% nos cabos
        mostrar(conexao, "Cabos antes do reajuste", CONSULTA_CABOS)
        cursor = conexao.execute(
            "UPDATE produtos SET preco = ROUND(preco * 1.10, 2) WHERE categoria = ?",
            ("Cabos",),
        )
        print(f"\n2. Reajuste de 10%: {cursor.rowcount} linha(s) alterada(s)")
        mostrar(conexao, "Cabos depois do reajuste", CONSULTA_CABOS)

        # 3. UPDATE somando ao valor que já existe
        cursor = conexao.execute(
            "UPDATE produtos SET quantidade = quantidade + ? WHERE nome = ?",
            (10, "Mouse Pad"),
        )
        print(f"\n3. Entrada de estoque: {cursor.rowcount} linha(s) alterada(s)")

        # 4. DELETE com WHERE: remove os produtos esgotados
        cursor = conexao.execute("DELETE FROM produtos WHERE quantidade = 0")
        print(f"4. Esgotados removidos: {cursor.rowcount} linha(s)")

        # 5. DELETE sem correspondência: não dá erro, só afeta 0 linhas
        cursor = conexao.execute(
            "DELETE FROM produtos WHERE nome = ?", ("Produto Inexistente",)
        )
        print(f"5. Produto inexistente: {cursor.rowcount} linha(s)")

        conexao.commit()
        total = conexao.execute("SELECT COUNT(*) AS total FROM produtos").fetchone()
        print(f"\nProdutos restantes: {total['total']}")

        # 6. O perigo do UPDATE sem WHERE... e como o rollback salva
        conexao.execute("UPDATE produtos SET preco = 0")
        mostrar(conexao, "Depois do UPDATE SEM WHERE (desastre!)", CONSULTA_PRIMEIROS)

        conexao.rollback()
        mostrar(conexao, "Depois do rollback (tudo restaurado)", CONSULTA_PRIMEIROS)
    finally:
        conexao.close()


if __name__ == "__main__":
    main()