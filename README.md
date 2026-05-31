# Miniguia de Estudos com NotebookLM — Databricks & Delta Lake

## Contexto e Objetivos

**Assunto escolhido:** Fundamentos do Databricks e Delta Lake com foco na certificação **Databricks Certified Data Engineer Associate**.

**Objetivos de estudo:**
- Compreender a arquitetura Lakehouse e como ela se diferencia de Data Warehouses e Data Lakes tradicionais
- Dominar os conceitos de Delta Lake: ACID transactions, Time Travel, schema enforcement e schema evolution
- Entender o fluxo de dados na arquitetura Medallion (Bronze → Silver → Gold)
- Conhecer os principais recursos do Databricks: clusters, jobs, notebooks, Auto Loader e Delta Live Tables
- Construir base sólida de conhecimento para a prova de certificação Data Engineer Associate

---

## Curadoria de Fontes

Fontes selecionadas e carregadas no NotebookLM:

| # | Título | Tipo | Link |
|---|--------|------|------|
| 1 | Databricks Documentation — Data Engineering | Texto | https://docs.databricks.com/en/introduction/index.html |
| 2 | Delta Lake Documentation Oficial | Texto | https://docs.delta.io/latest/index.html |
| 3 | Delta Lake: High-Performance ACID Table Storage over Cloud Object Stores (paper original) | PDF | https://www.vldb.org/pvldb/vol13/p3411-armbrust.pdf |
| 4 | Apache Spark — Spark SQL, DataFrames and Datasets Guide | Texto | https://spark.apache.org/docs/latest/sql-programming-guide.html |
| 5 | Databricks Certified Data Engineer Associate | Texto | https://www.databricks.com/learn/certification/data-engineer-associate |
| 6 | Databricks Certified Data Engineer Associate — Exam Guide | PDF | https://www.databricks.com/sites/default/files/2026-05/databricks-certified-data-engineer-associate-exam-guide-may-2026.pdf |

---

## Engenharia de Prompts e Cicatrizes

### Teste de fontes e features do notebooklm
####    Prompt 1 - Qual a mensagem do erro 0A000?
> As fontes fornecidas não contêm a mensagem específica para o erro 0A000. O material disponível apenas lista "Error Conditions" (Condições de Erro) no índice do guia do Spark SQL, mas não detalha os códigos de erro ou suas respectivas mensagens, focando apenas em uma introdução geral sobre Spark SQL, DataFrames e Datasets.
##### Contexto & Aprendizagem
A pergunta foi feita após colocar apenas a fonte (4). Como se trata de uma página com links para o conteúdo relevante e o notebooklm não faz webcrawling automático apenas o conteúdo imediatamente disponível no link é utilizado.
Uma solução viável seria fazer um webcrawler em python definindo um nível razoável de profundidade de download de páginas. Devido ao limite de fontes do notebooklm, como uma pesquisa poderia levar a vários arquivos, optou-se por gerar resultados em um único arquivo html para a url primária pesquisada. Veja mais em [Mr. Crawley](tools/README.md)
        
#### Prompt 1
**Pergunta:** "Com base nas fontes carregadas, explique a diferença entre um Data Lake, um Data Warehouse e um Lakehouse. Use exemplos práticos."

**Resposta obtida:**
<!-- Cole aqui a resposta do NotebookLM -->

**Observações / Dificuldades:**
<!-- Ex: A resposta misturou conceitos de fornecedores distintos. Foi necessário reformular pedindo para focar apenas nas fontes do Databricks. -->

---

#### Prompt 2
**Pergunta:** "Quais são as garantias ACID do Delta Lake e como o mecanismo de transaction log funciona internamente?"

**Resposta obtida:**
<!-- Cole aqui a resposta do NotebookLM -->

**Observações / Dificuldades:**
<!-- -->

---

#### Prompt 3
**Pergunta:** "Descreva a arquitetura Medallion (Bronze, Silver, Gold) e dê um exemplo de pipeline de dados real para cada camada."

**Resposta obtida:**
<!-- Cole aqui a resposta do NotebookLM -->

**Observações / Dificuldades:**
<!-- -->

---

#### Prompt 4
**Pergunta:** "Quais tópicos da documentação carregada têm maior peso na prova Databricks Data Engineer Associate? Organize por categoria."

**Resposta obtida:**
<!-- Cole aqui a resposta do NotebookLM -->

**Observações / Dificuldades:**
<!-- -->

---

## Miniguia de Estudo

### Resumos Estruturados

#### Tópico 1: Arquitetura Lakehouse

<!-- Resumo a preencher após estudo das fontes -->

#### Tópico 2: Delta Lake — ACID, Time Travel e Schema

<!-- Resumo a preencher após estudo das fontes -->

#### Tópico 3: Arquitetura Medallion (Bronze / Silver / Gold)

<!-- Resumo a preencher após estudo das fontes -->

#### Tópico 4: Databricks — Clusters, Jobs e Auto Loader

<!-- Resumo a preencher após estudo das fontes -->

#### Tópico 5: Delta Live Tables (DLT)

<!-- Resumo a preencher após estudo das fontes -->

---

### Glossário

| Conceito | Definição |
|----------|-----------|
| Lakehouse | Arquitetura que combina a flexibilidade de um Data Lake com as garantias de um Data Warehouse |
| Delta Lake | Camada de armazenamento open-source que adiciona ACID transactions sobre arquivos Parquet |
| Delta Table | Tabela gerenciada pelo Delta Lake, com transaction log associado |
| Transaction Log (`_delta_log`) | Diretório de metadados que registra cada operação na Delta Table em arquivos JSON |
| ACID | Atomicity, Consistency, Isolation, Durability — garantias de integridade transacional |
| Time Travel | Recurso que permite consultar versões históricas de uma Delta Table por versão ou timestamp |
| Schema Enforcement | Rejeita gravações que não respeitam o schema definido na tabela |
| Schema Evolution | Permite alterações no schema (ex: adição de colunas) de forma controlada |
| Medallion Architecture | Padrão de camadas Bronze (raw), Silver (limpo) e Gold (agregado/consumo) |
| Auto Loader | Ferramenta do Databricks para ingestão incremental e automática de arquivos em cloud storage |
| Delta Live Tables (DLT) | Framework declarativo do Databricks para pipelines de dados com qualidade e orquestração nativa |
| Unity Catalog | Solução de governança centralizada de dados e IA no Databricks |
| Databricks Runtime | Ambiente de execução baseado em Apache Spark, otimizado para o Databricks |
| Job | Unidade de agendamento e orquestração de notebooks ou scripts no Databricks |
| Cluster | Conjunto de máquinas virtuais que executam workloads Spark no Databricks |

---

### Prompts Reutilizáveis para Revisão

```
1. "Resuma os pontos principais sobre [tópico] em até 5 tópicos objetivos, com base nas fontes carregadas."
```

```
2. "Quais são as principais diferenças entre [conceito A] e [conceito B]? Inclua quando usar cada um."
```

```
3. "Crie 10 perguntas no estilo da prova Databricks Data Engineer Associate sobre [tópico], com gabarito comentado."
```

```
4. "Explique [conceito] como se eu fosse um engenheiro de dados vindo de SQL tradicional, sem experiência com Spark."
```

```
5. "Liste os erros mais comuns de iniciantes ao trabalhar com [Delta Lake / DLT / Auto Loader] e como evitá-los."
```
