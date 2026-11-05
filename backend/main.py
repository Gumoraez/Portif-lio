"""API do portfólio de Gustavo Valle de Moraes.

Endpoints:
  GET  /api/health        -> status da API
  POST /api/abc           -> recebe CSV (produto, valor) e devolve a curva ABC
  POST /api/contato       -> salva mensagem de contato no SQLite
"""
import csv
import io
from collections import defaultdict
import sqlite3
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field

DB_PATH = Path(__file__).parent / "contatos.db"

app = FastAPI(title="Portfólio Gustavo - API")

# Em produção, troque "*" pelo domínio do seu site (ex.: https://gustavovalle.github.io)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


def init_db() -> None:
    with sqlite3.connect(DB_PATH) as con:
        con.execute(
            """CREATE TABLE IF NOT EXISTS contatos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL,
                mensagem TEXT NOT NULL,
                criado_em TEXT NOT NULL
            )"""
        )


init_db()


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/abc")
async def curva_abc(arquivo: UploadFile = File(...)):
    """Classifica itens em A (até 80% do valor), B (até 95%) e C (restante)."""
    if not arquivo.filename.lower().endswith(".csv"):
        raise HTTPException(400, "Envie um arquivo .csv")

    conteudo = await arquivo.read()
    if len(conteudo) > 2_000_000:
        raise HTTPException(400, "Arquivo muito grande (máx. 2 MB)")

    texto = conteudo.decode("utf-8-sig", errors="replace")
    try:
        dialeto = csv.Sniffer().sniff(texto.splitlines()[0], delimiters=",;\t")
    except Exception:
        dialeto = csv.excel
    leitor = csv.DictReader(io.StringIO(texto), dialect=dialeto)
    if not leitor.fieldnames:
        raise HTTPException(400, "Não consegui ler o CSV")
    colunas = {c.strip().lower(): c for c in leitor.fieldnames}
    if not {"produto", "valor"}.issubset(colunas):
        raise HTTPException(400, "O CSV precisa das colunas 'produto' e 'valor'")

    totais: dict[str, float] = defaultdict(float)
    for linha in leitor:
        produto = (linha.get(colunas["produto"]) or "").strip()
        bruto = (linha.get(colunas["valor"]) or "").strip().replace(",", ".")
        try:
            valor = float(bruto)
        except ValueError:
            continue
        if produto and valor > 0:
            totais[produto] += valor
    if not totais:
        raise HTTPException(400, "Nenhum valor numérico válido encontrado")

    total = sum(totais.values())
    itens, acum = [], 0.0
    for produto, valor in sorted(totais.items(), key=lambda x: x[1], reverse=True):
        pct = valor / total * 100
        acum_ant = acum
        acum += pct
        # o item que cruza o corte entra na classe anterior
        classe = "A" if acum_ant < 80 else ("B" if acum_ant < 95 else "C")
        itens.append({"produto": produto, "valor": round(valor, 2), "pct": round(pct, 2),
                      "pct_acum": round(acum, 2), "classe": classe})

    resumo = []
    for c in "ABC":
        sel = [i for i in itens if i["classe"] == c]
        v = sum(i["valor"] for i in sel)
        resumo.append({"classe": c, "itens": len(sel), "valor": round(v, 2),
                       "pct_itens": round(len(sel) / len(itens) * 100, 2),
                       "pct_valor": round(v / total * 100, 2)})

    return {"total": round(total, 2), "qtd_itens": len(itens), "resumo": resumo, "itens": itens}


class Contato(BaseModel):
    nome: str = Field(min_length=2, max_length=100)
    email: EmailStr
    mensagem: str = Field(min_length=5, max_length=2000)


@app.post("/api/contato")
def contato(dados: Contato):
    with sqlite3.connect(DB_PATH) as con:
        con.execute(
            "INSERT INTO contatos (nome, email, mensagem, criado_em) VALUES (?, ?, ?, ?)",
            (dados.nome, dados.email, dados.mensagem, datetime.now().isoformat()),
        )
    return {"ok": True, "mensagem": "Mensagem recebida, obrigado!"}
