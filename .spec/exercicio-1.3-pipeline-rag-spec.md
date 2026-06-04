# Exercício 1.3 - Construção de Pipeline RAG

**Nome:** Leonardo Santana  
**Papel/Cargo:** Desenvolvedor  
**Data:** 2026-06-04  

--- 

# Análise Inicial (Humana)

## Entendimento do Problema

A NovaTech possui um volume significativo de documentação distribuída entre diferentes fontes de conhecimento, incluindo documentos operacionais, políticas corporativas, procedimentos internos e tabelas de referência.

O principal objetivo da solução é permitir que atendentes obtenham respostas rápidas e confiáveis utilizando linguagem natural, reduzindo o tempo gasto na busca manual de informações e aumentando a consistência das respostas fornecidas aos clientes.

Entretanto, modelos de linguagem não possuem capacidade nativa de consultar documentos corporativos atualizados. Mesmo quando possuem conhecimento sobre determinados assuntos, esse conhecimento pode estar desatualizado, incompleto ou não refletir as regras específicas adotadas pela organização.

Dessa forma, torna-se necessário utilizar uma arquitetura baseada em Retrieval-Augmented Generation (RAG), permitindo que informações relevantes sejam recuperadas dinamicamente da base documental e utilizadas como contexto durante a geração da resposta.

---

## Papel do Pipeline RAG

O pipeline RAG é responsável por conectar a base de conhecimento corporativa ao modelo de linguagem.

Sua função não é apenas armazenar documentos, mas garantir que o conteúdo correto seja recuperado no momento da consulta.

O sucesso da solução depende diretamente da capacidade do pipeline de recuperar informações relevantes, completas e atualizadas.

Mesmo um modelo avançado apresentará respostas incorretas caso receba documentos inadequados ou contexto insuficiente.

Por esse motivo, a qualidade do mecanismo de recuperação possui impacto direto na qualidade das respostas produzidas pelo assistente.

---

## Principais Desafios Identificados

Durante a análise inicial foram identificados desafios técnicos relevantes que precisam ser considerados durante a construção da solução.

### Recuperação de Contexto Relevante

O primeiro desafio consiste em garantir que os documentos mais relevantes sejam recuperados para cada consulta realizada.

Uma recuperação inadequada pode levar o modelo a responder utilizando informações incompletas ou não relacionadas à pergunta do usuário.

Por esse motivo, a estratégia de indexação e busca possui papel fundamental na arquitetura proposta.

---

### Estratégia de Chunking

Os documentos corporativos normalmente possuem tamanho superior ao contexto que pode ser enviado ao modelo durante cada consulta.

Dessa forma, torna-se necessário dividir os documentos em fragmentos menores (chunks).

Entretanto, uma fragmentação excessiva pode causar perda de contexto, enquanto fragmentos muito grandes podem reduzir a precisão da recuperação.

O desafio consiste em encontrar um equilíbrio que preserve significado sem comprometer a eficiência da busca.

---

### Preservação da Semântica

Durante o processo de chunking existe o risco de separar informações que possuem dependência contextual.

Esse problema é especialmente relevante em procedimentos operacionais, políticas corporativas e tabelas de regras.

Uma estratégia inadequada pode fazer com que apenas parte da informação seja recuperada, comprometendo a interpretação correta do conteúdo.

---

### Atualização da Base de Conhecimento

A documentação da NovaTech sofre atualizações periódicas realizadas por diferentes áreas da empresa.

O pipeline deve permitir a reindexação dos documentos de forma simples, garantindo que novas versões sejam refletidas nas consultas futuras.

Sem esse mecanismo existe o risco de utilização de informações obsoletas.

---

### Avaliação da Qualidade da Recuperação

A simples geração de uma resposta aparentemente correta não garante que o pipeline esteja funcionando adequadamente.

É necessário validar se os documentos recuperados são realmente aqueles esperados para cada consulta.

Por esse motivo, a avaliação deve considerar não apenas a resposta final do modelo, mas também a qualidade dos chunks recuperados durante a etapa de busca.

---

## Estratégia Inicial Proposta

Considerando os requisitos do cenário, a estratégia inicial consiste em construir um pipeline simplificado composto pelas seguintes etapas:

1. Ingestão dos documentos.
2. Processamento e chunking do conteúdo.
3. Geração de embeddings.
4. Armazenamento em banco vetorial.
5. Busca por similaridade semântica.
6. Montagem do contexto para o LLM.
7. Geração da resposta fundamentada na documentação recuperada.

Essa abordagem permite validar os principais conceitos envolvidos em uma arquitetura RAG sem introduzir complexidades desnecessárias para o escopo da prova de conceito.

