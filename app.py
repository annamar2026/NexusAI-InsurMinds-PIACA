
import json
import time

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from agentes.extracao import ExtracaoAgent
from agentes.analise import AnaliseAgent
from agentes.comparacao import ComparacaoAgent


# --------------------------------------------------
# CONFIGURACAO
# --------------------------------------------------

load_dotenv()

st.set_page_config(
    page_title="InsurMinds | Comparador D&O",
    page_icon="🛡️",
    layout="wide",
)

st.title("🛡️ InsurMinds")
st.subheader(
    "Plataforma Inteligente de Análise e Comparação de Apólices D&O"
)

st.markdown(
    """
    Carregue duas apólices em PDF para extrair informações,
    analisar os documentos com inteligência artificial e comparar
    limites, franquias, coberturas, sublimites e exclusões.
    """
)

st.info(
    "Protótipo acadêmico. Os dados extraídos por IA precisam ser "
    "conferidos nos documentos originais. A ferramenta não substitui "
    "a análise profissional nem constitui recomendação securitária."
)


# --------------------------------------------------
# FUNCOES AUXILIARES
# --------------------------------------------------

def formatar_valor(valor):
    """Converte valores complexos em texto legível."""
    if valor is None:
        return "Não identificado"

    if isinstance(valor, dict):
        return "; ".join(
            f"{chave}: {formatar_valor(item)}"
            for chave, item in valor.items()
        )

    if isinstance(valor, list):
        return "; ".join(
            formatar_valor(item) for item in valor
        )

    return str(valor)


def analisar_pdf(arquivo, nome, agente_extracao, agente_analise):
    """Extrai o texto e solicita a análise do Gemini."""
    if arquivo is None:
        raise ValueError(f"Selecione o arquivo da {nome}.")

    if not arquivo.getvalue():
        raise ValueError(f"O arquivo da {nome} está vazio.")

    texto = agente_extracao.extrair_texto(
        arquivo.getvalue()
    )

    if not texto.strip():
        raise ValueError(
            f"Não foi possível extrair texto da {nome}."
        )

    dados = agente_analise.analisar_apolice(texto)

    if not isinstance(dados, dict):
        raise ValueError(
            f"A análise da {nome} não retornou um objeto JSON válido."
        )

    return dados


# --------------------------------------------------
# UPLOAD DOS DOCUMENTOS
# --------------------------------------------------

coluna_upload_a, coluna_upload_b = st.columns(2)

with coluna_upload_a:
    arquivo_a = st.file_uploader(
        "📄 Apólice A (PDF)",
        type=["pdf"],
        key="upload_apolice_a",
    )

with coluna_upload_b:
    arquivo_b = st.file_uploader(
        "📄 Apólice B (PDF)",
        type=["pdf"],
        key="upload_apolice_b",
    )

executar = st.button(
    "Analisar e comparar apólices",
    type="primary",
    use_container_width=True,
)


# --------------------------------------------------
# ANALISE E COMPARACAO
# --------------------------------------------------

if executar:

    if arquivo_a is None or arquivo_b is None:
        st.warning(
            "Selecione os dois arquivos PDF antes de iniciar."
        )

    else:
        try:
            agente_extracao = ExtracaoAgent()
            agente_analise = AnaliseAgent()
            agente_comparacao = ComparacaoAgent()

            barra = st.progress(0)
            status = st.empty()

            status.info(
                "Etapa 1/4: extraindo e analisando a Apólice A..."
            )

            dados_a = analisar_pdf(
                arquivo_a,
                "Apólice A",
                agente_extracao,
                agente_analise,
            )

            barra.progress(40)

            status.info(
                "Etapa 2/4: extraindo e analisando a Apólice B..."
            )

            dados_b = analisar_pdf(
                arquivo_b,
                "Apólice B",
                agente_extracao,
                agente_analise,
            )

            barra.progress(80)

            status.info(
                "Etapa 3/4: comparando os dados extraídos..."
            )

            comparacao = agente_comparacao.comparar(
                dados_a,
                dados_b,
            )

            barra.progress(100)
            status.success(
                "Etapa 4/4: análise e comparação concluídas!"
            )

            # Guardar os resultados na sessão para que
            # atualizações da interface não apaguem os dados.
            st.session_state["resultado_do"] = {
                "apolice_a": dados_a,
                "apolice_b": dados_b,
                "comparacao": comparacao,
            }

        except Exception as erro:
            st.error(
                "Não foi possível concluir a análise. "
                "Confira os detalhes abaixo."
            )

            mensagem = str(erro)
            mensagem_lower = mensagem.lower()

            if (
                "503" in mensagem
                or "service_unavailable" in mensagem_lower
                or "temporarily unavailable" in mensagem_lower
            ):
                st.warning(
                    "O serviço do Gemini está temporariamente "
                    "indisponível ou sobrecarregado. Aguarde um pouco "
                    "antes de tentar novamente."
                )

            elif (
                "429" in mensagem
                or "resource_exhausted" in mensagem_lower
            ):
                st.warning(
                    "A API informou limite de solicitações ou de uso. "
                    "Verifique a cota e os limites da sua chave Gemini."
                )

            elif (
                "api key" in mensagem_lower
                or "gemini_api_key" in mensagem_lower
            ):
                st.warning(
                    "Confira se a chave GEMINI_API_KEY está definida "
                    "no arquivo .env. Nunca compartilhe sua chave."
                )

            else:
                st.error(f"Detalhes técnicos: {mensagem}")

            st.caption(
                "Se o problema persistir, confira também o terminal "
                "do VS Code para obter a mensagem completa."
            )


