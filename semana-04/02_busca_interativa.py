"""Busca de produtos por parte do nome, usando parâmetros seguros."""

from banco_exemplo import abrir_banco_exemplo


def buscar_produtos(conexao, termo):
    """Devolve os produtos cujo nome contém o termo, do mais barato ao mais caro."""
    return conexao.execute(
        "SELECT nome, categoria, preco, quantidade FROM produtos "
        "WHERE nome LIKE ? ORDER BY preco",
        (f"%{termo}%",),
    ).fetchall()


def main():
    conexao = abrir_banco_exemplo()
    try:
        while True:
            termo = input("\nBuscar produto (ENTER para sair): ").strip()
            if termo == "":
                print("Até logo!")
                break

            produtos = buscar_produtos(conexao, termo)
            if not produtos:
                print("Nenhum produto encontrado.")
                continue

            for produto in produtos:
                print(
                    f"{produto['nome']:<18} R$ {produto['preco']:>8.2f} "
                    f"({produto['quantidade']} un.)"
                )
    finally:
        conexao.close()


if __name__ == "__main__":
    main()