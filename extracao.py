
from pathlib import Path
from io import BytesIO
from pypdf import PdfReader


class ExtracaoAgent:

    def extrair_texto(self, arquivo_pdf):
        # Aceita tanto um caminho de arquivo quanto os bytes
        # de um PDF carregado pela interface Streamlit.
        if isinstance(arquivo_pdf, bytes):
            leitor = PdfReader(BytesIO(arquivo_pdf))
        else:
            caminho = Path(arquivo_pdf)

            if not caminho.exists():
                raise FileNotFoundError(
                    f"Arquivo não encontrado: {caminho}"
                )

            leitor = PdfReader(str(caminho))

        paginas = []

        for numero, pagina in enumerate(leitor.pages, start=1):
            texto = pagina.extract_text() or ""

            if texto.strip():
                paginas.append(
                    f"\n--- Página {numero} ---\n{texto}"
                )

        texto_completo = "\n".join(paginas)

        if not texto_completo.strip():
            raise ValueError(
                "Não foi possível extrair texto deste PDF. "
                "Ele pode estar digitalizado como imagem e precisar de OCR."
            )

        return texto_completo