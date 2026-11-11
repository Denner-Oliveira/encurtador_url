let inputExpirar = document.getElementById("dt_expiracao");

const hoje = new Date();
const hoje_max = new Date();

const ano = hoje.getFullYear();
const mes = String(hoje.getMonth() + 1).padStart(2, "0");
const dia = String(hoje.getDate()).padStart(2, "0");

hoje_max.setDate(hoje_max.getDate() + 730)

const ano_max = hoje_max.getFullYear();
const mes_max = String(hoje_max.getMonth() + 1).padStart(2, "0");
const dia_max = String(hoje_max.getDate()).padStart(2, "0");

inputExpirar.min = `${ano}-${mes}-${dia}`;
inputExpirar.max = `${ano_max}-${mes_max}-${dia_max}`


function getCookie(name) {

    let cookieValue = null;

    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");

        for (let cookie of cookies) {
            cookie = cookie.trim();

            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
                break;
            }
        }
    }

    return cookieValue;
}


const form = document.getElementById("formEncurtador");

const inputUrl = document.getElementById("url");

const inputExpiracao = document.getElementById("dt_expiracao");

const resultado = document.getElementById("resultado");

const erro = document.getElementById("erro");

const carregando = document.getElementById("carregando");

const btnEncurtar = document.getElementById("btnEncurtar");

const urlEncurtada = document.getElementById("urlEncurtada");

const btnCopiar = document.getElementById("btnCopiar");


form.addEventListener("submit",
    async function(event) {
        event.preventDefault();

        resultado.style.display = "none";
        erro.style.display = "none";

        const url =
            inputUrl.value.trim();

        const dtExpiracao =
            inputExpiracao.value;

        if (!url) {
            mostrarErro("Informe uma URL.");
            return;
        }

        const dados = {url: url};

        if (dtExpiracao) {
            dados.dt_expiracao =dtExpiracao;
        }

        const csrftoken = getCookie("csrftoken");

        btnEncurtar.disabled = true;
        carregando.style.display = "block";

        try {

            const response =
                await fetch("/api/v1/encurta_url",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":"application/json",
                            "X-CSRFToken":csrftoken
                        },

                        body: JSON.stringify(dados)
                    }
                );

            const data =
                await response.json();

            if (!response.ok) {
                throw new Error(data.detail || data.error || "Não foi possível encurtar a URL.");
            }

            if (!data.url) {

                throw new Error("A API não retornou a URL encurtada.");
            }

            urlEncurtada.value =data.url;

            resultado.style.display ="block";


        } catch (error) {

            console.error( "Erro ao encurtar URL:",error);

            mostrarErro(error.message ||"Erro ao comunicar com o servidor.");

        } finally {

            btnEncurtar.disabled =false;

            carregando.style.display ="none";
        }
    }
);

btnCopiar.addEventListener("click",
    async function() {

        try {

            await navigator.clipboard.writeText(
                urlEncurtada.value
            );

            const textoOriginal = btnCopiar.textContent;

            btnCopiar.textContent = "Copiado!";

            setTimeout(function() {
                btnCopiar.textContent = textoOriginal;
            },1500);


        } catch (error) {
            urlEncurtada.select();

            document.execCommand("copy");

            btnCopiar.textContent ="Copiado!";

            setTimeout(function() {
                btnCopiar.textContent ="Copiar";
            },1500);
        }
    }
);

function mostrarErro(mensagem) {

    erro.textContent = mensagem;

    erro.style.display = "block";
}

(() => {
    const form = document.getElementById("formDeletaUrl");
    const inputCodigo = document.getElementById("codigoUrl");
    const botao = document.getElementById("btnDeletarUrl");
    const status = document.getElementById("statusDeletaUrl");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const codigo = inputCodigo.value.trim();

        if (!codigo) {
            status.textContent = "Informe o código da URL.";
            status.style.color = "#c0392b";
            return;
        }

        if (!window.confirm(`Deseja excluir a URL com o código "${codigo}"?`)) {
            return;
        }

        botao.disabled = true;
        status.textContent = "";

        try {
            const response = await fetch(`/api/v1/deleta_url/${encodeURIComponent(codigo)}`,{ method: "DELETE" });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || data.error || "Não foi possível excluir a URL.");
            }

            status.textContent = data.detail || "URL excluída com sucesso.";
            status.style.color = "#17633d";
            inputCodigo.value = "";
        } catch (error) {
            status.textContent = error instanceof Error ? error.message : "Erro ao comunicar com o servidor.";
            status.style.color = "#c0392b";
        } finally {
            botao.disabled = false;
        }
    });
})();