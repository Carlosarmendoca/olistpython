# 📊 Olist Analytics — Python & Streamlit

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge\&logo=python\&logoColor=white)]()
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge\&logo=streamlit\&logoColor=white)]()
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge\&logo=pandas\&logoColor=white)]()
[![Plotly](https://img.shields.io/badge/Plotly-239120?style=for-the-badge\&logo=plotly\&logoColor=white)]()

> **🔗 Acesse o Dashboard Online:** [Insira o link do Streamlit Cloud aqui após o deploy]

Projeto de análise de dados desenvolvido a partir do dataset público da **Olist**, empresa brasileira de marketplace, com foco em análise de vendas, clientes, categorias e desempenho geográfico.

O projeto foi desenvolvido como parte do meu portfólio na área de **Data Analytics**, utilizando Python, Pandas, SQL e visualização de dados para transformar dados brutos em informações úteis para tomada de decisão.

---

## 🎯 Objetivo

Transformar dados brutos de pedidos, clientes, produtos, itens e pagamentos em informações que permitam analisar:

* 📈 Evolução do faturamento e volume de pedidos;
* 💰 Ticket médio e prazo médio de entrega;
* 📦 Desempenho e ranking das categorias;
* 📍 Distribuição geográfica e receita por estado;
* 👥 Evolução e distribuição da base de clientes;
* 🔎 Comportamento dos pedidos por status.

---

## 🚀 Destaques Técnicos do Dashboard

* **Design Executivo:** Interface desenvolvida com redução de ruídos visuais, foco em Data Storytelling e utilização de uma identidade visual consistente.

* **Cross-Filtering Geográfico:** Interatividade utilizando `st.session_state`. A seleção de um estado no mapa do Brasil atualiza dinamicamente os indicadores e análises da página.

* **Localização PT-BR Customizada:** Formatação de valores monetários e quantitativos seguindo o padrão brasileiro, incluindo valores como `R$ 15,42 milhões` e `110.197`.

* **Alta Performance:** Utilização de `@st.cache_data` e organização das transformações em funções reutilizáveis para evitar operações desnecessárias.

* **Identificação de Clientes Únicos:** Utilização de `customer_unique_id` para evitar a contagem duplicada de clientes que realizaram múltiplos pedidos.

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia     | Utilização                                                                         |
| :------------- | :----------------------------------------------------------------------------------|
| **Python**     | Desenvolvimento da aplicação e tratamento dos dados                                |
| **Pandas**     | Manipulação, transformação, agrupamento e análise dos dados                        |
| **Plotly**     | Criação de gráficos interativos com foco em visualização limpa                     |
| **Streamlit**  | Construção da interface do dashboard e filtros interativos                         |
| **SQL**        | Consultas, agregações e lógica de criação de métricas                              |
| **Git/GitHub** | Versionamento e documentação do projeto                                            |
| **Gemini**     | Ferramenta de IA auxiliar utilizada para revisão, correção e construção de código  |

---

# 📈 Dashboards

O projeto está dividido em três páginas principais.

## 1. Painel Executivo

Visão geral dos principais indicadores de desempenho do negócio.

### Métricas

* Faturamento total;
* Total de pedidos;
* Ticket médio;
* Prazo médio de entrega.

### Análises

* Mapa interativo de receita por estado;
* Evolução mensal do faturamento;
* Análise Month-over-Month (MoM);
* Principais categorias.

---

## 2. Desempenho das Categorias

Análise do desempenho comercial das categorias de produtos, permitindo identificar quais categorias apresentam maior participação e volume.

### Métricas

* Receita;
* Quantidade de pedidos;
* Quantidade de itens;
* Preço médio dos produtos;
* Valor médio por item com frete.

### Análises

* Ranking das Top 10 categorias por receita;
* Comparação de desempenho entre categorias;
* Evolução temporal das principais métricas.

---

## 3. Análise de Clientes

Análise da distribuição geográfica e evolução da base de clientes.

A identificação dos clientes utiliza `customer_unique_id`, permitindo considerar corretamente clientes que realizaram múltiplos pedidos.

### Métricas

* Total de clientes únicos;
* Clientes com pedidos entregues;
* Clientes com pedidos cancelados;
* Clientes com pedidos faturados.

### Análises

* Top 10 estados por clientes;
* Top 10 cidades por clientes;
* Evolução acumulada da base de clientes;
* Distribuição de clientes por status dos pedidos.

---

# 💡 Resultados e Insights

A estruturação dos dados e dos dashboards permite obter diferentes visões estratégicas sobre a operação, como:

* Identificação de regiões com maior concentração de clientes e maior volume de vendas, contribuindo para análises comerciais e logísticas;
* Identificação de categorias com maior participação no faturamento e comparação entre volume de vendas e valor gerado;
* Acompanhamento da evolução da base de clientes ao longo do período analisado;
* Identificação da distribuição de clientes associados aos diferentes status dos pedidos;
* Comparação entre indicadores comerciais e operacionais para apoiar análises de desempenho.

---

# 🔎 Tratamento e Preparação dos Dados

Durante o desenvolvimento foram realizadas etapas de limpeza, transformação e preparação dos dados utilizando Pandas.

Entre os principais tratamentos:

* Conversão de `strings` para `datetime`;
* Tratamento de valores ausentes;
* Padronização dos nomes de cidades utilizando *Title Case*;
* Criação de bases unificadas utilizando `merge()`;
* Agrupamentos e agregações utilizando `groupby()`;
* Contagem de clientes únicos utilizando `nunique()`;
* Criação de métricas derivadas;
* Organização das transformações em funções reutilizáveis;
* Reutilização de bases para reduzir operações repetitivas.

---

# 📊 Principais Métricas

### Faturamento

Valor total associado aos pedidos analisados.

### Ticket Médio

```text
Ticket Médio = Faturamento Total / Total de Pedidos
```

### Clientes Únicos

Quantidade distinta de clientes identificados por:

```text
customer_unique_id
```

### Receita por Categoria

Permite comparar a contribuição das diferentes categorias para o faturamento total.

### Receita Mensal

Permite acompanhar a evolução do faturamento ao longo do período analisado.

### Evolução da Base de Clientes

A evolução acumulada considera cada cliente apenas uma vez, utilizando seu primeiro pedido identificado para determinar o período de entrada na base.

---

# 🧠 Principais Aprendizados

O desenvolvimento deste projeto permitiu aplicar conceitos importantes de **Data Analytics**, incluindo:

* Exploração e tratamento de dados;
* Manipulação de DataFrames com Pandas;
* SQL para análise de dados;
* Criação e validação de métricas de negócio;
* `groupby()` e agregações;
* `merge()` e relacionamento entre tabelas;
* `nunique()` para identificação de clientes únicos;
* Análise temporal;
* Criação de indicadores;
* Visualização de dados;
* Desenvolvimento de dashboards interativos;
* Organização de código em funções reutilizáveis;
* Versionamento utilizando Git e GitHub.

---

# 🚀 Próximos Passos

Como evolução do projeto, algumas possibilidades são:

* Integração com banco de dados em nuvem, como BigQuery ou PostgreSQL;
* Automatização do carregamento dos dados;
* Criação de pipelines utilizando Airflow;
* Evolução das análises de retenção e recorrência;
* Análise de Cohort de clientes;
* Análise RFM;
* Criação de uma camada analítica utilizando SQL e dbt;
* Inclusão de novos indicadores de negócio.

---

# 📁 Estrutura do Projeto

```text
olistpython/
│
├── dados/
│   ├── pedidos_limpo.csv
│   ├── clientes_limpo.csv
│   ├── itens_limpo.csv
│   ├── pagamentos_limpo.csv
│   └── produtos_limpo.csv
│
├── Notebooks/
│   └── Análises e exploração dos dados
│
├── pages/
│   ├── 1_Painel_Executivo.py
│   ├── 2_Desempenho_Categorias.py
│   └── 3_Analise_Clientes.py
│
├── views/
│   └── Funções de preparação das bases
│       utilizadas pelos dashboards
│
├── Inicio.py
├── requirements.txt
└── README.md
```

---

# 📌 Sobre o Projeto

Este projeto faz parte do meu portfólio de **Data Analytics** e tem como objetivo demonstrar, na prática, a aplicação de Python, Pandas, SQL e ferramentas de visualização em um problema de negócio.

Mais do que construir gráficos, o projeto busca demonstrar o processo de:

**Dados → Tratamento → Métricas → Análise → Visualização → Insights**

---

## 👤 Autor

**Carlos Alberto Rodrigues de Mendonça**

Projeto desenvolvido para composição de portfólio na área de **Data Analytics**.

🔗 [GitHub](https://github.com/Carlosarmendoca)
