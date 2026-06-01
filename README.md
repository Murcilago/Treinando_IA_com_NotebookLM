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

###    Prompt 1 - Qual a mensagem do erro 0A000?
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



### Prompt 2 - Com base nas fontes carregadas, explique a diferença entre um Data Lake, um Data Warehouse e um Lakehouse. Use exemplos práticos.

> Um Data Warehouse fornece dados limpos e estruturados e é otimizado para gerar relatórios de Business Intelligence (BI). Esses sistemas são projetados para dados que não mudam com alta frequência, a fim de evitar conflitos entre consultas simultâneas. No entanto, eles geralmente dependem de formatos proprietários, o que limita o suporte para cargas de trabalho de ciência de dados e Machine Learning (ML).
>
>    Exemplo prático: Uma plataforma corporativa voltada exclusivamente para analistas de negócios, que gera painéis (dashboards) e relatórios gerenciais a partir de dados históricos e imutáveis, mas que não serve para o treinamento de modelos de inteligência artificial.
>
> Um Data Lake surgiu como uma solução para armazenar e processar dados de forma barata e eficiente em resposta ao aumento exponencial dos tipos e volumes de dados. Ele armazena permanentemente dados de qualquer natureza e em qualquer formato. É muito utilizado para ciência de dados e ML, mas não é adequado para relatórios de BI devido à sua natureza bruta e não validada.
>
>    Exemplo prático: Um repositório de baixo custo onde a empresa "despeja" todos os seus dados brutos de forma não estruturada (como imagens, arquivos JSON ou vídeos). Cientistas de dados podem explorar essas informações para treinar algoritmos, mas a equipe de negócios não consegue usar esses dados diretamente para métricas financeiras precisas.
>
> Um Data Lakehouse é um sistema de gerenciamento que combina os benefícios de ambos. Ele oferece o acesso aberto e o armazenamento barato em formatos padrão de um Data Lake, aliados aos protocolos de indexação, baixa latência de consulta e alta confiabilidade típicos de um Data Warehouse. O objetivo principal é evitar sistemas isolados e estabelecer uma única fonte da verdade para a organização.
>
>    Exemplo prático: Uma arquitetura unificada (como o padrão Medallion) onde os dados brutos de várias fontes chegam e são armazenados de forma barata (camada Bronze). Esses dados são então validados e enriquecidos com a confiabilidade de transações ACID (camada Prata) e organizados em tabelas finais (camada Gold). A partir desse mesmo ambiente, um cientista de dados pode extrair recursos para um aplicativo de Machine Learning, enquanto um analista de negócios gera um dashboard de BI em tempo real, sem a necessidade de duplicar ou sincronizar os dados entre sistemas diferentes.

##### Contexto & Aprendizagem

A resposta foi validada com um segundo modelo (ChatGPT), que inicialmente apontou imprecisões técnicas. Após apresentar as fontes utilizadas, o modelo revisou sua crítica e concluiu que a resposta é uma **síntese fiel da visão Databricks/Delta Lake**, não um erro factual.
  
  O aprendizado principal: as fontes carregadas foram produzidas pelos próprios criadores do Lakehouse, o que gera um viés de origem natural — Data Warehouse e Data Lake são apresentados de forma simplificada para justificar a existência do Lakehouse. Para a certificação Databricks, essa é exatamente a visão esperada. Para estudos aprofundados de conceitos técnicos a curadoria de fontes deve ser feita com muito cuidado.

