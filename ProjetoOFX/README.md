# ProjetoOFX

Leitura de extrato bancário no formato OFX com Python, com carga opcional em PostgreSQL (processo ETL simplificado).

## Estrutura

```
ProjetoOFX
├── main.py            # leitura, exibição e totais (+ chamada ao banco com --banco)
├── banco.py           # desafio extra: gravação no PostgreSQL sem duplicatas
├── schema.sql         # criação da tabela + consultas de validação
├── extrato.ofx        # arquivo de entrada
├── requirements.txt
└── README.md
```

## Como executar

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt

python main.py                 # parte principal
python main.py --banco         # parte principal + gravação no PostgreSQL
```

## Banco de dados (desafio extra)

1. Crie/escolha um banco no PostgreSQL.
2. Defina as variáveis de ambiente (ou edite `CONFIG` em `banco.py`):
   `PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER`, `PGPASSWORD`.
3. Execute `python main.py --banco` (a tabela é criada automaticamente; o `schema.sql` serve de referência).
4. No DBeaver, conecte no mesmo banco e rode `SELECT * FROM movimentacoes;`.

### Bônus: sem duplicatas

A tabela possui `UNIQUE (data_movimentacao, valor, descricao)` e o `INSERT` usa `ON CONFLICT DO NOTHING`. Rodar o programa várias vezes não duplica registros: na segunda execução, todas as linhas aparecem como "ignoradas".

## Conceito

Extração (leitura do OFX) → Transformação (cálculo de entradas/saídas/saldo, ajuste de tipos) → Carga (INSERT no PostgreSQL).
