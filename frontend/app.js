// Formulário de contato: envia para o e-mail via FormSubmit, sem sair da página.
const form = document.getElementById("form-contato");
const status = document.getElementById("contato-status");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  if (form.querySelector('[name="_honey"]').value) return; // proteção contra robôs

  const botao = form.querySelector("button");
  botao.disabled = true;
  status.textContent = "Enviando...";
  status.className = "status";

  try {
    const url = form.action.replace("formsubmit.co/", "formsubmit.co/ajax/");
    const r = await fetch(url, {
      method: "POST",
      headers: { Accept: "application/json" },
      body: new FormData(form),
    });
    const data = await r.json();
    if (!r.ok || String(data.success) !== "true") throw new Error(data.message);
    status.textContent = "Mensagem enviada! Vou responder em breve.";
    status.className = "status ok";
    form.reset();
  } catch (err) {
    status.textContent = "Não foi possível enviar agora. Tente de novo em instantes.";
    status.className = "status erro";
  } finally {
    botao.disabled = false;
  }
});
