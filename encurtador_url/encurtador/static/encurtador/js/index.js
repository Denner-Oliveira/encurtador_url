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
    /*
     * Obtém o valor do cookie CSRF criado pelo Django.
     */
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


    /*
     * Elementos da página
     */
    const form =
        document.getElementById("formEncurtador");

    const inputUrl =
        document.getElementById("url");

    const inputExpiracao =
        document.getElementById("dt_expiracao");

    const resultado =
        document.getElementById("resultado");

    const erro =
        document.getElementById("erro");

    const carregando =
        document.getElementById("carregando");

    const btnEncurtar =
        document.getElementById("btnEncurtar");

    const urlEncurtada =
        document.getElementById("urlEncurtada");

    const btnCopiar =
        document.getElementById("btnCopiar");


    /*
     * Envio do formulário
     */
    form.addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();


            /*
             * Limpa resultados anteriores
             */
            resultado.style.display = "none";

            erro.style.display = "none";


            /*
             * Obtém os dados do formulário
             */
            const url =
                inputUrl.value.trim();

            const dtExpiracao =
                inputExpiracao.value;


            /*
             * Validação básica
             */
            if (!url) {

                mostrarErro(
                    "Informe uma URL."
                );

                return;
            }


            /*
             * Monta o JSON enviado para o Django
             */
            const dados = {
                url: url
            };


            /*
             * A data só é enviada se tiver sido informada.
             */
            if (dtExpiracao) {

                dados.dt_expiracao =
                    dtExpiracao;
            }


            /*
             * Obtém o token CSRF.
             */
            const csrftoken =
                getCookie("csrftoken");


            /*
             * Estado de carregamento
             */
            btnEncurtar.disabled = true;

            carregando.style.display = "block";


            try {

                /*
                 * Requisição para a URL correta
                 *
                 * Django:
                 * path(
                 *     'encurta_url',
                 *     views.encurta_url
                 * )
                 */
                const response =
                    await fetch(
                        "/api/v1/encurta_url",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json",

                                "X-CSRFToken":
                                    csrftoken
                            },

                            body:
                                JSON.stringify(dados)
                        }
                    );


                /*
                 * Tenta interpretar a resposta como JSON.
                 */
                const data =
                    await response.json();


                /*
                 * Verifica erro HTTP.
                 */
                if (!response.ok) {

                    throw new Error(
                        data.detail ||
                        data.error ||
                        "Não foi possível encurtar a URL."
                    );
                }


                /*
                 * Verifica se o Django retornou
                 * a URL encurtada.
                 */
                if (!data.url) {

                    throw new Error(
                        "A API não retornou a URL encurtada."
                    );
                }


                /*
                 * Mostra o resultado.
                 */
                urlEncurtada.value =
                    data.url;

                resultado.style.display =
                    "block";


            } catch (error) {

                console.error(
                    "Erro ao encurtar URL:",
                    error
                );

                mostrarErro(
                    error.message ||
                    "Erro ao comunicar com o servidor."
                );


            } finally {

                btnEncurtar.disabled =
                    false;

                carregando.style.display =
                    "none";
            }
        }
    );


    /*
     * Copiar URL encurtada
     */
    btnCopiar.addEventListener(
        "click",
        async function() {

            try {

                await navigator.clipboard.writeText(
                    urlEncurtada.value
                );


                const textoOriginal =
                    btnCopiar.textContent;


                btnCopiar.textContent =
                    "Copiado!";


                setTimeout(
                    function() {

                        btnCopiar.textContent =
                            textoOriginal;

                    },
                    1500
                );


            } catch (error) {

                /*
                 * Fallback para navegadores
                 * que não suportam Clipboard API.
                 */
                urlEncurtada.select();

                document.execCommand("copy");

                btnCopiar.textContent =
                    "Copiado!";


                setTimeout(
                    function() {

                        btnCopiar.textContent =
                            "Copiar";

                    },
                    1500
                );
            }
        }
    );


    /*
     * Exibe mensagens de erro.
     */
    function mostrarErro(mensagem) {

        erro.textContent =
            mensagem;

        erro.style.display =
            "block";
    }
