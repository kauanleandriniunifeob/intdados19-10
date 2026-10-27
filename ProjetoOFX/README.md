# Atividade OFX - Integração de Dados

Programa em Python que lê um extrato bancário no formato OFX e mostra as movimentações na tela. Também tem a parte extra de salvar tudo no PostgreSQL.

## O que o programa faz

- Lê o arquivo `extrato.ofx` com a biblioteca `ofxparse`
- Mostra data, valor e descrição de cada movimentação
- Mostra quantas movimentações foram encontradas
- Calcula o total de entradas, o total de saídas e o saldo

## Como rodar

Precisa ter o Python instalado.

```
pip install -r requirements.txt
python main.py
```

Para salvar no banco também:

```
python main.py --banco
```

## Parte do PostgreSQL

O arquivo `banco.py` conecta no banco com o `psycopg2` e insere cada movimentação na tabela `movimentacoes`. A tabela é criada sozinha se ainda não existir (o `schema.sql` tem o mesmo comando).

Os dados de conexão ficam nas variáveis de ambiente `PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER` e `PGPASSWORD`. Se não definir nada, ele usa localhost, porta 5432 e usuário postgres.

Para conferir, abri a tabela no DBeaver e rodei:

```
SELECT * FROM movimentacoes;
```

### Evitando duplicados (desafio bônus)

Coloquei uma restrição UNIQUE em data, valor e descrição, e o INSERT usa `ON CONFLICT DO NOTHING`. Assim, se rodar o programa de novo com o mesmo arquivo, ele não grava as linhas repetidas e avisa quantas foram ignoradas.

## Observação

O saldo calculado (R$ 11.840,30) é diferente do saldo que vem no final do arquivo OFX (R$ 12.030,20). Isso acontece porque o extrato só tem as movimentações de 01/10 a 17/10 e não mostra o saldo que a conta já tinha antes.
