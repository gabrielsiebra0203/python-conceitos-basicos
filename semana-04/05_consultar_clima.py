"""Consultas de verificação sobre os dados de clima coletados."""

import sqlite3
from pathlib import Path

ARQUIVO_BANCO = Path(__file__).parent / "clima.db"


def formatar(valor, sufixo=""):
    """Mostra um traço quando a API não trouxe valor para o dia."""
    if valor is None:
        return "-"
    return f"{valor:.1f}{sufixo}"


def main():
    if not ARQUIVO_BANCO.exists():
        print("Banco não encontrado. Rode antes: python semana-04/05_clima_banco.py")
        return

    conexao = sqlite3.connect(ARQUIVO_BANCO)
    conexao.row_factory = sqlite3.Row
    try:
        total = conexao.execute("SELECT COUNT(*) AS total FROM previsoes").fetchone()
        print(f"Registros em previsoes: {total['total']}")

        duplicados = conexao.execute(
            """
            SELECT cidade_id, data, COUNT(*) AS vezes
            FROM previsoes
            GROUP BY cidade_id, data
            HAVING COUNT(*) > 1
            """
        ).fetchall()
        print(f"Registros duplicados: {len(duplicados)}")

        print("\nOs 5 dias com mais chuva prevista:")
        chuvosos = conexao.execute(
            """
            SELECT c.nome AS cidade, p.data, p.chuva_mm
            FROM previsoes AS p
            INNER JOIN cidades AS c ON c.id = p.cidade_id
            WHERE p.chuva_mm IS NOT NULL
            ORDER BY p.chuva_mm DESC
            LIMIT 5
            """
        ).fetchall()
        for linha in chuvosos:
            print(f"  {linha['data']}  {linha['cidade']:<12} {formatar(linha['chuva_mm'], ' mm')}")

        cidade = input("\nVer a previsão de qual cidade? (ENTER para sair): ").strip()
        if cidade == "":
            return

        linhas = conexao.execute(
            """
            SELECT c.nome AS cidade, p.data, p.temp_min, p.temp_max, p.chuva_mm
            FROM previsoes AS p
            INNER JOIN cidades AS c ON c.id = p.cidade_id
            WHERE c.nome LIKE ?
            ORDER BY c.nome, p.data
            """,
            (f"%{cidade}%",),
        ).fetchall()

        if not linhas:
            print("Nenhuma previsão encontrada para essa cidade.")
            return

        print(f"\n{'Cidade':<12} {'Data':<11} {'Mín':>6} {'Máx':>6} {'Chuva':>9}")
        for linha in linhas:
            print(
                f"{linha['cidade']:<12} {linha['data']:<11} {formatar(linha['temp_min']):>6} "
                f"{formatar(linha['temp_max']):>6} {formatar(linha['chuva_mm'], ' mm'):>9}"
            )
    finally:
        conexao.close()


if __name__ == "__main__":
    main()