---

## Critérios de Sucesso

Para que o pipeline seja considerado adequado para o cenário da NovaTech, ele deve ser capaz de:

- Recuperar documentos relevantes para cada consulta.
- Preservar o contexto necessário para interpretação correta das informações.
- Reduzir riscos de alucinação através do grounding documental.
- Permitir atualização da base de conhecimento.
- Apresentar rastreabilidade entre pergunta, documentos recuperados e resposta produzida.
- Demonstrar funcionamento completo do fluxo de ingestão, indexação e recuperação.

Esses critérios serão utilizados para orientar as decisões técnicas adotadas durante a implementação da prova de conceito e servirão como referência para avaliação dos resultados obtidos.

---

# Arquitetura Proposta

## Visão Geral

A arquitetura proposta segue o padrão Retrieval-Augmented Generation (RAG), permitindo que o modelo de linguagem utilize informações corporativas da NovaTech durante o processo de geração de respostas.

O objetivo principal da arquitetura é reduzir a dependência do conhecimento pré-treinado do modelo e garantir que as respostas sejam fundamentadas em documentos oficiais da organização.

A solução foi estruturada em etapas independentes e desacopladas, permitindo evolução gradual dos componentes sem necessidade de reestruturação completa da plataforma.

O fluxo completo consiste na ingestão dos documentos, processamento do conteúdo, geração de embeddings, armazenamento vetorial, recuperação semântica e montagem do contexto utilizado pelo modelo de linguagem.

---

## Componentes da Solução

A arquitetura é composta pelos seguintes componentes principais:

### 1. Camada de Ingestão

Responsável por realizar a leitura dos documentos disponibilizados para a solução.

Nesta prova de conceito serão utilizados documentos em formato Markdown, simulando os conteúdos corporativos disponibilizados pela NovaTech.

O objetivo desta camada é transformar arquivos físicos em conteúdo estruturado que possa ser processado pelas etapas seguintes.

---

### 2. Camada de Processamento e Chunking

Após a ingestão, os documentos passam por um processo de segmentação em fragmentos menores (chunks).

Essa etapa é necessária porque documentos completos normalmente excedem o volume ideal de contexto para recuperação e utilização pelo modelo.

A estratégia de chunking deve preservar a semântica do conteúdo e evitar a fragmentação de informações que possuam dependência contextual.

---

### 3. Camada de Vetorização

Cada chunk gerado é convertido em um vetor numérico através de um modelo de embeddings.

Essa representação vetorial permite comparar semanticamente perguntas e documentos, independentemente de correspondências literais de palavras.

O objetivo é possibilitar buscas baseadas em significado e não apenas em palavras-chave.

---

### 4. Banco Vetorial

Os embeddings produzidos durante a vetorização são armazenados em uma base vetorial.

Essa camada é responsável por indexar os vetores e permitir consultas de similaridade semântica de forma eficiente.

Durante a execução da prova de conceito será utilizado um banco vetorial local, suficiente para validar os conceitos de recuperação semântica sem adicionar complexidades de infraestrutura.

---

### 5. Camada de Recuperação

Quando uma pergunta é realizada, a consulta também é transformada em embedding.

Esse embedding é utilizado para localizar os chunks mais semanticamente próximos dentro da base vetorial.

O resultado dessa etapa é um conjunto reduzido de documentos relevantes que serão utilizados como contexto para geração da resposta.

---

### 6. Montagem de Contexto

Os chunks recuperados são organizados e combinados com o System Prompt antes de serem enviados ao modelo de linguagem.

Essa etapa possui papel crítico na qualidade das respostas, pois define quais informações disputarão espaço dentro da janela de contexto disponível.

A organização adequada dos documentos recuperados reduz riscos associados ao fenômeno conhecido como "lost in the middle" e melhora a utilização do contexto pelo modelo.

---

### 7. Geração de Resposta

O modelo de linguagem recebe o System Prompt, os chunks recuperados e a pergunta do usuário.

A resposta deve ser produzida utilizando exclusivamente as informações presentes no contexto fornecido, seguindo os guardrails definidos para a solução.

Essa abordagem reduz riscos de alucinação e aumenta a confiabilidade das respostas apresentadas aos atendentes.

---

## Fluxo de Processamento

O fluxo operacional da solução pode ser representado da seguinte forma:

```text
Documentos (.md)
        ↓
Ingestão
        ↓
Chunking
        ↓
Embeddings
        ↓
Banco Vetorial
        ↓
Pergunta do Usuário
        ↓
Busca Semântica
        ↓
Top-K Chunks
        ↓
Montagem de Contexto
        ↓
LLM
        ↓
Resposta
```

