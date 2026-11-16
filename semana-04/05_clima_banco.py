"""Coleta a previsão do tempo (API Open-Meteo) e grava no SQLite sem duplicar registros."""

import logging
import sqlite3
from datetime import datetime
from pathlib import Path

import requests

ARQUIVO_BANCO = Path(__file__).parent / "clima.db"
ARQUIVO_LOG = Path(__file__).parent / "clima.log"
URL_API = "https://api.open-meteo.com/v1/forecast"

CIDADES = [
    ("Fortaleza", -3.73, -38.52),
    ("São Paulo", -23.55, -46.63),
    ("Recife", -8.05, -34.88),
]


# ------------------------------- Banco de dados -------------------------------

def conectar():
    """Abre o banco com chaves estrangeiras ligadas e linhas acessíveis por nome."""
    conexao = sqlite3.connect(ARQUIVO_BANCO)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def criar_tabelas(conexao):
    """Cria as tabelas cidades e previsoes, se ainda não existirem."""
    conexao.execute(
        """
        CREATE TABLE IF NOT EXISTS cidades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL
        )
        """
    )
    conexao.execute(
        """
        CREATE TABLE IF NOT EXISTS previsoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cidade_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            temp_max REAL,
            temp_min REAL,
            chuva_mm REAL,
            coletado_em TEXT NOT NULL,
            UNIQUE (cidade_id, data),
            FOREIGN KEY (cidade_id) REFERENCES cidades (id)
        )
        """
    )
    conexao.commit()


def garantir_cidade(conexao, nome, latitude, longitude):
    """Cadastra a cidade se ela ainda não existir e devolve o id dela."""
    conexao.execute(
        "INSERT OR IGNORE INTO cidades (nome, latitude, longitude) VALUES (?, ?, ?)",
        (nome, latitude, longitude),
    )
    linha = conexao.execute("SELECT id FROM cidades WHERE nome = ?", (nome,)).fetchone()
    return linha["id"]


def salvar_previsoes(conexao, cidade_id, previsoes):
    """Grava as previsões com UPSERT. Devolve (quantidade de novas, quantidade atualizadas)."""
    coletado_em = datetime.now().isoformat(timespec="seconds")
    novas = 0
    atualizadas = 0

    for previsao in previsoes:
        ja_existia = conexao.execute(
            "SELECT 1 FROM previsoes WHERE cidade_id = ? AND data = ?",
            (cidade_id, previsao["data"]),
        ).fetchone()

        conexao.execute(
            """
            INSERT INTO previsoes (cidade_id, data, temp_max, temp_min, chuva_mm, coletado_em)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT (cidade_id, data) DO UPDATE SET
                temp_max = excluded.temp_max,
                temp_min = excluded.temp_min,
                chuva_mm = excluded.chuva_mm,
                coletado_em = excluded.coletado_em
            """,
            (
                cidade_id,
                previsao["data"],
                previsao["temp_max"],
                previsao["temp_min"],
                previsao["chuva_mm"],
                coletado_em,
            ),
        )

        if ja_existia:
            atualizadas += 1
        else:
            novas += 1

    return novas, atualizadas


# ----------------------------------- API ------------------------------------

def buscar_previsao(latitude, longitude, dias=7):
    """Consulta a API e devolve uma lista de dicionários, um por dia."""
    parametros = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "auto",
        "forecast_days": dias,
    }
    resposta = requests.get(URL_API, params=parametros, timeout=10)
    resposta.raise_for_status()
    diario = resposta.json()["daily"]

    previsoes = []
    for data, temp_max, temp_min, chuva in zip(
        diario["time"],
        diario["temperature_2m_max"],
        diario["temperature_2m_min"],
        diario["precipitation_sum"],
    ):
        previsoes.append(
            {"data": data, "temp_max": temp_max, "temp_min": temp_min, "chuva_mm": chuva}
        )
    return previsoes


# --------------------------------- Pipeline ---------------------------------

def coletar(conexao):
    """Busca e grava a previsão de cada cidade. Devolve a quantidade de erros."""
    erros = 0

    for nome, latitude, longitude in CIDADES:
        try:
            previsoes = buscar_previsao(latitude, longitude)
        except requests.exceptions.RequestException as erro:
            logging.error("Falha ao consultar a API para %s: %s", nome, erro)
            erros += 1
            continue
        except (KeyError, ValueError) as erro:
            logging.error("Resposta inesperada da API para %s: %s", nome, erro)
            erros += 1
            continue

        with conexao:
            cidade_id = garantir_cidade(conexao, nome, latitude, longitude)
            novas, atualizadas = salvar_previsoes(conexao, cidade_id, previsoes)

        logging.info("%s: %d nova(s), %d atualizada(s)", nome, novas, atualizadas)

    return erros


def mostrar_resumo(conexao):
    """Mostra um resumo por cidade, calculado direto pelo banco."""
    linhas = conexao.execute(
        """
        SELECT c.nome AS cidade,
               COUNT(p.id) AS dias,
               ROUND(AVG(p.temp_max), 1) AS media_max,
               ROUND(MIN(p.temp_min), 1) AS minima,
               ROUND(MAX(p.temp_max), 1) AS maxima,
               ROUND(COALESCE(SUM(p.chuva_mm), 0), 1) AS chuva_total
        FROM cidades AS c
        INNER JOIN previsoes AS p ON p.cidade_id = c.id
        GROUP BY c.id, c.nome
        ORDER BY media_max DESC
        """
    ).fetchall()

    print(f"\n{'Cidade':<12} {'Dias':>4} {'Média máx':>10} {'Mín':>6} {'Máx':>6} {'Chuva mm':>9}")
    print("-" * 52)
    for linha in linhas:
        print(
            f"{linha['cidade']:<12} {linha['dias']:>4} {linha['media_max']:>10.1f} "
            f"{linha['minima']:>6.1f} {linha['maxima']:>6.1f} {linha['chuva_total']:>9.1f}"
        )


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%H:%M:%S",
        handlers=[logging.FileHandler(ARQUIVO_LOG, encoding="utf-8"), logging.StreamHandler()],
    )

    conexao = conectar()
    try:
        criar_tabelas(conexao)
        erros = coletar(conexao)
        mostrar_resumo(conexao)
        if erros:
            logging.warning("Coleta concluída com %d erro(s).", erros)
    finally:
        conexao.close()


if __name__ == "__main__":
    main()