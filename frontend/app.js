// Endereço da API: local em desenvolvimento; troque pela URL do Render depois do deploy.
const API_URL = location.hostname === "localhost" || location.hostname === "127.0.0.1"
  ? "http://127.0.0.1:8000"
  : "https://SEU-APP.onrender.com";

const fmt = (n) => n.toLocaleString("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 });

function setStatus(el, msg, tipo = "") {
  el.textContent = msg;
  el.className = "status " + tipo;
}

// Curva ABC
document.getElementById("form-abc").addEventListener("submit", async (e) => {
  e.preventDefault();
  const status = document.getElementById("abc-status");
  const arquivo = document.getElementById("arquivo").files[0];
  if (!arquivo) return;

  setStatus(status, "Calculando... (a API pode levar alguns segundos para acordar)");
  const fd = new FormData();
  fd.append("arquivo", arquivo);

  try {
    const r = await fetch(`${API_URL}/api/abc`, { method: "POST", body: fd });
    const data = await r.json();
    if (!r.ok) throw new Error(data.detail || "Erro ao processar");

    document.getElementById("kpis").innerHTML = data.resumo.map((c) => `
      <div class="kpi ${c.classe}">
        <div class="cl">Classe ${c.classe}</div>
        <small>${c.itens} itens (${fmt(c.pct_itens)}% dos itens)</small>
        <small>R$ ${fmt(c.valor)} (${fmt(c.pct_valor)}% do valor)</small>
      </div>`).join("");

    document.getElementById("tabela").innerHTML = data.itens.map((i) => `
      <tr>
        <td>${String(i.produto).replace(/[<>&]/g, "")}</td>
        <td>R$ ${fmt(i.valor)}</td>
        <td>${fmt(i.pct)}%</td>
        <td>${fmt(i.pct_acum)}%</td>
        <td><span class="badge ${i.classe}">${i.classe}</span></td>
      </tr>`).join("");

    document.getElementById("abc-resultado").hidden = false;
    setStatus(status, `${data.qtd_itens} itens analisados · total R$ ${fmt(data.total)}`, "ok");
  } catch (err) {
    setStatus(status, err.message || "Não foi possível conectar à API", "erro");
  }
});

// Contato
document.getElementById("form-contato").addEventListener("submit", async (e) => {
  e.preventDefault();
  const form = e.target;
  const status = document.getElementById("contato-status");
  const dados = Object.fromEntries(new FormData(form));

  setStatus(status, "Enviando...");
  try {
    const r = await fetch(`${API_URL}/api/contato`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(dados),
    });
    const data = await r.json();
    if (!r.ok) throw new Error("Confira os campos e tente de novo");
    setStatus(status, data.mensagem, "ok");
    form.reset();
  } catch (err) {
    setStatus(status, err.message || "Não foi possível enviar", "erro");
  }
});
