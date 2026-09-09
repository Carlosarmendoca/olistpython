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

## 💡 Principais Insights

A navegação pelos dashboards permitiu identificar alguns padrões relevantes no comportamento de vendas, clientes e logística da Olist.

### 1. São Paulo lidera em faturamento, mas tem ticket médio 14% menor que o Rio de Janeiro, que está em segundo lugar

São Paulo concentra o maior faturamento, com R$ 5,77 milhões, quase três vezes o valor registrado pelo Rio de Janeiro, que ocupa a segunda posição (R$ 2,06 milhões).

Apesar disso, o ticket médio paulista é 14% menor: R$ 142,47 contra R$ 166,45 no Rio de Janeiro.

**Leitura:** São Paulo apresenta maior volume de pedidos, enquanto o Rio de Janeiro possui pedidos de maior valor médio.

### 2. Estados remotos apresentam menor volume e maior ticket médio

O Acre registra apenas 80 pedidos, o menor volume entre os estados analisados. Em contrapartida, apresenta o maior ticket médio, de R$ 244,83, acompanhado pelo maior prazo médio de entrega: 21 dias.

Para comparação, São Paulo apresenta prazo médio de 8,7 dias.

**Leitura:** os dados mostram uma combinação de baixo volume, maior valor por pedido e maior prazo de entrega em estados mais distantes dos principais centros de distribuição.

**Hipótese a investigar:** a distância logística pode estar relacionada ao comportamento observado de ticket e prazo, mas essa relação exigiria uma análise adicional para ser confirmada.

### 3. A categoria com maior faturamento não é a que possui maior volume

A categoria Beleza Saúde lidera em faturamento, com R$ 1,41 milhão, superando Cama Mesa Banho, que registra R$ 1,23 milhão.

Entretanto, Cama Mesa Banho possui maior volume de pedidos (9.272 contra 8.647).

A diferença é explicada pelo ticket médio: R$ 163,30 em Beleza Saúde contra R$ 132,14 em Cama Mesa Banho.

O comportamento também aparece em Relógios Presentes, que possui o menor volume entre as cinco principais categorias (5.495 pedidos), mas apresenta o maior ticket médio (R$ 230,09), alcançando a segunda posição em faturamento.

**Leitura:** volume de pedidos, isoladamente, não determina o faturamento. O valor médio dos pedidos exerce papel importante no desempenho das categorias.

### 4. A concentração de clientes acompanha a concentração das vendas

São Paulo possui 40.302 dos 96.096 clientes, representando aproximadamente 42% da base total.

O estado também apresenta forte vantagem sobre o Rio de Janeiro, que possui 12.384 clientes.

Essa concentração se repete no nível municipal: a cidade de São Paulo possui 14.984 clientes, quase quatro vezes o número registrado pela cidade do Rio de Janeiro (6.620).

Além disso, 4 das 10 cidades com maior número de clientes estão no estado de São Paulo.

**Leitura:** A concentração de clientes em São Paulo acompanha sua liderança em faturamento, indicando forte concentração da operação nesse estado.

### 🔎 Questões para investigação

Além dos padrões identificados, os dashboards permitem explorar novas hipóteses de negócio:

- **Logística:** estados com maior prazo médio de entrega apresentam também maiores taxas de cancelamento?
- **Categorias:** como o ticket médio de cada categoria evolui ao longo do tempo?
- **Clientes:** a participação de São Paulo na base de clientes permanece estável ou apresenta mudanças ao longo dos anos?
- **Faturamento:** estados com maior ticket médio também apresentam maior receita por cliente?
- **Experiência de compra:** existe relação entre prazo de entrega e comportamento de compra dos clientes?

### 🎯 Conclusão

Os dados mostram que volume de pedidos, ticket médio, localização dos clientes e desempenho logístico não necessariamente caminham na mesma direção. A análise conjunta dessas dimensões permite identificar diferenças importantes entre estados e categorias que poderiam passar despercebidas ao observar apenas o faturamento total.

---

## 🚀 Próximos Passos

Como evolução do projeto, algumas possibilidades são:

- Aprofundar as análises de comportamento e recorrência dos clientes;
- Explorar novas métricas e indicadores de negócio;
- Investigar relações entre desempenho logístico e comportamento de compra;
- Centralizar funções de formatação e estilo em um módulo `utils/`;
- Evoluir a preparação dos dados para uma estrutura mais automatizada de processamento;
- Aplicar conceitos de Engenharia de Dados estudados em projetos futuros, explorando etapas como ingestão, transformação, armazenamento e orquestração de dados.

---

## 📁 Estrutura do Projeto

```
olistpython/
│
├── assets/
│   ├── painel_executivo_1.png ... painel_executivo_4.png
│   ├── desempenho_categorias_1.png ... desempenho_categorias_4.png
│   └── analise_clientes_1.png ... analise_clientes_4.png
│
├── dados/
│   ├── pedidos_limpo.csv
│   ├── clientes_limpo.csv
│   ├── itens_limpo.csv
│   ├── pagamentos_limpo.csv
│   ├── produtos_limpo.csv
│   └── brazil_states.geojson
│
├── Notebooks/
│   └── Análises e exploração dos dados
│
├── pages/
│   ├── 1_📊_Painel_Executivo.py
│   ├── 2_🏆_Desempenho_Categorias.py
│   └── 3_👥_Analise_Clientes.py
│
├── views/
│   └── Funções de preparação das bases
│
├── .gitignore
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