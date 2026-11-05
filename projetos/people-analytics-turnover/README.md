# People Analytics: Turnover (dados fictícios)

**Situação:** uma empresa fictícia com 800 funcionários queria entender onde a rotatividade estava concentrada.

**Ação:** tratamento da base de RH no Power Query (tipos de data, nulos como "ativo", faixas salariais e tempo de casa) e dashboard no Power BI com as medidas do `medidas.dax`.

**Resultado:**
- Turnover geral de 20,5% em 2025.
- A área de **Atendimento** teve turnover de 42,3%, cerca do dobro da média.
- Atendimento também concentra a menor faixa salarial (até R$ 3,2 mil), sinal de que remuneração é um fator a investigar.

## Dados
`dados/funcionarios.csv` — id_funcionario, area, data_admissao, salario, data_desligamento (vazio = ativo).

## Como montar no Power BI
1. Importe o CSV e, no Power Query, defina as colunas de data como Data.
2. Crie as colunas calculadas e medidas do `medidas.dax`.
3. Visuais sugeridos: cartões (Headcount, Turnover %), barras de turnover por área com linha da média, matriz área × faixa salarial.
