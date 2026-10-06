# 🛡️ InsurMinds — Plataforma Inteligente para Análise e Comparação de Apólices D&O

## 📌 Sobre o projeto

O **InsurMinds** é uma plataforma acadêmica desenvolvida para auxiliar na análise e comparação de apólices de seguro **D&O (Directors and Officers)**.

A aplicação permite o carregamento de duas apólices em formato PDF, realiza a extração do conteúdo documental, estrutura informações relevantes e apresenta uma comparação entre os documentos.

O projeto utiliza inteligência artificial generativa como parte do processo de análise documental, além de mecanismos de contingência para permitir a demonstração da aplicação quando o serviço externo de IA estiver temporariamente indisponível.

> **Aviso:** o sistema é um protótipo acadêmico. Os resultados devem ser conferidos nos documentos originais e não constituem parecer jurídico, recomendação securitária ou decisão automatizada de contratação.

---

## 🎯 Objetivos

* Automatizar a leitura inicial de documentos de seguro D&O;
* Estruturar informações relevantes das apólices;
* Comparar duas apólices de forma organizada;
* Identificar diferenças entre limites, franquias, coberturas, sublimites e exclusões;
* Utilizar inteligência artificial generativa para auxiliar na análise documental;
* Demonstrar uma aplicação prática de IA aplicada ao mercado de seguros.

---

## ⚙️ Funcionalidades

* Upload de duas apólices em PDF;
* Extração automática de texto;
* Análise estruturada dos documentos;
* Identificação de informações contratuais relevantes;
* Comparação entre Apólice A e Apólice B;
* Exibição das principais diferenças;
* Visualização de coberturas, exclusões e sublimites;
* Exportação da comparação em formato JSON;
* Mensagens de progresso durante o processamento;
* Mecanismo de contingência para continuidade da demonstração em caso de indisponibilidade temporária do serviço de IA.

---

## 🧠 Tecnologias utilizadas

* **Python**
* **Streamlit**
* **Google Gemini API**
* **Google Gen AI SDK**
* **pypdf**
* **Pandas**
* **python-dotenv**

---

## 📁 Estrutura do projeto

```text
plataforma_do/
│
├── app.py
├── requirements.txt
├── README.md
├── .env
├── .env.example
├── .gitignore
│
├── agentes/
│   ├── __init__.py
│   ├── extracao.py
│   ├── analise.py
│   └── comparacao.py
│
└── documentos/
    ├── Apolice_DO_Ficticia_A.pdf
    └── Apolice_DO_Ficticia_B.pdf
```

---

## 🚀 Instalação

### 1. Criar e ativar o ambiente virtual

No terminal:

```bash
python -m venv .venv
```

No Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

### 2. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar a chave da API

Crie um arquivo chamado:

```text
.env
```

e configure:

```text
GEMINI_API_KEY=sua_chave_aqui
```

**Nunca publique a chave da API no GitHub.**

---

## ▶️ Execução

Com o ambiente virtual ativado, execute:

```bash
streamlit run app.py
```

A aplicação será disponibilizada localmente pelo Streamlit.

Depois:

1. Carregue a Apólice A;
2. Carregue a Apólice B;
3. Clique em **Analisar e comparar apólices**;
4. Consulte o resumo e a comparação;
5. Se desejar, exporte os resultados em JSON.

---

## 🔐 Segurança e privacidade

O projeto adota algumas medidas básicas de segurança:

* A chave da API é armazenada em variável de ambiente;
* O arquivo `.env` é excluído do controle de versão pelo `.gitignore`;
* Os documentos utilizados para demonstração são fictícios;
* O sistema não deve ser utilizado para inserir informações confidenciais ou dados pessoais reais sem avaliação adequada dos mecanismos de segurança;
* Os resultados gerados por IA devem ser revisados antes de qualquer utilização profissional.

---

## 🤖 Uso de inteligência artificial

A aplicação utiliza um modelo de inteligência artificial generativa para auxiliar na identificação e estruturação das informações presentes nas apólices.

Foram implementadas instruções para:

* extrair apenas informações presentes no documento;
* evitar a invenção de informações;
* utilizar `null` quando determinado dado não for identificado;
* não emitir parecer jurídico;
* não recomendar automaticamente uma apólice;
* tratar o conteúdo do documento como dados e não como instruções.

---

## ⚠️ Limitações

A versão atual do protótipo trabalha principalmente com PDFs que possuem texto selecionável.

Documentos digitalizados exclusivamente como imagens podem exigir uma etapa adicional de **OCR (Reconhecimento Óptico de Caracteres)**.

Além disso, a análise automatizada não substitui a conferência humana do documento original.

---

## 📄 Documentos de demonstração

Os arquivos disponibilizados na pasta `documentos/` são apólices **fictícias**, criadas exclusivamente para fins acadêmicos e de demonstração da plataforma.

---

## 👥 Equipe

Projeto desenvolvido como parte do projeto final do programa **InsurMinds** pela equipe NexusAI.

---

## 📜 Licença

Este projeto é disponibilizado sob a licença **MIT**.

Consulte o arquivo `LICENSE` para obter o texto completo da licença.
