-- Tabela do enunciado + restrição UNIQUE (bônus: impede transações duplicadas)
CREATE TABLE IF NOT EXISTS movimentacoes (
    id SERIAL PRIMARY KEY,
    data_movimentacao DATE,
    valor NUMERIC(15,2),
    descricao VARCHAR(255),
    CONSTRAINT uq_movimentacao UNIQUE (data_movimentacao, valor, descricao)
);

-- Consultas úteis para validar no DBeaver
-- SELECT * FROM movimentacoes ORDER BY data_movimentacao;
-- SELECT COUNT(*) FROM movimentacoes;
-- SELECT SUM(valor) FILTER (WHERE valor > 0) AS entradas,
--        SUM(valor) FILTER (WHERE valor < 0) AS saidas,
--        SUM(valor)                          AS saldo
--   FROM movimentacoes;
