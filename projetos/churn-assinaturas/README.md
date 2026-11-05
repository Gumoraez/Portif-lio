# Análise de Churn de Assinaturas (dados fictícios)

**Situação:** um serviço de streaming fictício com 25 mil assinantes perdia clientes sem saber em que momento nem em qual plano.

**Ação:** consultas em PostgreSQL com CTEs, `ROLLUP`, `FILTER` e window functions para medir churn por plano, tempo até o cancelamento, retenção por coorte mensal e receita perdida (`analise.sql`).

**Resultado:**
- 39,8% dos assinantes cancelaram ao longo de 2025.
- 82% dos cancelamentos aconteceram nos **primeiros 60 dias**.
- O plano Básico responde por cerca de 2 em cada 3 cancelamentos precoces.
- Recomendação: priorizar o onboarding e ofertas de upgrade nos dois primeiros meses.

## Dados
`dados/assinantes.csv` — id_assinante, plano, mensalidade, data_inicio, data_cancelamento (vazio = ativo).

## Como rodar
```sql
-- no psql, dentro desta pasta
\i analise.sql   -- cria a tabela
\copy assinantes FROM 'dados/assinantes.csv' CSV HEADER NULL ''
```
