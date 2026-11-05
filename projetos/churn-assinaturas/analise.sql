-- Análise de Churn de Assinaturas (PostgreSQL) — dados fictícios

CREATE TABLE assinantes (
    id_assinante      INT PRIMARY KEY,
    plano             VARCHAR(20),
    mensalidade       NUMERIC(6,2),
    data_inicio       DATE,
    data_cancelamento DATE
);
-- \copy assinantes FROM 'dados/assinantes.csv' CSV HEADER NULL ''

-- 1) Churn geral e por plano
SELECT plano,
       COUNT(*)                                          AS assinantes,
       COUNT(data_cancelamento)                          AS cancelados,
       ROUND(100.0 * COUNT(data_cancelamento) / COUNT(*), 1) AS churn_pct
FROM assinantes
GROUP BY ROLLUP (plano)
ORDER BY churn_pct DESC;

-- 2) Em que momento o cliente cancela?
WITH tempo AS (
    SELECT plano, data_cancelamento - data_inicio AS dias
    FROM assinantes
    WHERE data_cancelamento IS NOT NULL
)
SELECT CASE WHEN dias <= 30 THEN '0-30 dias'
            WHEN dias <= 60 THEN '31-60 dias'
            WHEN dias <= 120 THEN '61-120 dias'
            ELSE '120+ dias' END                      AS faixa,
       COUNT(*)                                        AS cancelamentos,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct
FROM tempo
GROUP BY 1
ORDER BY MIN(dias);

-- 3) Retenção por coorte mensal (mês de entrada × meses ativos)
WITH coorte AS (
    SELECT id_assinante,
           DATE_TRUNC('month', data_inicio)::date AS mes_coorte,
           COALESCE(data_cancelamento, DATE '2025-12-31') AS fim
    FROM assinantes
),
meses AS (
    SELECT c.mes_coorte, m.n,
           COUNT(*) FILTER (WHERE c.fim >= c.mes_coorte + (m.n || ' month')::interval) AS ativos,
           COUNT(*) AS total
    FROM coorte c
    CROSS JOIN generate_series(0, 6) AS m(n)
    WHERE c.mes_coorte + (m.n || ' month')::interval <= DATE '2025-12-31'
    GROUP BY c.mes_coorte, m.n
)
SELECT mes_coorte, n AS mes, ROUND(100.0 * ativos / total, 1) AS retencao_pct
FROM meses
ORDER BY mes_coorte, n;

-- 4) Receita mensal perdida com cancelamentos (MRR perdido)
SELECT DATE_TRUNC('month', data_cancelamento)::date AS mes,
       SUM(mensalidade)                             AS mrr_perdido,
       SUM(SUM(mensalidade)) OVER (ORDER BY DATE_TRUNC('month', data_cancelamento)) AS acumulado
FROM assinantes
WHERE data_cancelamento IS NOT NULL
GROUP BY 1
ORDER BY 1;
