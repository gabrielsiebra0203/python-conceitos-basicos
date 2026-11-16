"""Cria um banco SQLite com produtos de exemplo para praticar consultas SQL."""

import sqlite3
from pathlib import Path

ARQUIVO_BANCO = Path(__file__).parent / "consultas.db"

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


def abrir_banco_exemplo():
    """Recria o banco de exemplo do zero e devolve a conexão aberta."""
    conexao = sqlite3.connect(ARQUIVO_BANCO)
    conexao.row_factory = sqlite3.Row

    conexao.execute("DROP TABLE IF EXISTS produtos")
    conexao.execute(
        """
        CREATE TABLE produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            categoria TEXT NOT NULL,
            preco REAL NOT NULL,
            quantidade INTEGER NOT NULL DEFAULT 0
        )
        """
    )
    conexao.executemany(
        "INSERT INTO produtos (nome, categoria, preco, quantidade) VALUES (?, ?, ?, ?)",
        PRODUTOS,
    )
    conexao.commit()
    return conexao