---

## Tecnologias Selecionadas

| Componente | Tecnologia |
|------------|------------|
| Linguagem | Python |
| Documentos | Markdown |
| Embeddings | all-MiniLM-L6-v2 |
| Banco Vetorial | ChromaDB |
| Busca Semântica | Similaridade Vetorial |
| LLM | Claude (simulação do comportamento final) |

---

## Justificativa Técnica

A escolha das tecnologias foi realizada considerando simplicidade de implementação, baixo custo operacional e aderência ao objetivo da prova de conceito.

O Python foi selecionado por possuir amplo ecossistema para aplicações de IA e RAG.

O modelo de embeddings all-MiniLM-L6-v2 foi escolhido por apresentar bom equilíbrio entre desempenho, velocidade e consumo de recursos, sendo amplamente utilizado em protótipos de recuperação semântica.

O ChromaDB foi adotado por permitir execução local, fácil integração com Python e baixa complexidade operacional, características adequadas para validação dos conceitos propostos no exercício.

A utilização de documentos Markdown simplifica o processo de ingestão e facilita a rastreabilidade das informações utilizadas durante os testes.

---

## Benefícios Esperados

A arquitetura proposta busca atender aos principais objetivos da NovaTech:

- Redução do tempo de busca por informações.
- Maior consistência das respostas fornecidas aos clientes.
- Redução da dependência de conhecimento tácito dos colaboradores.
- Facilidade de atualização da base documental.
- Menor risco de respostas não fundamentadas.
- Possibilidade de evolução futura para ambientes corporativos de maior escala.

A adoção dessa arquitetura permite validar os principais conceitos envolvidos em soluções RAG, mantendo o escopo adequado para uma prova de conceito e fornecendo uma base sólida para futuras evoluções.

---

# Estratégia de Chunking

## Objetivo

A estratégia de chunking tem como objetivo dividir os documentos da NovaTech em unidades menores que possam ser indexadas e recuperadas de forma eficiente pelo pipeline RAG, preservando o significado das informações e reduzindo perdas de contexto durante a busca semântica.

O principal desafio desta etapa consiste em equilibrar precisão de recuperação e preservação semântica. Chunks excessivamente pequenos podem fragmentar informações relacionadas, enquanto chunks muito grandes podem reduzir a qualidade da recuperação e desperdiçar espaço na janela de contexto do modelo.

---

## Estratégia Adotada

Considerando que os documentos fornecidos pela NovaTech estão em formato Markdown e possuem estrutura textual relativamente organizada, será utilizada uma estratégia de chunking baseada em estrutura documental.

A segmentação seguirá prioritariamente a organização lógica dos documentos, respeitando:

- Títulos principais.
- Subtítulos.
- Seções funcionais.
- Listas.
- Tabelas.
- Blocos de texto relacionados.

Sempre que possível, cada chunk representará uma unidade semântica completa.

O objetivo é evitar que regras, exceções ou procedimentos sejam divididos entre múltiplos chunks.

---

## Preservação de Contexto

Durante o processo de segmentação será utilizado overlap entre chunks consecutivos.

O overlap reduz o risco de perda de informações localizadas próximas aos limites de divisão dos documentos.

Essa abordagem aumenta a probabilidade de recuperação correta quando uma informação relevante encontra-se distribuída entre duas seções adjacentes.

---

## Tamanho dos Chunks

Para esta prova de conceito será adotado um tamanho aproximado entre 300 e 500 tokens por chunk.

A escolha desse intervalo busca equilibrar:

### Precisão de Recuperação

Chunks menores tendem a produzir resultados mais específicos durante a busca semântica.

### Preservação Semântica

Chunks maiores preservam melhor o contexto necessário para interpretação correta das informações.

### Compatibilidade com Embeddings

O tamanho definido permanece adequado ao modelo de embeddings utilizado na prova de conceito, evitando perdas significativas de conteúdo durante a vetorização.

---

## Tratamento de Tabelas

Tabelas representam um caso especial dentro da estratégia de chunking.

Sempre que possível, tabelas serão preservadas como unidades indivisíveis.

A fragmentação de tabelas pode comprometer a relação entre linhas e colunas, reduzindo significativamente a qualidade da recuperação e dificultando a interpretação posterior pelo modelo de linguagem.

---

## Metadados dos Chunks

Cada chunk armazenado no banco vetorial será acompanhado de metadados auxiliares.

Os metadados previstos incluem:

- Nome do documento.
- Tipo do documento.
- Seção de origem.
- Identificador do chunk.
- Ordem original dentro do documento.

