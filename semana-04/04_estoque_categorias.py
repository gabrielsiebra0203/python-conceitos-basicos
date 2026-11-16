"""Mini-sistema de estoque com categorias: duas tabelas ligadas por chave estrangeira."""

import sqlite3
from pathlib import Path

from banco_relacional import conectar, criar_tabelas

ARQUIVO_ESTOQUE = Path(__file__).parent / "estoque_categorias.db"


# ----------------------------- Camada do banco -----------------------------

def listar_categorias(conexao):
    """Devolve todas as categorias com a quantidade de produtos de cada uma."""
    return conexao.execute(
        """
        SELECT c.id, c.nome, COUNT(p.id) AS total_produtos
        FROM categorias AS c
        LEFT JOIN produtos AS p ON p.categoria_id = c.id
        GROUP BY c.id, c.nome
        ORDER BY c.nome
        """
    ).fetchall()


def buscar_categoria(conexao, id_categoria):
    """Devolve a categoria com esse id, ou None se não existir."""
    return conexao.execute(
        "SELECT id, nome FROM categorias WHERE id = ?", (id_categoria,)
    ).fetchone()


def adicionar_categoria(conexao, nome):
    """Cria uma categoria e devolve o id novo, ou None se o nome já existir."""
    try:
        with conexao:
            cursor = conexao.execute("INSERT INTO categorias (nome) VALUES (?)", (nome,))
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None


def remover_categoria(conexao, id_categoria):
    """Apaga a categoria. Devolve False se o banco recusar (ela ainda tem produtos)."""
    try:
        with conexao:
            conexao.execute("DELETE FROM categorias WHERE id = ?", (id_categoria,))
    except sqlite3.IntegrityError:
        return False
    return True


def adicionar_produto(conexao, nome, categoria_id, preco, quantidade):
    """Cria um produto e devolve o id novo, ou None se o banco recusar."""
    try:
        with conexao:
            cursor = conexao.execute(
                "INSERT INTO produtos (nome, categoria_id, preco, quantidade) "
                "VALUES (?, ?, ?, ?)",
                (nome, categoria_id, preco, quantidade),
            )
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None


def listar_produtos(conexao, categoria_id=None):
    """Devolve os produtos com o nome da categoria, opcionalmente de uma só categoria."""
    sql = """
        SELECT p.id, p.nome, c.nome AS categoria, p.preco, p.quantidade
        FROM produtos AS p
        INNER JOIN categorias AS c ON c.id = p.categoria_id
    """
    parametros = ()
    if categoria_id is not None:
        sql += " WHERE c.id = ?"
        parametros = (categoria_id,)
    sql += " ORDER BY c.nome, p.nome"
    return conexao.execute(sql, parametros).fetchall()


# --------------------------- Camada do usuário -----------------------------

def ler_inteiro(mensagem, minimo=0):
    """Pede um inteiro até o usuário digitar um valor válido."""
    while True:
        try:
            valor = int(input(mensagem))
        except ValueError:
            print("Digite um número inteiro.")
            continue
        if valor < minimo:
            print(f"O valor deve ser pelo menos {minimo}.")
            continue
        return valor


def ler_decimal(mensagem, minimo=0):
    """Pede um número decimal (aceita vírgula ou ponto) até ser válido."""
    while True:
        try:
            valor = float(input(mensagem).replace(",", "."))
        except ValueError:
            print("Digite um número, como 19.90 ou 19,90.")
            continue
        if valor < minimo:
            print(f"O valor deve ser pelo menos {minimo}.")
            continue
        return valor


def mostrar_categorias(categorias):
    """Mostra as categorias em formato de tabela."""
    if not categorias:
        print("Nenhuma categoria cadastrada.")
        return
    print(f"\n{'ID':>3}  {'Categoria':<16} {'Produtos':>8}")
    print("-" * 31)
    for c in categorias:
        print(f"{c['id']:>3}  {c['nome']:<16} {c['total_produtos']:>8}")


