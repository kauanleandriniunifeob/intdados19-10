"""Desafio extra: grava as movimentações do OFX no PostgreSQL.

Bônus: impede duplicatas de duas formas:
  1. Constraint UNIQUE na tabela (garantia no banco);
  2. INSERT ... ON CONFLICT DO NOTHING (o programa pode rodar várias
     vezes sobre o mesmo arquivo sem duplicar registros).

Configure a conexão por variáveis de ambiente (ou use os padrões abaixo):
    PGHOST, PGPORT, PGDATABASE, PGUSER, PGPASSWORD
"""
import os

import psycopg2

CONFIG = {
    "host": os.getenv("PGHOST", "localhost"),
    "port": os.getenv("PGPORT", "5432"),
    "dbname": os.getenv("PGDATABASE", "postgres"),
    "user": os.getenv("PGUSER", "postgres"),
    "password": os.getenv("PGPASSWORD", "postgres"),
}

SQL_CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS movimentacoes (
    id SERIAL PRIMARY KEY,
    data_movimentacao DATE,
    valor NUMERIC(15,2),
    descricao VARCHAR(255),
    CONSTRAINT uq_movimentacao UNIQUE (data_movimentacao, valor, descricao)
);
"""

SQL_INSERIR = """
INSERT INTO movimentacoes (data_movimentacao, valor, descricao)
VALUES (%s, %s, %s)
ON CONFLICT ON CONSTRAINT uq_movimentacao DO NOTHING;
"""


def gravar_transacoes(transacoes):
    """Insere as transações. Retorna (inseridas, duplicadas)."""
    inseridas = 0
    duplicadas = 0

    conexao = psycopg2.connect(**CONFIG)
    try:
        with conexao:  # commit automático; rollback em caso de erro
            with conexao.cursor() as cursor:
                cursor.execute(SQL_CRIAR_TABELA)

                for t in transacoes:
                    cursor.execute(
                        SQL_INSERIR,
                        (t.date.date(), t.amount, (t.memo or "")[:255]),
                    )
                    # rowcount = 1 se inseriu, 0 se foi ignorada por duplicidade
                    if cursor.rowcount == 1:
                        inseridas += 1
                    else:
                        duplicadas += 1
    finally:
        conexao.close()

    return inseridas, duplicadas
