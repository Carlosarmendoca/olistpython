# 📊 Olist Analytics — Python & Streamlit

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-239120?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)

> **🔗 Dashboard Online:** [Acesse o dashboard](https://olistpython-tt22kbyks8xx4a8dmvyfcj.streamlit.app/)

Projeto de **Data Analytics** desenvolvido em Python e Streamlit a partir do conjunto de dados público da **Olist**, uma empresa brasileira de tecnologia voltada ao ecossistema de e-commerce.

O projeto transforma dados de pedidos, clientes, produtos, itens e pagamentos em indicadores e análises para apoiar a compreensão do desempenho comercial, da distribuição geográfica e da evolução da base de clientes.

A base reúne pedidos realizados entre **2016 e 2018**, permitindo analisar diferentes etapas da jornada de compra, desde o pedido até a entrega logística ao cliente.

---

## 🖼️ Preview

<details>
<summary><b>📊 Ver prints do Painel Executivo</b></summary>
<br>

<p align="center">
  <img src="assets/painel_executivo_1.png" alt="Painel Executivo - Indicadores" width="800"/>
</p>

<p align="center">
  <img src="assets/painel_executivo_2.png" alt="Painel Executivo - Mapa por Estado" width="800"/>
</p>

<p align="center">
  <img src="assets/painel_executivo_3.png" alt="Painel Executivo - Top Categorias e Evolução" width="800"/>
</p>

<p align="center">
  <img src="assets/painel_executivo_4.png" alt="Painel Executivo - Análise MoM" width="800"/>
</p>

</details>

<details>
<summary><b>🏆 Ver prints de Desempenho das Categorias</b></summary>
<br>

<p align="center">
  <img src="assets/desempenho_categorias_1.png" alt="Desempenho de Categorias - Indicadores" width="800"/>
</p>

<p align="center">
  <img src="assets/desempenho_categorias_2.png" alt="Desempenho de Categorias - Top 10 por Faturamento" width="800"/>
</p>

<p align="center">
  <img src="assets/desempenho_categorias_3.png" alt="Desempenho de Categorias - Evolução do Ticket Médio" width="800"/>
</p>

<p align="center">
  <img src="assets/desempenho_categorias_4.png" alt="Desempenho de Categorias - Resumo por Categoria" width="800"/>
</p>

</details>

<details>
<summary><b>👥 Ver prints de Clientes e Pedidos</b></summary>
<br>

<p align="center">
  <img src="assets/analise_clientes_1.png" alt="Análise de Clientes - Indicadores" width="800"/>
</p>

<p align="center">
  <img src="assets/analise_clientes_2.png" alt="Análise de Clientes - Estados e Cidades" width="800"/>
</p>

<p align="center">
  <img src="assets/analise_clientes_3.png" alt="Análise de Clientes - Evolução Acumulada" width="800"/>
</p>

<p align="center">
  <img src="assets/analise_clientes_4.png" alt="Análise de Clientes - Status dos Pedidos" width="800"/>
</p>

</details>

<!-- Se tiver um GIF de demonstração, descomente o bloco abaixo -->
<!--
<p align="center"><img src="assets/demo.gif" alt="Demonstração do dashboard" width="800"/></p>
-->

---

---

## 🎯 Objetivo

Transformar dados brutos em informações que permitam analisar:

- 📈 Evolução do faturamento e volume de pedidos;
- 💰 Ticket médio e prazo médio de entrega;
- 📦 Desempenho das categorias de produtos;
- 📍 Distribuição geográfica de vendas e clientes;
- 👥 Evolução da base de clientes;
- 🔎 Distribuição dos pedidos por status.

---

## 📊 Dashboard

O projeto está dividido em três visões principais.

### 1. 📊 Painel Executivo
Visão geral do negócio: **faturamento total, total de pedidos, ticket médio e prazo médio de entrega**, com mapa interativo de receita por estado, evolução mensal do faturamento, análise Month-over-Month (MoM) e ranking das principais categorias.

### 2. 🏆 Desempenho das Categorias
Desempenho comercial por categoria: **faturamento, ticket médio, itens vendidos e preço médio por item**, com Top 10 categorias por faturamento, evolução mensal do ticket médio e resumo consolidado por categoria.

### 3. 👥 Clientes e Pedidos
Distribuição geográfica e evolução da base de clientes, usando `customer_unique_id` para contabilizar corretamente clientes com múltiplos pedidos. Traz **total de clientes, entregues, cancelados e faturados**, Top 10 estados e cidades, evolução acumulada da base e distribuição por status de pedido.

> Um mesmo cliente pode aparecer em mais de um status caso tenha realizado pedidos com situações diferentes.

---

## 🚀 Como Executar Localmente

```bash
# 1. Clone o repositório
git clone https://github.com/Carlosarmendoca/olistpython.git
cd olistpython

# 2. Crie e ative um ambiente virtual (opcional, mas recomendado)
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute a aplicação
streamlit run Inicio.py
```

O dashboard abrirá automaticamente no navegador em `http://localhost:8501`.

---

## 🚀 Destaques Técnicos

- **🎨 Design Executivo** — interface com foco em clareza visual, redução de ruídos e Data Storytelling, com identidade consistente entre as páginas
- **🔎 Filtros Interativos** — filtros por ano e estado em todas as páginas, permitindo explorar diferentes recortes da base
- **🗺️ Cross-Filtering Geográfico** — o mapa da visão executiva usa `st.session_state` para atualizar dinamicamente as análises conforme o estado clicado
- **🇧🇷 Formatação PT-BR** — valores monetários e quantitativos seguem o padrão brasileiro de moeda e separadores
- **⚡ Performance** — uso de `@st.cache_data` para evitar recarregamento desnecessário dos dados
- **👥 Clientes Únicos** — uso de `customer_unique_id` para evitar contagem duplicada de clientes com múltiplos pedidos
- **🧩 Organização do Código** — transformações e agregações centralizadas em `views/`, separando dados da apresentação

---

| Tecnologia     | Utilização                                                   |
| -------------- | ------------------------------------------------------------ |
| **Python**     | Desenvolvimento da aplicação e tratamento dos dados           |
| **Pandas**     | Manipulação, transformação, agrupamento e análise dos dados   |
| **NumPy**      | Operações e suporte ao processamento dos dados                |
| **Plotly**     | Criação de gráficos e mapas interativos no dashboard          |
| **Matplotlib** | Aplicação de gradientes de cores nas tabelas do dashboard      |
| **Streamlit**  | Desenvolvimento da interface e filtros interativos             |
| **Git/GitHub** | Versionamento e documentação do projeto                        |
| **IA**         | Apoio na revisão de código, refatoração e boas práticas de organização |

---

## 🔎 Tratamento e Preparação dos Dados

Etapas de limpeza e transformação realizadas com Pandas: conversão de campos para `datetime`, tratamento de valores ausentes, padronização de nomes de cidades, relacionamento entre bases com `merge()`, agregações com `groupby()`, contagem de clientes únicos com `nunique()` e criação de métricas derivadas — organizadas em funções reutilizáveis dentro de `views/`.
A pasta `Notebooks/` documenta essa etapa de exploração: é onde cada tratamento e métrica foi testado e validado antes de virar código definitivo em `views/`, servindo como registro do processo de análise por trás do dashboard.

---

## 📌 Principais Métricas

### Faturamento
Valor total associado aos pedidos considerados na análise.

### Ticket Médio
```
Ticket Médio = Faturamento Total / Total de Pedidos
```
### Clientes Únicos
Quantidade distinta de clientes identificados por `customer_unique_id`.

### Receita por Categoria
Permite comparar a contribuição das diferentes categorias para o faturamento total.

### Receita Mensal
Permite acompanhar a evolução do faturamento ao longo do período analisado.

### Evolução da Base de Clientes
A evolução acumulada considera cada cliente apenas uma vez e utiliza seu primeiro pedido identificado para determinar o período de entrada na base.

---

## 💡 Insights Possíveis

A estrutura dos dashboards permite explorar diferentes aspectos do negócio. Alguns achados encontrados ao navegar pelos dados:

- **São Paulo concentra o maior volume, mas não o maior valor por pedido.** O estado fatura R$ 5,77 mi contra R$ 2,06 mi do Rio de Janeiro (2º colocado) — quase 3x mais —, porém com ticket médio 14% *menor* (R$ 142,47 vs R$ 166,45). Isso sugere que SP vende mais em quantidade, enquanto o RJ vende, em média, itens de maior valor por pedido.

- **Regiões remotas compram menos, mas gastam mais por pedido — e esperam mais para receber.** O Acre tem apenas 80 pedidos registrados no período (o menor volume entre os estados), mas o maior ticket médio dos três analisados (R$ 244,83) e o prazo de entrega mais longo (21 dias, mais que o dobro de São Paulo). Esse padrão é comum em estados distantes dos centros de distribuição: poucas compras, de maior valor, possivelmente pra compensar o custo e o tempo do frete.

- **A categoria líder em faturamento não é a que mais vende em volume.** "Beleza Saude" fatura mais que "Cama Mesa Banho" (R$ 1,41 mi vs R$ 1,23 mi) apesar de ter menos pedidos (8.647 vs 9.272) — o ticket médio 24% maior (R$ 163,30 vs R$ 132,14) compensa a diferença de volume. "Relogios Presentes" reforça o padrão: é a categoria com menor volume entre o Top 5 (5.495 pedidos), mas o maior ticket médio (R$ 230,09), garantindo a 2ª posição em faturamento.

- **São Paulo concentra a base de clientes na mesma proporção que concentra vendas.** Dos 96.096 clientes totais, 40.302 (42%) estão em SP — mais de 3x o Rio de Janeiro (12.384). A concentração se repete por cidade: a capital paulista tem 14.984 clientes (quase 4x a cidade do Rio, com 6.620), e 4 das 10 cidades com mais clientes do país estão no estado de São Paulo.

- A estrutura do dashboard também permite investigar outras questões de negócio, como:
  - Se o prazo de entrega mais longo em estados remotos afeta a taxa de cancelamento;
  - Como o ticket médio evolui mês a mês dentro de uma mesma categoria;
  - Se a concentração de clientes em SP se mantém estável ao longo dos anos ou está mudando.

---

## 🚀 Próximos Passos

Como evolução do projeto, algumas possibilidades são:

- Evoluir o projeto para uma estrutura de **pipeline de dados**, automatizando as etapas de ingestão, tratamento e disponibilização dos dados;
- Centralizar funções de formatação e estilo (hoje replicadas entre as páginas) em um módulo `utils/` compartilhado;
- Aprofundar as análises realizadas no dashboard;
- Incluir novos indicadores de negócio;
- Explorar análises de comportamento e recorrência dos clientes;
- Aplicar os conhecimentos adquiridos nos estudos de Engenharia de Dados para evoluir a arquitetura do projeto.

---

## 📁 Estrutura do Projeto

```
olistpython/
│
├── assets/
│   ├── painel_executivo.png
│   ├── desempenho_categorias.png
│   └── analise_clientes.png
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
│
├── Inicio.py
├── requirements.txt
└── README.md
```

---

## 📌 Sobre o Projeto

Este projeto faz parte do meu portfólio de **Data Analytics** e tem como objetivo demonstrar, na prática, a aplicação de Python, Pandas e ferramentas de visualização em um problema de negócio.

Mais do que construir gráficos, o projeto busca demonstrar o processo de:

**Dados → Tratamento → Métricas → Análise → Visualização → Insights**

---

## 👤 Autor

**Carlos Alberto Rodrigues de Mendonça**

Projeto desenvolvido para composição de portfólio na área de **Data Analytics**.

🔗 [GitHub](https://github.com/Carlosarmendoca)