def mostrar_produtos(produtos):
    """Mostra os produtos em formato de tabela."""
    if not produtos:
        print("Nenhum produto encontrado.")
        return
    print(f"\n{'ID':>3}  {'Produto':<20} {'Categoria':<14} {'Preço':>10} {'Qtd':>5}")
    print("-" * 57)
    for p in produtos:
        print(
            f"{p['id']:>3}  {p['nome']:<20} {p['categoria']:<14} "
            f"R$ {p['preco']:>7.2f} {p['quantidade']:>5}"
        )


def pedir_categoria(conexao):
    """Pede um ID e devolve a categoria, ou None (avisando) se ela não existir."""
    id_categoria = ler_inteiro("ID da categoria: ", minimo=1)
    categoria = buscar_categoria(conexao, id_categoria)
    if categoria is None:
        print("Categoria não encontrada.")
    return categoria


def opcao_listar_categorias(conexao):
    mostrar_categorias(listar_categorias(conexao))


def opcao_adicionar_categoria(conexao):
    nome = input("Nome da categoria: ").strip()
    if nome == "":
        print("O nome não pode ficar vazio.")
        return
    novo_id = adicionar_categoria(conexao, nome)
    if novo_id is None:
        print(f"Já existe uma categoria chamada '{nome}'.")
    else:
        print(f"Categoria cadastrada com o ID {novo_id}.")


def opcao_adicionar_produto(conexao):
    categorias = listar_categorias(conexao)
    if not categorias:
        print("Cadastre uma categoria antes de adicionar produtos.")
        return

    mostrar_categorias(categorias)
    categoria = pedir_categoria(conexao)
    if categoria is None:
        return

    nome = input("Nome do produto: ").strip()
    if nome == "":
        print("O nome não pode ficar vazio.")
        return
    preco = ler_decimal("Preço: ")
    quantidade = ler_inteiro("Quantidade inicial: ")

    novo_id = adicionar_produto(conexao, nome, categoria["id"], preco, quantidade)
    if novo_id is None:
        print("Não foi possível cadastrar o produto.")
    else:
        print(f"Produto cadastrado com o ID {novo_id} na categoria {categoria['nome']}.")


def opcao_listar_produtos(conexao):
    mostrar_produtos(listar_produtos(conexao))


def opcao_produtos_da_categoria(conexao):
    mostrar_categorias(listar_categorias(conexao))
    categoria = pedir_categoria(conexao)
    if categoria is None:
        return
    mostrar_produtos(listar_produtos(conexao, categoria["id"]))


def opcao_remover_categoria(conexao):
    mostrar_categorias(listar_categorias(conexao))
    categoria = pedir_categoria(conexao)
    if categoria is None:
        return
    resposta = input(f"Remover a categoria '{categoria['nome']}'? (s/n): ").strip().lower()
    if resposta != "s":
        print("Remoção cancelada.")
    elif remover_categoria(conexao, categoria["id"]):
        print("Categoria removida.")
    else:
        print("Não foi possível remover: a categoria ainda tem produtos.")


def exibir_menu():
    print("\n===== ESTOQUE COM CATEGORIAS =====")
    print("1 - Listar categorias")
    print("2 - Adicionar categoria")
    print("3 - Adicionar produto")
    print("4 - Listar todos os produtos")
    print("5 - Listar produtos de uma categoria")
    print("6 - Remover categoria")
    print("0 - Sair")


def main():
    acoes = {
        "1": opcao_listar_categorias,
        "2": opcao_adicionar_categoria,
        "3": opcao_adicionar_produto,
        "4": opcao_listar_produtos,
        "5": opcao_produtos_da_categoria,
        "6": opcao_remover_categoria,
    }

    conexao = conectar(ARQUIVO_ESTOQUE)
    try:
        criar_tabelas(conexao)
        while True:
            exibir_menu()
            opcao = input("Escolha uma opção: ").strip()

            if opcao == "0":
                print("Até logo!")
                break

            acao = acoes.get(opcao)
            if acao is None:
                print("Opção inválida.")
                continue
            acao(conexao)
    finally:
        conexao.close()


if __name__ == "__main__":
    main()