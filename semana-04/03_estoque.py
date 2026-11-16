"""Mini-sistema de estoque no terminal: CRUD completo com SQLite."""

import sqlite3
from pathlib import Path

ARQUIVO_BANCO = Path(__file__).parent / "estoque.db"


# ----------------------------- Camada do banco -----------------------------

def conectar():
    """Abre o banco, cria a tabela se preciso e devolve a conexão."""
    conexao = sqlite3.connect(ARQUIVO_BANCO)
    conexao.row_factory = sqlite3.Row
    conexao.execute(
        """
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            preco REAL NOT NULL CHECK (preco >= 0),
            quantidade INTEGER NOT NULL DEFAULT 0 CHECK (quantidade >= 0)
        )
        """
    )
    conexao.commit()
    return conexao


def adicionar_produto(conexao, nome, preco, quantidade):
    """Cria um produto e devolve o id novo, ou None se o banco recusar."""
    try:
        with conexao:
            cursor = conexao.execute(
                "INSERT INTO produtos (nome, preco, quantidade) VALUES (?, ?, ?)",
                (nome, preco, quantidade),
            )
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None


def listar_produtos(conexao):
    """Devolve todos os produtos em ordem alfabética."""
    return conexao.execute(
        "SELECT id, nome, preco, quantidade FROM produtos ORDER BY nome"
    ).fetchall()


def buscar_por_nome(conexao, termo):
    """Devolve os produtos cujo nome contém o termo."""
    return conexao.execute(
        "SELECT id, nome, preco, quantidade FROM produtos WHERE nome LIKE ? ORDER BY nome",
        (f"%{termo}%",),
    ).fetchall()


def buscar_produto(conexao, id_produto):
    """Devolve o produto com esse id, ou None se não existir."""
    return conexao.execute(
        "SELECT id, nome, preco, quantidade FROM produtos WHERE id = ?",
        (id_produto,),
    ).fetchone()


def atualizar_preco(conexao, id_produto, novo_preco):
    """Altera o preço. Devolve True se algum produto foi alterado."""
    with conexao:
        cursor = conexao.execute(
            "UPDATE produtos SET preco = ? WHERE id = ?", (novo_preco, id_produto)
        )
    return cursor.rowcount > 0


def movimentar_estoque(conexao, id_produto, variacao):
    """Soma (entrada) ou subtrai (saída, valor negativo) unidades do estoque.

    Devolve False se o banco recusar, por exemplo ao deixar o estoque negativo.
    """
    try:
        with conexao:
            cursor = conexao.execute(
                "UPDATE produtos SET quantidade = quantidade + ? WHERE id = ?",
                (variacao, id_produto),
            )
    except sqlite3.IntegrityError:
        return False
    return cursor.rowcount > 0


def remover_produto(conexao, id_produto):
    """Apaga o produto. Devolve True se algum produto foi removido."""
    with conexao:
        cursor = conexao.execute("DELETE FROM produtos WHERE id = ?", (id_produto,))
    return cursor.rowcount > 0


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


def mostrar_tabela(produtos):
    """Mostra uma lista de produtos em formato de tabela."""
    if not produtos:
        print("Nenhum produto encontrado.")
        return
    print(f"\n{'ID':>3}  {'Produto':<20} {'Preço':>10} {'Qtd':>5}")
    print("-" * 42)
    for p in produtos:
        print(f"{p['id']:>3}  {p['nome']:<20} R$ {p['preco']:>7.2f} {p['quantidade']:>5}")


def pedir_produto(conexao):
    """Pede um ID e devolve o produto, ou None (avisando) se ele não existir."""
    id_produto = ler_inteiro("ID do produto: ", minimo=1)
    produto = buscar_produto(conexao, id_produto)
    if produto is None:
        print("Produto não encontrado.")
    return produto


def opcao_adicionar(conexao):
    nome = input("Nome do produto: ").strip()
    if nome == "":
        print("O nome não pode ficar vazio.")
        return
    preco = ler_decimal("Preço: ")
    quantidade = ler_inteiro("Quantidade inicial: ")

    novo_id = adicionar_produto(conexao, nome, preco, quantidade)
    if novo_id is None:
        print(f"Não foi possível adicionar: já existe um produto chamado '{nome}'.")
    else:
        print(f"Produto cadastrado com o ID {novo_id}.")


def opcao_listar(conexao):
    mostrar_tabela(listar_produtos(conexao))


def opcao_buscar(conexao):
    termo = input("Parte do nome: ").strip()
    mostrar_tabela(buscar_por_nome(conexao, termo))


def opcao_atualizar_preco(conexao):
    produto = pedir_produto(conexao)
    if produto is None:
        return
    print(f"Preço atual de {produto['nome']}: R$ {produto['preco']:.2f}")
    novo_preco = ler_decimal("Novo preço: ")
    atualizar_preco(conexao, produto["id"], novo_preco)
    print("Preço atualizado.")


def opcao_entrada(conexao):
    produto = pedir_produto(conexao)
    if produto is None:
        return
    quantidade = ler_inteiro("Unidades que entraram: ", minimo=1)
    movimentar_estoque(conexao, produto["id"], quantidade)
    print(f"Entrada registrada. Estoque de {produto['nome']}: {produto['quantidade'] + quantidade}")


def opcao_saida(conexao):
    produto = pedir_produto(conexao)
    if produto is None:
        return
    quantidade = ler_inteiro("Unidades que saíram: ", minimo=1)
    if movimentar_estoque(conexao, produto["id"], -quantidade):
        print(f"Saída registrada. Estoque de {produto['nome']}: {produto['quantidade'] - quantidade}")
    else:
        print(f"Estoque insuficiente: há apenas {produto['quantidade']} unidade(s).")


def opcao_remover(conexao):
    produto = pedir_produto(conexao)
    if produto is None:
        return
    resposta = input(f"Remover '{produto['nome']}'? (s/n): ").strip().lower()
    if resposta == "s":
        remover_produto(conexao, produto["id"])
        print("Produto removido.")
    else:
        print("Remoção cancelada.")


def exibir_menu():
    print("\n===== ESTOQUE =====")
    print("1 - Adicionar produto")
    print("2 - Listar produtos")
    print("3 - Buscar por nome")
    print("4 - Atualizar preço")
    print("5 - Entrada de estoque")
    print("6 - Saída de estoque")
    print("7 - Remover produto")
    print("0 - Sair")


def main():
    acoes = {
        "1": opcao_adicionar,
        "2": opcao_listar,
        "3": opcao_buscar,
        "4": opcao_atualizar_preco,
        "5": opcao_entrada,
        "6": opcao_saida,
        "7": opcao_remover,
    }

    conexao = conectar()
    try:
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