"""Cria um banco SQLite com duas tabelas relacionadas: categorias e produtos."""

import sqlite3
from pathlib import Path

ARQUIVO_BANCO = Path(__file__).parent / "relacional.db"

CATEGORIAS = ["Periféricos", "Monitores", "Computadores", "Cabos", "Acessórios", "Games"]

PRODUTOS = [
    ("Teclado Mecânico", "Periféricos", 289.90, 15),
    ("Mouse Gamer", "Periféricos", 129.90, 30),
    ("Mouse Pad", "Periféricos", 39.90, 60),
    ("Monitor 24 pol", "Monitores", 749.00, 8),
    ("Monitor 27 pol", "Monitores", 1199.00, 5),
    ("Notebook 15", "Computadores", 3499.00, 4),
    ("Desktop Básico", "Computadores", 2599.00, 3),
    ("Cabo HDMI", "Cabos", 19.90, 120),
    ("Cabo USB-C", "Cabos", 24.90, 90),
    ("Hub USB", "Acessórios", 79.90, 25),
    ("Webcam HD", "Acessórios", 159.90, 12),
    ("Headset", "Acessórios", 199.90, 0),
]


def conectar(arquivo=ARQUIVO_BANCO):
    """Abre o banco com chaves estrangeiras ligadas e linhas acessíveis por nome."""
    conexao = sqlite3.connect(arquivo)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def criar_tabelas(conexao):
    """Cria as tabelas categorias e produtos, se ainda não existirem."""
    conexao.execute(
        """
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE
        )
        """
    )
    conexao.execute(
        """
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            categoria_id INTEGER NOT NULL,
            preco REAL NOT NULL CHECK (preco >= 0),
            quantidade INTEGER NOT NULL DEFAULT 0 CHECK (quantidade >= 0),
            FOREIGN KEY (categoria_id) REFERENCES categorias (id)
        )
        """
    )
    conexao.commit()


def abrir_banco_exemplo():
    """Recria o banco de exemplo do zero e devolve a conexão aberta."""
    conexao = conectar()

    # A ordem importa: primeiro a tabela que depende (produtos), depois a categorias.
    conexao.execute("DROP TABLE IF EXISTS produtos")
    conexao.execute("DROP TABLE IF EXISTS categorias")
    criar_tabelas(conexao)

    ids_categorias = {}
    for nome in CATEGORIAS:
        cursor = conexao.execute("INSERT INTO categorias (nome) VALUES (?)", (nome,))
        ids_categorias[nome] = cursor.lastrowid

    for nome, categoria, preco, quantidade in PRODUTOS:
        conexao.execute(
            "INSERT INTO produtos (nome, categoria_id, preco, quantidade) VALUES (?, ?, ?, ?)",
            (nome, ids_categorias[categoria], preco, quantidade),
        )

    conexao.commit()
    return conexao