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

| # | Título | Tipo | Link | Processado com * | 
|---|--------|------|------|----------------|
| 1 | Databricks Documentation — Data Engineering | PDF** | https://docs.databricks.com/en/introduction/index.html | Mr. Crawley --depth 1 (mai/2026) |
| 2 | Delta Lake Documentation Oficial | PDF** | https://docs.delta.io/latest/index.html | Mr. Crawley --depth 1 (mai/2026) |
| 3 | Delta Lake: High-Performance ACID Table Storage over Cloud Object Stores (paper original) | PDF | https://www.vldb.org/pvldb/vol13/p3411-armbrust.pdf | Download direto (mai/2026) |
| 4 | Apache Spark — Spark SQL, DataFrames and Datasets Guide | PDF** | https://spark.apache.org/docs/latest/sql-programming-guide.html | Mr. Crawley --depth 1 (mai/2026) |
| 5 | Databricks Certified Data Engineer Associate — Exam Guide | PDF | https://www.databricks.com/sites/default/files/2026-05/databricks-certified-data-engineer-associate-exam-guide-may-2026.pdf | Download direto (mai/2026) |

\* Durante a curadoria foi observada a necessidade de um webcrawler para páginas com links. Detalhes no primeiro prompt.

\*\* Sites consolidados em html com Mr. Crawley e convertidos para PDF.  

---

## Engenharia de Prompts e Cicatrizes

### Teste de fontes e features do notebooklm

####    Prompt 1 - Qual a mensagem do erro 0A000?
> As fontes fornecidas não contêm a mensagem específica para o erro 0A000. O material disponível apenas lista "Error Conditions" (Condições de Erro) no índice do guia do Spark SQL, mas não detalha os códigos de erro ou suas respectivas mensagens, focando apenas em uma introdução geral sobre Spark SQL, DataFrames e Datasets.
##### Contexto & Aprendizagem
A pergunta foi feita após colocar apenas a fonte (4). Como se trata de uma página com links para o conteúdo relevante e o notebooklm não faz webcrawling automático apenas o conteúdo imediatamente disponível no link é utilizado.
Uma solução viável seria fazer um webcrawler em python definindo um nível razoável de profundidade de download de páginas. Devido ao limite de fontes do notebooklm, como uma pesquisa poderia levar a vários arquivos, optou-se por gerar resultados em um único arquivo html para a url primária pesquisada. Veja mais em [Mr. Crawley](tools/README.md)

Após gerar um pdf, baixando o conteúdo das páginas com profundidade de links=1, e trocando a fonte no notebooklm do link (4) para o pdf consolidado, obtemos - após um tempo consideravelmente maior de loading dado o tamanho da referência - a resposta:
> No Spark SQL, o código 0A000 não se refere a uma única mensagem de erro, mas sim a um SQLSTATE (estado de erro) genérico que agrupa uma grande variedade de condições e subcondições de erro. Na prática, este código é utilizado para categorizar operações, tipos ou recursos que não são suportados pelo Spark (equivalente à classe de erro de "Feature Not Supported" no padrão SQL).
>
> A mensagem exata exibida no console dependerá da operação específica que falhou. Aqui estão algumas das principais mensagens e subcondições que acionam o erro 0A000:
>
>    CANNOT_INVOKE_IN_TRANSFORMATIONS: "Dataset transformations and actions can only be invoked by the driver, not inside of other Dataset transformations" (Transformações e ações de Dataset só podem ser invocadas pelo driver, e não dentro de outras transformações de Dataset).
>    CONCURRENT_QUERY: "Another instance of this query was just started by a concurrent session." (Outra instância desta consulta acabou de ser iniciada por uma sessão simultânea).
>    DATATYPE_CANNOT_ORDER: "Type <dataType> does not support ordered operations." (O tipo de dado especificado não suporta operações de ordenação).
>    DISTINCT_WINDOW_FUNCTION_UNSUPPORTED: "Distinct window functions are not supported." (Funções de janela com a cláusula DISTINCT não são suportadas).
>    CANNOT_UPDATE_FIELD: Ocorre quando se tenta atualizar diretamente um campo cujo tipo de dado não suporta a operação direta, como estruturas aninhadas (ARRAY, MAP, STRUCT ou INTERVAL).
>    UNSUPPORTED_DATATYPE: "Unsupported data type <typeName>." (O tipo de dado não é suportado).
>    UNSUPPORTED_JOIN_TYPE: "Unsupported join type <typ>." (O tipo de junção (JOIN) exigido não é suportado pelo Spark).
>    UNSUPPORTED_SAVE_MODE: "The save mode <saveMode> is not supported for: an existent/non-existent path." (O modo de salvamento utilizado não é suportado para caminhos já existentes ou inexistentes).
>    NOT_SUPPORTED_COMMAND_WITHOUT_HIVE_SUPPORT: O comando não é suportado a menos que o suporte ao Hive seja ativado através da configuração "spark.sql.catalogImplementation" para "hive".
>
> Como resolver: Como o código 0A000 abrange uma ampla gama de funcionalidades não suportadas, a forma correta de diagnosticar o erro é observar a subcondição que acompanha o código de estado na sua mensagem de erro (por exemplo, #UNSUPPORTED_DATATYPE ou #CANNOT_UPDATE_FIELD) e corrigir a lógica da sua consulta ou código de acordo com a limitação apontada pelo Spark.



### Prompt 2 - outra pergunta aqui?

        
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