Essas informações aumentam a rastreabilidade da recuperação e facilitam futuras evoluções relacionadas a filtragem, auditoria e governança documental.

---

## Benefícios Esperados

A estratégia adotada busca proporcionar:

- Melhor qualidade de recuperação semântica.
- Preservação das relações entre regras e exceções.
- Redução de perda de contexto.
- Maior rastreabilidade das informações recuperadas.
- Melhor utilização da janela de contexto do modelo.

Além disso, a abordagem permanece suficientemente simples para implementação dentro do escopo da prova de conceito proposta pelo exercício.

---

## Limitações Conhecidas

Embora adequada para validação dos conceitos centrais de RAG, a estratégia proposta possui algumas limitações.

O tamanho ideal dos chunks depende diretamente do modelo de embeddings utilizado, do domínio dos documentos e do perfil das consultas realizadas pelos usuários.

Por esse motivo, a estratégia definida deve ser considerada uma hipótese inicial, sujeita a ajustes após a execução dos testes de recuperação e análise dos resultados obtidos.

As evidências produzidas durante os testes servirão como base para refinamentos futuros.

---

# Implementação do Pipeline

## Visão Geral

A implementação do pipeline RAG foi organizada em três scripts principais: ingestão, busca e montagem de prompt.

Essa separação permite isolar as responsabilidades do fluxo e facilitar a validação individual de cada etapa.

O pipeline foi implementado em Python utilizando ChromaDB como banco vetorial local e sentence-transformers para geração dos embeddings.

---

## Estrutura da Implementação

```text
pipeline-rag/
├── docs/
├── src/
│   ├── ingest.py
│   ├── search.py
│   └── prompt_builder.py
├── chroma_db/
├── requirements.txt
└── README.md
```
---

# Estratégia de Busca

## Objetivo

A etapa de busca tem como objetivo localizar os chunks mais relevantes para responder às perguntas realizadas pelos usuários.

Após a ingestão e indexação dos documentos, a busca representa o mecanismo responsável por conectar a consulta do usuário ao conhecimento armazenado na base vetorial.

O sucesso do pipeline depende diretamente da qualidade dessa recuperação.

---

## Funcionamento da Busca

Quando uma pergunta é recebida, o pipeline executa as seguintes etapas:

1. Recebimento da pergunta.
2. Conversão da pergunta em embedding.
3. Consulta ao ChromaDB.
4. Cálculo de similaridade vetorial.
5. Ordenação dos resultados.
6. Retorno dos Top-K chunks mais relevantes.

Essa abordagem permite recuperar documentos semanticamente relacionados mesmo quando não existe correspondência literal entre as palavras da consulta e os documentos indexados.

---

## Configuração Utilizada

### Modelo de Embeddings

```text
all-MiniLM-L6-v2
```

### Banco Vetorial

```text
ChromaDB
```

### Collection Utilizada

```text
novatech_docs
```

### Quantidade de Resultados Recuperados (Top-K)

```text
3
```

---

## Critérios de Avaliação

Durante os testes foram avaliados:

- Relevância dos documentos recuperados.
- Ordem dos resultados.
- Similaridade calculada.
- Correspondência com o gabarito esperado.
- Capacidade de recuperação de documentos normativos.

---

## Considerações

A busca semântica demonstrou capacidade de localizar documentos relacionados às perguntas realizadas.

Entretanto, os testes também evidenciaram limitações relacionadas à ordenação dos resultados e ao tratamento de diferentes níveis de autoridade documental.

---

# Montagem do Prompt

## Objetivo

A etapa de montagem do prompt tem como finalidade estruturar o contexto que será enviado ao modelo de linguagem.

Essa etapa combina a pergunta realizada pelo usuário com os documentos recuperados durante a busca semântica.

---

## Componentes do Prompt

### System Prompt

Contém identidade, regras de comportamento, guardrails e instruções gerais do assistente.

### Chunks Recuperados

Contém os documentos retornados pela busca semântica.

### Pergunta do Usuário

Representa a solicitação que deverá ser respondida pelo assistente.

---

## Fluxo de Montagem

```text
System Prompt
        +
Chunks Recuperados
        +
Pergunta do Usuário
        ↓
Prompt Final
        ↓
Modelo de Linguagem
        ↓
Resposta
```

---

## Benefícios

A utilização dessa estrutura permite:

- Redução de alucinações.
- Maior rastreabilidade.
- Fundamentação documental das respostas.
- Melhor aproveitamento do contexto recuperado.

---

## Considerações

