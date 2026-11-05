# Dashboard de Vendas de Varejo (dados fictícios)

**Situação:** uma rede fictícia de 12 lojas teve queda de faturamento no 2º semestre de 2025 e não sabia a causa.

**Ação:** modelo estrela no Power BI (`fato_vendas` + `dim_loja`, `dim_produto` e calendário) e medidas DAX de faturamento, ticket médio, variação entre semestres e mix de categorias (`medidas.dax`).

**Resultado:**
- Faturamento anual de R$ 82,9 mi, com queda de 7,3% do 1º para o 2º semestre.
- Ticket médio caiu 8,6% (R$ 2.192 → R$ 2.003).
- 3 lojas (Rio de Janeiro, Florianópolis e Recife) concentram toda a queda; as demais cresceram levemente.
- Causa: nessas lojas o mix migrou para Acessórios, itens de baixo valor.

## Dados (`dados/`)
| Arquivo | Linhas | Conteúdo |
|---|---|---|
| fato_vendas.csv | ~39,5 mil | id_venda, data, id_loja, id_produto, quantidade, valor |
| dim_loja.csv | 12 | id_loja, loja, cidade |
| dim_produto.csv | 40 | id_produto, produto, categoria, preco |

## Como montar no Power BI
1. Obter dados > Texto/CSV e importe os três arquivos.
2. Crie a tabela `dCalendario` e as medidas do `medidas.dax`.
3. Relacione `fato_vendas[data]` → `dCalendario[Date]`, `id_loja` e `id_produto` às dimensões.
4. Visuais sugeridos: cartões (Faturamento, Ticket Médio), linha mensal por loja, matriz loja × semestre com variação %, barras de mix por categoria.
