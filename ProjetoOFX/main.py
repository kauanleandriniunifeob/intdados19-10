"""Leitura de extrato bancário OFX.

Exibe cada movimentação (data, valor, descrição), a quantidade total e,
ao final, total de entradas, total de saídas e saldo calculado.

Uso:
    python main.py                 # apenas leitura e totais
    python main.py --banco         # além disso, grava no PostgreSQL (desafio extra)
"""
import sys
from decimal import Decimal

from ofxparse import OfxParser

ARQUIVO_OFX = "extrato.ofx"


def ler_transacoes(caminho=ARQUIVO_OFX):
    with open(caminho, "rb") as arquivo:
        ofx = OfxParser.parse(arquivo)
    return ofx, ofx.account.statement.transactions


def formatar_brl(valor):
    """Formata como R$ 1.234,56 (padrão brasileiro)."""
    texto = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


def exibir_extrato(transacoes):
    print("=" * 60)
    print("EXTRATO BANCÁRIO")
    print("=" * 60)

    for t in transacoes:
        print(
            f"Data      : {t.date.strftime('%d/%m/%Y')}\n"
            f"Valor     : {formatar_brl(t.amount)}\n"
            f"Descrição : {t.memo}\n"
            + "-" * 60
        )

    print(f"Quantidade total de movimentações: {len(transacoes)}")


def exibir_totais(transacoes):
    entradas = Decimal("0")
    saidas = Decimal("0")

    for t in transacoes:
        if t.amount > 0:
            entradas += t.amount
        else:
            saidas += t.amount

    saldo = entradas + saidas

    print("=" * 60)
    print("RESUMO")
    print("=" * 60)
    print(f"Total de entradas : {formatar_brl(entradas)}")
    print(f"Total de saídas   : {formatar_brl(saidas)}")
    print(f"Saldo calculado   : {formatar_brl(saldo)}")


def main():
    ofx, transacoes = ler_transacoes()

    exibir_extrato(transacoes)
    exibir_totais(transacoes)

    if "--banco" in sys.argv:
        from banco import gravar_transacoes

        print("=" * 60)
        print("GRAVAÇÃO NO POSTGRESQL")
        print("=" * 60)
        inseridas, duplicadas = gravar_transacoes(transacoes)
        print(f"Inseridas : {inseridas}")
        print(f"Ignoradas (duplicadas): {duplicadas}")


if __name__ == "__main__":
    main()
