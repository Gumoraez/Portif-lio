# Portfólio — Gustavo Valle de Moraes

Portfólio de Dados & BI com projetos usando dados fictícios.

## Projetos
- [Vendas de Varejo](projetos/vendas-varejo) — Power BI + DAX
- [Churn de Assinaturas](projetos/churn-assinaturas) — SQL (PostgreSQL)
- [People Analytics: Turnover](projetos/people-analytics-turnover) — Power BI + Power Query
- Demo de Análise de Pareto (ABC) — Python + FastAPI (`backend/`)

![Dashboard de vendas](frontend/img/vendas.png)

Front em HTML/CSS/JS + API em Python (FastAPI) com demo de Curva ABC e formulário de contato.

## Rodar localmente
```bash
# 1) API
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows  (Linux/Mac: source .venv/bin/activate)
pip install -r requirements.txt
uvicorn main:app --reload     # http://127.0.0.1:8000/docs

# 2) Site (outro terminal)
cd frontend
python -m http.server 5500    # abra http://127.0.0.1:5500
```

## Endpoints
- `GET /api/health` — status
- `POST /api/abc` — CSV com colunas `produto,valor` → classes A (≤80%), B (≤95%), C
- `POST /api/contato` — salva nome, e-mail e mensagem em SQLite

## Deploy
- **Front:** GitHub Pages ou Vercel (pasta `frontend`).
- **API:** Render → Web Service, root `backend`, start `uvicorn main:app --host 0.0.0.0 --port $PORT`.
- Depois, troque `https://SEU-APP.onrender.com` em `frontend/app.js` e restrinja o CORS em `main.py` ao domínio do site.