### Prompt 3 - Quais são as garantias ACID do Delta Lake e como o mecanismo de transaction log funciona internamente?
> O Delta Lake fornece garantias ACID (Atomicidade, Consistência, Isolamento, Durabilidade) sobre data lakes estendendo arquivos de dados Parquet com um log de transações baseado em arquivos.
Garantias ACID do Delta Lake:
>
>    Isolamento Serializável: O Delta Lake assegura transações com o nível de isolamento serializável (Serializable isolation level), garantindo que os leitores tenham sempre uma visualização de snapshot consistente e que nunca vejam dados inconsistentes, mesmo na presença de leituras e escritas simultâneas em múltiplos clusters.
>    Controle de Concorrência Otimista (Optimistic Concurrency Control): As garantias entre escritas concorrentes são gerenciadas de forma otimista. O processo ocorre em até três etapas lógicas principais: (1) Leitura da versão mais recente disponível para identificar arquivos a serem modificados; (2) Escrita das modificações escrevendo os novos arquivos de dados de forma temporária; e (3) Validação e Commit, onde o Delta verifica antes de aplicar se as mudanças conflitam com alguma outra alteração executada concorrentemente. Se não houver conflitos, as mudanças entram como uma nova versão atômica da tabela; caso existam conflitos, a operação falha para proteger a tabela de corrompimento de dados.
>
> Como o mecanismo de Transaction Log funciona internamente: O mecanismo que viabiliza essas garantias e as operações avançadas é o log de transações, que rastreia todo o estado da tabela diretamente no armazenamento de objetos da nuvem.
>
>    Estrutura de Armazenamento: O log é armazenado fisicamente em um subdiretório chamado _delta_log dentro do diretório principal da tabela.
>    Registros de Log em JSON: Todas as modificações da tabela criam arquivos no formato JSON com nomes representados por IDs numéricos crescentes (como 000001.json, 000002.json, etc). Cada um desses arquivos json encapsula de forma imutável um array de ações aplicadas à versão imediatamente anterior para compor a versão atual.
>    As Ações (Actions): Dentro dos logs, o Delta armazena o delta de mudanças, incluindo:
>        Add / Remove Files: Metadados que apontam que um arquivo físico de dados foi inserido ou excluído. Ao adicionar, são incluídas estatísticas ricas desse arquivo (como contagem de linhas e min/max das colunas) que tornam consultas altamente otimizadas e evitam listar arquivos ativamente no storage de nuvem.
>        Change Metadata: Modificações estruturais, de esquema, ou formato de armazenamento.
>        Update Application Transaction IDs: Ferramenta para gerenciar idenificadores de transação customizados úteis para garantir semântica exactly-once (exatamente uma vez) para processos de streaming, assegurando que o lote de processamento não seja inserido duas vezes se a aplicação falhar.
>    Atomicidade de Gravação do Log: O sucesso de um commit depende da criação atômica do próprio arquivo json. Se duas aplicações tentarem registrar o 000003.json ao mesmo tempo, sistemas baseados em arquivos na nuvem (ou coordenadores de concorrência) assegurarão que apenas uma consiga, e a outra terá que tentar na próxima versão (000004.json), resolvendo o conflito sem danificar os dados.
>    Checkpoints (Compactação do Log em Parquet): Apenas usar arquivos JSON faria a leitura do histórico e do estado atual demorar com o tempo. Para contornar isso, o Delta Lake processa e comprime logs periodicamente em Checkpoints (por padrão, a cada 10 transações) gerados em arquivos Apache Parquet. Esses checkpoints guardam todo o estado válido, removendo ações redundantes (ex: se um arquivo foi listado num "Add" no log 1, e teve um "Remove" no log 5, no checkpoint 10 isso é resumido). O uso de um formato colunar como o Parquet para os checkpoints entrega uma performance absurdamente mais alta para entender quais arquivos pertencem à tabela.

##### Contexto & Aprendizagem

A resposta foi validada com um segundo modelo (ChatGPT), que a classificou como tecnicamente sólida. Diferente do Prompt 2, não há viés relevante de fonte — a explicação está alinhada com a arquitetura real do Delta Lake, com forte referência ao paper original (fonte 3).

Dois conceitos centrais ficaram implícitos e merecem destaque:

- Snapshot Reconstruction: o estado atual da tabela é reconstruído pelo algoritmo checkpoint mais recente + logs posteriores = snapshot atual — o conceito mais importante do transaction log.
- Time Travel: a capacidade de consultar versões históricas (VERSION AS OF) é consequência direta da arquitetura versionada do log; a resposta não conectou os dois.

Dito isso, um terceiro modelo (Claude) avaliou ambas as respostas e apontou que o ChatGPT frequentemente enfatiza detalhes de implementação sem relevância para o nível de estudo, o que pode aumentar a complexidade desnecessariamente ou induzir quem está iniciando a erros. Mais uma vez a curadoria se mostra importante: para não errar por falta, boas fontes; para não errar por excesso, o NotebookLM — desde que bem alimentado — tende a ser mais eficaz que modelos generalistas.


### Prompt 4 - Descreva a arquitetura Medallion (Bronze, Silver, Gold) e dê um exemplo de pipeline de dados real para cada camada.

##### Contexto & Aprendizagem

### Prompt 5 - Quais tópicos da documentação carregada têm maior peso na prova Databricks Data Engineer Associate? Organize por categoria.

##### Contexto & Aprendizagem

---

## Miniguia de Estudo

### Resumos Estruturados

#### Tópico 1: Arquitetura Lakehouse