# --------------------------------------------------
# EXIBICAO DOS RESULTADOS
# --------------------------------------------------

if "resultado_do" in st.session_state:

    resultado = st.session_state["resultado_do"]

    dados_a = resultado["apolice_a"]
    dados_b = resultado["apolice_b"]
    comparacao = resultado["comparacao"]

    st.divider()
    st.header("1. Resumo das apólices")

    col_a, col_b = st.columns(2)

    campos_resumo = [
        ("seguradora", "Seguradora"),
        ("segurado_principal", "Segurado principal"),
        ("vigencia", "Vigência"),
        ("limite_agregado", "Limite agregado"),
        ("franquia", "Franquia"),
    ]

    with col_a:
        st.subheader("Apólice A")

        for campo, rotulo in campos_resumo:
            st.markdown(f"**{rotulo}:**")
            st.write(formatar_valor(dados_a.get(campo)))

    with col_b:
        st.subheader("Apólice B")

        for campo, rotulo in campos_resumo:
            st.markdown(f"**{rotulo}:**")
            st.write(formatar_valor(dados_b.get(campo)))

    st.divider()
    st.header("2. Comparação detalhada")

    tabela_dados = []

    for item in comparacao:
        tabela_dados.append(
            {
                "Campo analisado": item["campo"],
                "Apólice A": formatar_valor(item["apolice_a"]),
                "Apólice B": formatar_valor(item["apolice_b"]),
                "Há diferença?": (
                    "Sim" if item["diferente"] else "Não"
                ),
            }
        )

    tabela = pd.DataFrame(tabela_dados)

    st.dataframe(
        tabela,
        use_container_width=True,
        hide_index=True,
    )

    diferentes = [
        item for item in comparacao
        if item["diferente"]
    ]

    st.header("3. Principais diferenças")

    if diferentes:
        st.write(
            f"Foram identificados {len(diferentes)} campos "
            "com valores diferentes."
        )

        for item in diferentes:
            with st.expander(item["campo"]):
                st.markdown("**Apólice A**")
                st.write(formatar_valor(item["apolice_a"]))

                st.markdown("**Apólice B**")
                st.write(formatar_valor(item["apolice_b"]))
    else:
        st.info(
            "Não foram identificadas diferenças nos campos comparados."
        )

    st.header("4. Coberturas e exclusões")

    col_cob_a, col_cob_b = st.columns(2)

    with col_cob_a:
        st.subheader("Apólice A")
        st.markdown("**Coberturas**")
        st.write(formatar_valor(dados_a.get("coberturas")))
        st.markdown("**Exclusões**")
        st.write(formatar_valor(dados_a.get("exclusoes")))
        st.markdown("**Sublimites**")
        st.write(formatar_valor(dados_a.get("sublimites")))

    with col_cob_b:
        st.subheader("Apólice B")
        st.markdown("**Coberturas**")
        st.write(formatar_valor(dados_b.get("coberturas")))
        st.markdown("**Exclusões**")
        st.write(formatar_valor(dados_b.get("exclusoes")))
        st.markdown("**Sublimites**")
        st.write(formatar_valor(dados_b.get("sublimites")))

    st.header("5. Dados completos da análise")

    with st.expander("JSON da Apólice A"):
        st.json(dados_a)

    with st.expander("JSON da Apólice B"):
        st.json(dados_b)

    arquivo_resultado = json.dumps(
        resultado,
        ensure_ascii=False,
        indent=2,
    )

    st.download_button(
        "Baixar comparação em JSON",
        data=arquivo_resultado,
        file_name="comparacao_apolices_do.json",
        mime="application/json",
        use_container_width=True,
    )

    st.caption(
        "A comparação apresenta diferenças nos dados extraídos. "
        "Ela não determina automaticamente a suficiência das coberturas "
        "nem qual apólice é mais vantajosa."
    )

st.divider()

st.caption(
    "InsurMinds | Projeto acadêmico de análise documental de seguros D&O"
)
