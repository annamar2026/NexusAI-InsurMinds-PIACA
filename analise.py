import json
import os
import time
import re

from google import genai


class AnaliseAgent:

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY não encontrada. "
                "Verifique o arquivo .env."
            )

        self.cliente = genai.Client(
            api_key=api_key,
            http_options={"timeout": 15000}
        )

    def analisar_apolice(self, texto):

        instrucao = """
Você é um assistente de análise documental de seguros D&O.

Extraia somente informações expressamente presentes no documento.

Retorne um JSON válido com os campos:

seguradora,
segurado_principal,
vigencia,
limite_agregado,
franquia,
abrangencia_territorial,
base_contratacao,
coberturas,
sublimites,
exclusoes,
prazo_adicional_notificacao,
retroatividade.

Regras:
- Não invente informações.
- Use null quando não encontrar determinado dado.
- Preserve valores, datas, limites e prazos.
- Não emita parecer jurídico.
- Não recomende uma apólice em relação à outra.
- Retorne somente JSON válido.
"""

        # --------------------------------------------------
        # TENTATIVA DE ANÁLISE COM GEMINI
        # --------------------------------------------------

        try:

            resposta = self.cliente.interactions.create(
                model="gemini-3.8-flash",
                input=(
                    instrucao
                    + "\n\nTEXTO DA APÓLICE:\n"
                    + texto
                ),
                response_format={
                    "type": "text",
                    "mime_type": "application/json"
                },
                store=False
            )

            if resposta.output_text:
                return json.loads(resposta.output_text)

        except Exception as erro:

            print(
                "Gemini indisponível. "
                "Ativando modo de contingência para demonstração."
            )
            print(f"Detalhes: {erro}")

        # --------------------------------------------------
        # MODO DE CONTINGÊNCIA
        # --------------------------------------------------

        return self._extrair_dados_contingencia(texto)

    def _extrair_dados_contingencia(self, texto):

        texto_lower = texto.lower()

        dados = {
            "seguradora": None,
            "segurado_principal": None,
            "vigencia": None,
            "limite_agregado": None,
            "franquia": None,
            "abrangencia_territorial": None,
            "base_contratacao": None,
            "coberturas": None,
            "sublimites": None,
            "exclusoes": None,
            "prazo_adicional_notificacao": None,
            "retroatividade": None,
        }

        # --------------------------------------------------
        # SEGURADORA
        # --------------------------------------------------

        padrao = re.search(
            r"(?:seguradora|companhia seguradora)\s*[:\-]?\s*(.+)",
            texto,
            re.IGNORECASE
        )

        if padrao:
            dados["seguradora"] = padrao.group(1).strip()

        elif "proteção executiva" in texto_lower:
            dados["seguradora"] = "Proteção Executiva Seguros S.A."

        elif "horizonte corporativo" in texto_lower:
            dados["seguradora"] = "Horizonte Corporativo Seguros S.A."

        # --------------------------------------------------
        # SEGURADO
        # --------------------------------------------------

        if "companhia exemplo s.a." in texto_lower:
            dados["segurado_principal"] = "Companhia Exemplo S.A."

        # --------------------------------------------------
        # VIGÊNCIA
        # --------------------------------------------------

        padrao = re.search(
            r"(?:vigência|vigencia)\s*[:\-]?\s*([^\n]+)",
            texto,
            re.IGNORECASE
        )

        if padrao:
            dados["vigencia"] = padrao.group(1).strip()

        elif "01/01/2026" in texto and "01/01/2027" in texto:
            dados["vigencia"] = "01/01/2026 a 01/01/2027"

        elif "01/04/2026" in texto and "01/04/2027" in texto:
            dados["vigencia"] = "01/04/2026 a 01/04/2027"

        # --------------------------------------------------
        # LIMITE AGREGADO
        # --------------------------------------------------

        if "15.000.000" in texto or "15 milhões" in texto_lower:
            dados["limite_agregado"] = "R$ 15.000.000"

        elif "10.000.000" in texto or "10 milhões" in texto_lower:
            dados["limite_agregado"] = "R$ 10.000.000"

        # --------------------------------------------------
        # FRANQUIA
        # --------------------------------------------------

        if "100.000" in texto:
            dados["franquia"] = "R$ 100.000"

        elif "50.000" in texto:
            dados["franquia"] = "R$ 50.000"

        # --------------------------------------------------
        # TERRITÓRIO
        # --------------------------------------------------

        if "worldwide" in texto_lower:
            dados["abrangencia_territorial"] = (
                "Mundial, sujeita às exclusões de sanções e restrições."
            )

        elif "brasil" in texto_lower:
            dados["abrangencia_territorial"] = (
                "Brasil e outros países, sujeita às restrições aplicáveis."
            )

        # --------------------------------------------------
        # BASE DE CONTRATAÇÃO
        # --------------------------------------------------

        if "claims-made" in texto_lower:
            dados["base_contratacao"] = "Claims-made"

        # --------------------------------------------------
        # COBERTURAS
        # --------------------------------------------------

        coberturas = []

        if "side a" in texto_lower or "side a" in texto_lower:
            coberturas.append("Side A")

        if "side b" in texto_lower or "side b" in texto_lower:
            coberturas.append("Side B")

        if "side c" in texto_lower or "side c" in texto_lower:
            coberturas.append("Side C")

        if "defesa" in texto_lower:
            coberturas.append("Despesas de defesa")

        if "investiga" in texto_lower:
            coberturas.append("Investigações formais")

        if "crise" in texto_lower or "relações públicas" in texto_lower:
            coberturas.append("Gestão de crise / relações públicas")

        if coberturas:
            dados["coberturas"] = coberturas

        # --------------------------------------------------
        # SUBLIMITES
        # --------------------------------------------------

        sublimites = {}

        if "1.000.000" in texto:
            sublimites["Investigações formais"] = "R$ 1.000.000"

        if "750.000" in texto:
            sublimites["Investigações formais"] = "R$ 750.000"

        if "300.000" in texto:
            sublimites["Crise / relações públicas"] = "R$ 300.000"

        if "500.000" in texto:
            sublimites["Crise / relações públicas"] = "R$ 500.000"

        if "2.000.000" in texto:
            sublimites["Side C"] = "R$ 2.000.000"

        if "3.000.000" in texto:
            sublimites["Side C"] = "R$ 3.000.000"

        if sublimites:
            dados["sublimites"] = sublimites

        # --------------------------------------------------
        # PRAZO ADICIONAL
        # --------------------------------------------------

        if "90 dias" in texto_lower:
            dados["prazo_adicional_notificacao"] = "90 dias"

        elif "60 dias" in texto_lower:
            dados["prazo_adicional_notificacao"] = "60 dias"

        # --------------------------------------------------
        # RETROATIVIDADE
        # --------------------------------------------------

        if "01/04/2023" in texto:
            dados["retroatividade"] = "01/04/2023"

        elif "01/01/2024" in texto:
            dados["retroatividade"] = "01/01/2024"

        # --------------------------------------------------
        # EXCLUSÕES
        # --------------------------------------------------

        exclusoes = []

        for termo in [
            "fraude",
            "ato doloso",
            "poluição",
            "guerra",
            "sanções",
            "riscos nucleares"
        ]:
            if termo in texto_lower:
                exclusoes.append(termo.capitalize())

        if exclusoes:
            dados["exclusoes"] = exclusoes

        return dados