*    O que é: Um sistema de gerenciamento de dados que une o melhor de dois mundos, combinando os benefícios de escalabilidade, flexibilidade e baixo custo dos Data Lakes com a confiabilidade, estruturação e performance de consultas dos Data Warehouses.
*    Por que foi criado: Para unificar e acelerar soluções de dados, estabelecendo uma plataforma única com acesso direto a formatos de dados abertos padrão (como Parquet), aliando isso a protocolos de indexação para apoiar simultaneamente equipes de BI (Business Intelligence), engenharia e ciência de dados/ML.
*    Quais problemas resolve: Elimina os "silos de dados" isolados e a necessidade de duplicar dados entre sistemas diferentes para diversas cargas de trabalho. Com isso, reduz custos redundantes, garante uma "única fonte da verdade" (single source of truth) e resolve as falhas de consistência (falta de transações ACID) inerentes aos sistemas básicos de armazenamento em nuvem.
*    Componente Essencial - Motor e Armazenamento Otimizado: A arquitetura no Databricks é construída sobre o Apache Spark (motor de processamento distribuído, massivamente escalável) e o Delta Lake (camada de armazenamento otimizada que garante transações ACID, cumprimento de esquema e manipulação eficiente de metadados sobre arquivos na nuvem).
*    Componente Essencial - Governança Unificada: O Unity Catalog atua como o pilar de segurança do Lakehouse, fornecendo uma solução unificada de governança com controle de acesso refinado (granular), auditoria, rastreamento de linhagem de dados e descoberta de ativos de dados e IA em todos os workspaces.
*    Padrão de Design (Medallion Architecture): O Lakehouse utiliza tipicamente a Arquitetura Medalhão (composta pelas camadas Bronze, Prata e Ouro), estruturando os dados de forma que eles sejam ingeridos brutos, progressivamente limpos, validados, enriquecidos e, por fim, agregados para o consumo final do negócio.

#### Tópico 2: Delta Lake — ACID, Time Travel e Schema

*    Fundamento do Delta Lake: É a camada de armazenamento otimizada e o formato padrão no Databricks. Ele estende arquivos de dados abertos Apache Parquet adicionando um log de transações (transaction log) que rastreia os metadados de forma escalável.
*    Transações ACID: O Delta Lake utiliza controle de concorrência otimista e garante o nível de isolamento serializável para as operações. Isso permite a unificação confiável de cargas de trabalho em lote (batch) e fluxo contínuo (streaming), garantindo que leitores concorrentes nunca visualizem dados inconsistentes em caso de gravação parcial ou falha.
*    Time Travel (Viagem no Tempo): Permite acessar snapshots (versões do estado exato) anteriores de uma tabela. É executado através da sintaxe SQL VERSION AS OF <versão> ou TIMESTAMP AS OF <data_hora>. É utilizado principalmente para reverter modificações ou deleções acidentais (rollbacks), auditoria e para reprodutibilidade de modelos de Machine Learning.
*    Retenção e Time Travel: Para viajar no tempo, tanto o log quanto os arquivos Parquet antigos devem estar disponíveis. O histórico do log é mantido por 30 dias por padrão (configurável via delta.logRetentionDuration), desde que os arquivos de dados subjacentes não tenham sido apagados permanentemente pelo comando de limpeza VACUUM.
*    Schema Enforcement (Imposição de Esquema): O Delta adota um modelo rígido de validação na gravação (schema-on-write). Ele rejeita automaticamente transações que tentem inserir colunas inexistentes ou com tipos de dados incompatíveis com o esquema da tabela destino, impedindo a injeção de dados de má qualidade (bad records) no Data Lake.
*    Schema Evolution (Evolução Automática de Esquema): O esquema de uma tabela pode evoluir automaticamente para acomodar novos dados. Durante a gravação (append ou overwrite), basta utilizar a opção .option("mergeSchema", "true") na API do DataFrame para que as novas colunas originadas da fonte sejam assimiladas dinamicamente à estrutura da tabela.
*    Evolução Explícita (DDL) e Column Mapping: A evolução estrutural também pode ser feita explicitamente com comandos como ALTER TABLE (para adicionar ou reordenar colunas). Operações destrutivas ou de renomeação, como excluir (DROP) ou renomear (RENAME) colunas, só podem ser executadas como operações rápidas apenas de metadados — sem a necessidade de reescrever fisicamente todos os arquivos Parquet afetados — se o recurso de Column Mapping estiver ativado na tabela

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