Embora a prova de conceito utilize o Claude manualmente para validação das respostas, a estrutura proposta é compatível com integrações futuras baseadas em APIs de modelos de linguagem.

---

# Testes Realizados

Também foi realizado um teste ponta a ponta utilizando o prompt gerado pelo pipeline e executado manualmente no Claude.

O resultado demonstrou que o pipeline é funcional e capaz de produzir respostas fundamentadas no contexto recuperado.

O teste também permitiu identificar limitações relacionadas à precisão da recuperação semântica, reforçando a importância de mecanismos complementares como re-ranking, autoridade documental e controle de versões.

## Teste 01

### Pergunta

Qual o prazo de devolução para carga perigosa?

### Resultado Esperado

Recuperação prioritária da Política de Devolução POL-001 contendo a regra referente às cargas perigosas.

### Resultado Obtido

Top 1:
FAQ-atendimento.md

Top 2:
POL-001-politica-devolucao.md

Top 3:
PROC-042-frete-especial-v1.md

### Avaliação

Parcialmente correto.

O documento correto foi recuperado, porém não apareceu na primeira posição do ranking.

---

## Teste 02

### Pergunta

Meu cliente é Gold, qual o SLA de resolução?

### Resultado Esperado

Recuperação prioritária do documento SLA-2024.

### Resultado Obtido

Top 1:
FAQ-atendimento.md

Top 2:
SLA-2024-tabela-sla-clientes.md

Top 3:
FAQ-atendimento.md

### Avaliação

Parcialmente correto.

A informação correta foi recuperada, porém novamente o FAQ foi priorizado em relação ao documento oficial.

---

## Teste 03

### Pergunta

Quanto custa o frete para 600kg para Manaus?

### Resultado Esperado

Recuperação prioritária do procedimento PROC-042-v2.

### Resultado Obtido

Top 1:
PROC-042-frete-especial-v1.md

Top 2:
PROC-042-v2-frete-especial-revisado.md

Top 3:
PROC-042-v2-frete-especial-revisado.md

### Avaliação

Parcialmente correto.

Os documentos relevantes foram recuperados, porém a versão antiga foi classificada acima da versão revisada.

---

## Resultado Geral

O pipeline demonstrou capacidade de recuperar documentos semanticamente relacionados às consultas realizadas.

Todos os testes retornaram documentos relevantes, comprovando o funcionamento da ingestão, vetorização e recuperação semântica.

Entretanto, foram observadas limitações relacionadas à ordenação dos resultados.

---

# Problemas Encontrados

## Problema 01 - FAQ Superando Documentos Oficiais

Durante os testes foi observado que conteúdos provenientes do FAQ foram classificados acima de documentos normativos oficiais.

Esse comportamento ocorreu nos testes relacionados à devolução e SLA.

### Impactos

- Redução da autoridade documental das respostas.
- Maior risco de utilização de conteúdos informais.
- Menor confiabilidade da recuperação.

---

## Problema 02 - Ausência de Controle de Versão

Os documentos PROC-042-v1 e PROC-042-v2 coexistem na mesma base vetorial.

Como não existem metadados de vigência, o mecanismo de recuperação não consegue determinar automaticamente qual documento representa a versão válida.

### Impactos

- Possibilidade de recuperação de regras conflitantes.
- Risco de utilização de procedimentos desatualizados.
- Dificuldade de governança documental.

---

# Melhorias Propostas

## Melhoria 01 - Autoridade Documental

Adicionar metadados de autoridade documental durante a ingestão.

Exemplo:

```text
POLÍTICA > PROCEDIMENTO > SLA > FAQ
```

Esses metadados poderiam ser utilizados durante a ordenação dos resultados.

---

## Melhoria 02 - Controle de Vigência

Adicionar metadados relacionados à versão e vigência dos documentos.

Exemplo:

```text
versao=2
vigente=true
```

Essa abordagem permitiria priorizar automaticamente documentos atualizados.

---

## Melhoria 03 - Re-Ranking

Implementar uma etapa de re-ranking após a recuperação inicial.

Essa camada permitiria refinar a ordenação dos resultados e aumentar a precisão do pipeline.

---

# Conclusão

A implementação do pipeline RAG demonstrou a viabilidade técnica da utilização de busca semântica para suporte às operações da NovaTech.

A arquitetura proposta validou os principais componentes envolvidos em soluções RAG, incluindo ingestão documental, chunking, geração de embeddings, indexação vetorial, recuperação semântica e montagem de contexto.

Embora construída como prova de conceito, a solução apresenta potencial para evolução em direção a um ambiente corporativo escalável, governado e aderente aos objetivos de negócio da organização.