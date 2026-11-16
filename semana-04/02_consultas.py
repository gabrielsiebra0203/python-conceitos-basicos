"""Consultas SQL: WHERE, ORDER BY, LIMIT, LIKE, BETWEEN e IN."""

from banco_exemplo import abrir_banco_exemplo

# Constante nossa, sem dados digitados por usuário, por isso é seguro juntar com texto.
SELECT_BASE = "SELECT nome, categoria, preco, quantidade FROM produtos"


def mostrar(titulo, conexao, sql, parametros=()):
    """Executa uma consulta e mostra o resultado em formato de tabela."""
    linhas = conexao.execute(sql, parametros).fetchall()

    print(f"\n=== {titulo} ===")
    print(f"SQL: {sql}")
    print(f"Resultado: {len(linhas)} linha(s)")
    for linha in linhas:
        print(
            f"  {linha['nome']:<18} {linha['categoria']:<13} "
            f"R$ {linha['preco']:>8.2f} {linha['quantidade']:>4} un."
        )


def main():
    conexao = abrir_banco_exemplo()
    try:
        mostrar("1. Todos os produtos", conexao, SELECT_BASE)
        mostrar("2. Preço maior que 100", conexao, SELECT_BASE + " WHERE preco > 100")
        mostrar(
            "3. Só da categoria Periféricos",
            conexao,
            SELECT_BASE + " WHERE categoria = ?",
            ("Periféricos",),
        )
        mostrar(
            "4. Preço entre 50 e 300 e com estoque",
            conexao,
            SELECT_BASE + " WHERE preco BETWEEN 50 AND 300 AND quantidade > 0",
        )
        mostrar("5. Do mais caro ao mais barato", conexao, SELECT_BASE + " ORDER BY preco DESC")
        mostrar("6. Os 3 mais caros", conexao, SELECT_BASE + " ORDER BY preco DESC LIMIT 3")
        mostrar("7. Nome contém 'mouse'", conexao, SELECT_BASE + " WHERE nome LIKE '%mouse%'")
        mostrar(
            "8. Categorias Cabos ou Acessórios",
            conexao,
            SELECT_BASE + " WHERE categoria IN ('Cabos', 'Acessórios')",
        )
        mostrar("9. Produtos esgotados", conexao, SELECT_BASE + " WHERE quantidade = 0")
    finally:
        conexao.close()


if __name__ == "__main__":
    main()