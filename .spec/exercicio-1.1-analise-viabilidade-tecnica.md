# Exercício 1.1 — Análise de Viabilidade Técnica com Fundamentos de LLM e Engenharia de Contexto

**Nome:** Leonardo Santana
**Papel/Cargo:** Desenvolvedor
**Data:** 2026-06-01

--- 

# Análise Inicial (Humana)

## Visão Geral

Com base nas informações fornecidas pela NovaTech, a construção de um assistente de IA fundamentado em documentação corporativa é tecnicamente viável utilizando uma arquitetura baseada em Retrieval-Augmented Generation (RAG).

A abordagem RAG é mais adequada do que o treinamento ou fine-tuning de um modelo dedicado, pois a documentação da empresa sofre atualizações frequentes, possui múltiplas fontes de origem e contém informações operacionais que precisam permanecer sincronizadas com as versões mais recentes dos documentos corporativos.

Entretanto, a viabilidade do projeto não depende apenas da escolha do modelo de linguagem (LLM), mas principalmente da qualidade do pipeline de ingestão, indexação, recuperação e gerenciamento de contexto. Em sistemas corporativos de consulta documental, a maior parte dos problemas de qualidade não está relacionada à capacidade do modelo responder perguntas, mas sim à capacidade do sistema recuperar os documentos corretos e disponibilizar contexto suficiente para que o modelo produza respostas confiáveis.

A documentação da NovaTech apresenta características que aumentam significativamente a complexidade técnica da solução:

- Aproximadamente 800 documentos PDF contendo tabelas complexas e fluxogramas.
- Aproximadamente 400 páginas de wiki interligadas por referências internas.
- Aproximadamente 50 planilhas contendo fórmulas e dependências entre células.
- Existência conhecida de documentos contraditórios e múltiplas versões do mesmo procedimento.
- Parte dos documentos em formato escaneado, exigindo OCR antes da indexação.

Essas características introduzem desafios importantes relacionados à extração de conteúdo, preservação de contexto semântico, qualidade dos embeddings e recuperação precisa da informação.

---

## Viabilidade Técnica

Do ponto de vista tecnológico, não existem impedimentos para implementação da solução utilizando uma arquitetura moderna baseada em:

- Pipeline de ingestão documental.
- Extração e normalização de conteúdo.
- Geração de embeddings.
- Banco vetorial para recuperação semântica.
- LLM para geração das respostas.
- Camada de governança e observabilidade.

O ecossistema Microsoft já disponível na NovaTech também reduz riscos de integração, uma vez que o SharePoint, Teams e Azure AI Services possuem mecanismos nativos que podem ser utilizados durante a implementação.

A principal incerteza técnica não está na geração das respostas pelo modelo, mas sim na qualidade dos dados recuperados para compor o contexto de cada consulta.

---

## Principais Hipóteses Técnicas

Para esta análise inicial, estão sendo consideradas as seguintes hipóteses:

1. Os documentos do SharePoint podem ser extraídos de forma automatizada.
2. Os documentos escaneados possuem qualidade suficiente para OCR.
3. Os documentos possuem estrutura minimamente consistente para permitir segmentação em chunks.
4. Existe acesso aos metadados necessários para identificar autoria, data de publicação e versão dos documentos.
5. As áreas responsáveis pelos documentos poderão participar do processo de validação de conteúdo.

Caso alguma dessas hipóteses não se confirme durante o discovery, o esforço necessário para implementação poderá aumentar significativamente.

---

## Principais Riscos Técnicos Identificados

Mesmo antes de uma análise aprofundada dos documentos, já é possível identificar alguns riscos relevantes:

### Qualidade da Extração

Informações presentes em tabelas extensas, fluxogramas e documentos escaneados podem ser parcialmente perdidas durante a ingestão, comprometendo a precisão das respostas.

### Contradições Documentais

A existência de versões diferentes do mesmo procedimento pode fazer com que o mecanismo de recuperação forneça informações conflitantes ao modelo, aumentando o risco de respostas inconsistentes.

### Limitações de Contexto

Embora modelos modernos possuam janelas de contexto extensas, a base documental estimada possui milhões de tokens, tornando impossível fornecer todo o conhecimento ao modelo simultaneamente. Isso exige estratégias eficientes de retrieval, ranking e compressão de contexto.

### Lost in the Middle

Em contextos extensos, informações posicionadas no meio do prompt tendem a receber menos atenção do modelo, reduzindo a probabilidade de utilização durante a geração da resposta.

### Evolução da Base de Conhecimento

Como a documentação é atualizada regularmente por diferentes áreas, o pipeline deverá garantir reprocessamento frequente para evitar que respostas sejam geradas com base em conteúdo desatualizado.

---

## Conclusão Inicial

A solução proposta é tecnicamente viável e compatível com o estado atual das tecnologias de IA Generativa e RAG.

Entretanto, o sucesso do projeto dependerá significativamente mais da qualidade da engenharia de contexto, da governança documental e do pipeline de recuperação de informação do que da escolha do modelo de linguagem em si.

Os maiores riscos identificados neste momento estão relacionados à qualidade da documentação, à presença de conteúdo contraditório e à necessidade de gerenciamento eficiente do orçamento de contexto disponível para o modelo.

Esses pontos serão aprofundados nas próximas etapas desta análise.

---

# Análise das Fontes Documentais

## PDFs com Tabelas Complexas

### Desafio Técnico

Os documentos PDF armazenados no SharePoint contêm tabelas complexas utilizadas em cálculos de frete, regras operacionais e parâmetros comerciais. Durante a extração para o pipeline de RAG, existe o risco de perda da estrutura tabular, especialmente em tabelas extensas que se estendem por múltiplas páginas.

A simples conversão do PDF para texto pode romper o relacionamento entre linhas e colunas, eliminando parte do significado original da informação.

### Impacto no RAG

A perda da estrutura tabular pode comprometer diretamente a qualidade dos embeddings gerados e, consequentemente, a recuperação dos chunks corretos.

Em cenários de consulta relacionados a frete, regiões ou regras operacionais, o modelo pode recuperar informações incompletas ou interpretar incorretamente os dados apresentados na tabela.

Além disso, tabelas mal extraídas aumentam significativamente o risco de respostas incorretas mesmo quando o retrieval recupera o documento correto.

### Estratégia de Mitigação

- Utilizar ferramentas de extração estruturada capazes de preservar a semântica das tabelas.
- Aplicar estratégias específicas de chunking para conteúdos tabulares.
- Evitar que linhas de uma mesma tabela sejam divididas entre múltiplos chunks.
- Repetir cabeçalhos em tabelas extensas para preservar contexto.
- Considerar armazenamento estruturado para tabelas críticas relacionadas a cálculos de frete.

---

## PDFs Escaneados

### Desafio Técnico

Parte da documentação encontra-se em formato escaneado, exigindo OCR para conversão em texto pesquisável.

Embora tecnologias modernas de OCR apresentem bons resultados, ainda existe a possibilidade de erros de reconhecimento, principalmente em documentos com baixa qualidade de digitalização, tabelas complexas ou informações numéricas.

### Impacto no RAG

Falhas no OCR propagam erros para todas as etapas posteriores do pipeline.

Números incorretamente reconhecidos podem gerar respostas erradas relacionadas a SLA, valores financeiros, regras de frete e procedimentos operacionais.

Como os embeddings são gerados a partir do texto extraído, erros nesta etapa contaminam diretamente o processo de recuperação.

### Estratégia de Mitigação

- Utilizar mecanismos de OCR com score de confiança.
- Implementar validações automáticas de qualidade após a extração.
- Aplicar revisão humana para documentos considerados críticos.
- Priorizar documentos digitais sempre que versões nativas estiverem disponíveis.
- Monitorar métricas de qualidade da extração durante a ingestão.

---

## Wiki Confluence

### Desafio Técnico

A wiki corporativa apresenta conteúdo altamente interconectado através de links internos, hierarquias de navegação e macros customizadas.

Durante a ingestão existe o risco de perda de contexto caso cada página seja processada isoladamente, desconsiderando relacionamentos com outras páginas da base.

### Impacto no RAG

A quebra das relações entre documentos pode dificultar consultas que dependam da combinação de informações distribuídas em múltiplas páginas.

Além disso, páginas recuperadas fora do contexto correto podem gerar respostas incompletas ou ambíguas.

O problema torna-se mais evidente em perguntas que exigem navegação entre procedimentos, políticas e regras complementares.

### Estratégia de Mitigação

- Preservar metadados de navegação durante a indexação.
- Manter relacionamentos entre páginas e referências cruzadas.
- Armazenar breadcrumbs e hierarquia documental como metadados.
- Utilizar estratégias de retrieval capazes de recuperar documentos relacionados.
- Considerar abordagens de recuperação multi-hop para consultas complexas.

---

## Planilhas com Fórmulas Interdependentes

### Desafio Técnico

As planilhas representam o tipo de conteúdo mais distante do formato textual tradicional utilizado pelos modelos de linguagem.

Grande parte do conhecimento está armazenada através de fórmulas, dependências entre células, múltiplas abas e regras implícitas de cálculo.

A simples conversão desse conteúdo para texto elimina parte significativa da lógica existente na planilha.

### Impacto no RAG

A perda das relações entre células reduz drasticamente a capacidade do sistema responder perguntas baseadas em cálculos, parâmetros ou regras de negócio.

Mesmo que a recuperação encontre o conteúdo correto, o modelo pode não compreender adequadamente as dependências existentes entre os dados.

Isso aumenta o risco de respostas incorretas em consultas relacionadas a frete, SLA e regras comerciais.

### Estratégia de Mitigação

- Tratar planilhas como fontes estruturadas de dados.
- Utilizar processos de ETL para normalização do conteúdo.
- Armazenar dados em estruturas consultáveis, como bancos relacionais.
- Utilizar Function Calling ou consultas estruturadas para informações críticas.
- Evitar depender exclusivamente de embeddings para interpretação de conteúdo tabular complexo.

---

# Estimativa de Volume da Base em Tokens

## Objetivo

Antes de definir a estratégia de recuperação de contexto, é necessário estimar o volume aproximado da base documental da NovaTech.

Essa estimativa permite avaliar a viabilidade do uso de LLMs, dimensionar o pipeline de RAG e compreender as limitações impostas pela janela de contexto dos modelos.

---

## PDFs do SharePoint

### Premissas

- 800 documentos PDF
- Média de 10 páginas por documento
- Média de 500 palavras por página
- Conversão aproximada de 0,75 palavras por token

### Cálculo

```text
800 documentos × 10 páginas × 500 palavras

= 4.000.000 palavras
```

Conversão para tokens:

```text
4.000.000 ÷ 0,75

≈ 5.333.333 tokens
```

### Análise

Os documentos PDF representam a maior parcela da base de conhecimento da NovaTech.

Além do volume textual, é importante considerar que parte desses documentos contém tabelas complexas, imagens, fluxogramas e conteúdo escaneado, fatores que podem aumentar o volume efetivo durante a indexação.

---

## Wiki Confluence

### Premissas

- 400 páginas
- Média de 1.500 palavras por página
- Conversão aproximada de 0,75 palavras por token

### Cálculo

```text
400 páginas × 1.500 palavras

= 600.000 palavras
```

Conversão para tokens:

```text
600.000 ÷ 0,75

≈ 800.000 tokens
```

### Análise

Embora menor que a base de PDFs, a wiki possui forte interdependência entre páginas através de links internos e hierarquias de navegação.

Esse fator aumenta a complexidade do retrieval mesmo sem representar o maior volume de dados.

---

## Planilhas de Referência

### Premissas

- Aproximadamente 50 planilhas
- Conteúdo predominantemente estruturado
- Presença de fórmulas interdependentes

### Cálculo

Não foi realizada uma estimativa direta em tokens para as planilhas, pois seu conteúdo não deve ser tratado exclusivamente como texto durante a ingestão.

### Análise

O principal desafio das planilhas não está relacionado ao volume de tokens, mas à preservação da lógica de negócio presente nas fórmulas e relacionamentos entre células.

Por esse motivo, recomenda-se tratar esse conteúdo como dado estruturado e não apenas como documentos para indexação vetorial.

---

## Volume Total Estimado

### Cálculo Consolidado

| Fonte | Tokens Estimados |
|---------|---------:|
| PDFs | 5.333.333 |
| Wiki Confluence | 800.000 |
| Total Parcial | 6.133.333 |

Considerando:

- Metadados
- OCR
- Serialização de tabelas
- Overlap entre chunks
- Conteúdo auxiliar gerado durante a ingestão

estima-se que a base completa fique entre:

```text
6.000.000 e 8.000.000 tokens
```

---

## Impacto Arquitetural

A estimativa demonstra que a base documental da NovaTech é significativamente maior do que a janela de contexto disponível nos modelos atuais.

Mesmo modelos com janelas extensas, como o GPT-4o (128K tokens), são incapazes de processar simultaneamente todo o conteúdo disponível.

Isso torna inviável qualquer abordagem baseada em inserção direta da documentação completa no prompt.

Consequentemente, a solução depende obrigatoriamente de:

- Chunking eficiente.
- Recuperação semântica (retrieval).
- Relevância contextual.
- Gerenciamento do orçamento de atenção do modelo.
- Estratégias para mitigação do efeito Lost in the Middle.

---

# Análise de Orçamento de Contexto

## Objetivo

Embora a base documental estimada da NovaTech possua entre 6 e 8 milhões de tokens, os modelos de linguagem operam com uma janela de contexto limitada.

Dessa forma, torna-se necessário compreender quanto conteúdo efetivamente pode ser enviado ao modelo durante uma consulta e quais impactos essa limitação gera na arquitetura da solução.

A análise de orçamento de contexto é fundamental para definir estratégias de chunking, retrieval e montagem do prompt, garantindo que o modelo receba apenas as informações mais relevantes para responder cada pergunta.

---

## Premissas

Para esta análise foram consideradas as seguintes premissas:

- GPT-4o com janela de contexto de 128.000 tokens.
- System Prompt e instruções operacionais consumindo aproximadamente 2.000 tokens.
- Chunks documentais com tamanho médio de 500 tokens.
- Espaço adicional necessário para a pergunta do usuário e para a resposta gerada pelo modelo.

---

## Cálculo

### Capacidade disponível para contexto

```text
128.000 tokens
- 2.000 tokens (System Prompt e instruções)

= 126.000 tokens disponíveis
```

### Quantidade teórica de chunks

Considerando chunks de aproximadamente 500 tokens:

```text
126.000 ÷ 500

≈ 252 chunks
```

Do ponto de vista puramente matemático, seria possível inserir aproximadamente 252 chunks em uma única consulta.

---

## Análise

Apesar de 252 chunks caberem teoricamente na janela de contexto do GPT-4o, essa abordagem não é recomendada para ambientes corporativos de produção.

O desempenho dos modelos de linguagem não aumenta proporcionalmente à quantidade de contexto fornecido. À medida que o volume de informação cresce, múltiplos documentos passam a competir pela atenção do modelo durante a geração da resposta.

Esse fenômeno é conhecido como **Attention Dilution**, onde o excesso de contexto reduz a capacidade do modelo identificar quais informações são realmente relevantes para responder a pergunta do usuário.

Outro fator importante é o efeito conhecido como **Lost in the Middle**, observado em modelos de linguagem quando informações posicionadas no meio de contextos muito extensos recebem menos atenção do que informações posicionadas no início ou no final do prompt.

Além disso, a janela de contexto disponível não é utilizada exclusivamente pelos documentos recuperados. Outros elementos também consomem parte significativa do orçamento disponível, como:

- System Prompt.
- Instruções operacionais.
- Histórico da conversa.
- Metadados da consulta.
- Instruções de segurança.
- Citações de fontes.
- Resposta gerada pelo modelo.

Por esse motivo, utilizar o limite máximo teórico da janela de contexto tende a degradar a qualidade das respostas em vez de melhorá-la.

---

## Impacto na Arquitetura

A limitação da janela de contexto influencia diretamente a arquitetura da solução.

Como a base documental da NovaTech possui milhões de tokens, torna-se inviável fornecer todos os documentos ao modelo durante a inferência.

Isso torna obrigatória a utilização de uma arquitetura baseada em Retrieval-Augmented Generation (RAG), onde apenas os documentos mais relevantes para cada pergunta são recuperados e enviados ao modelo.

Nesse cenário, a qualidade da resposta passa a depender fortemente de:

- Qualidade dos embeddings.
- Estratégia de chunking.
- Processo de retrieval.
- Mecanismos de reranking.
- Gestão eficiente do orçamento de atenção do modelo.

---

## Recomendação

Para o cenário da NovaTech, recomenda-se recuperar entre 5 e 15 chunks altamente relevantes por consulta.

Essa abordagem reduz ruído, melhora a precisão das respostas e minimiza os efeitos relacionados à competição por atenção e ao fenômeno Lost in the Middle.

A seleção desses chunks deve ser realizada por mecanismos de retrieval e reranking capazes de priorizar os documentos mais relevantes para cada pergunta realizada pelos atendentes.

---

## Conclusão

A janela de contexto deve ser tratada como um recurso limitado e valioso da arquitetura.

O sucesso da solução não depende da quantidade de documentos enviados ao modelo, mas da capacidade do pipeline de recuperação selecionar os poucos documentos mais relevantes para compor o contexto de cada consulta.

Essa conclusão reforça a importância das estratégias de chunking e retrieval, que serão detalhadas na próxima seção desta análise.

---

# Estratégia Recomendada de Chunking

## Objetivo

A estratégia de chunking tem papel fundamental na qualidade das respostas geradas pelo assistente.

Como a base documental da NovaTech possui milhões de tokens e diferentes tipos de conteúdo (PDFs, tabelas, wiki corporativa e planilhas), a divisão dos documentos não pode ser realizada utilizando apenas tamanhos fixos de texto.

Uma estratégia inadequada de chunking pode fragmentar informações importantes, dificultar a recuperação dos documentos corretos e aumentar a ocorrência de respostas incompletas ou incorretas.

---

## Princípios Adotados

Para este cenário, a estratégia de chunking deve seguir os seguintes princípios:

- Preservar a semântica do conteúdo.
- Evitar fragmentação de procedimentos e regras de negócio.
- Minimizar a perda de contexto entre chunks.
- Facilitar a recuperação dos documentos mais relevantes.
- Reduzir os efeitos do fenômeno Lost in the Middle.
- Otimizar o uso da janela de contexto disponível.

Por esse motivo, não é recomendada uma estratégia baseada exclusivamente em chunks fixos de tamanho arbitrário.

---

## Estratégia para PDFs Procedurais

### Características

Os documentos PDF da NovaTech contêm procedimentos operacionais, regras de negócio, políticas corporativas e manuais de atendimento.

Grande parte das consultas realizadas pelos atendentes estará relacionada a tópicos específicos desses documentos.

### Estratégia Recomendada

Utilizar chunking semântico baseado em seções documentais.

Exemplo:

```text
POL-001
├── Seção 1 - Objetivo
├── Seção 2 - Elegibilidade
├── Seção 3 - Processo de Devolução
└── Seção 4 - Exceções
```

Cada seção deve gerar um ou mais chunks independentes.

### Tamanho Recomendado

- Entre 400 e 600 tokens por chunk.
- Overlap de aproximadamente 10%.

### Benefícios

- Mantém a coerência semântica.
- Melhora a qualidade dos embeddings.
- Facilita a recuperação de regras específicas.
- Reduz fragmentação de procedimentos.

---

## Estratégia para Tabelas Complexas

### Características

As tabelas de frete representam um dos conteúdos mais sensíveis da solução.

Elas contêm relacionamentos entre linhas e colunas que não podem ser perdidos durante a segmentação.

### Estratégia Recomendada

Evitar quebrar tabelas no meio de linhas ou colunas.

Sempre que possível:

- Repetir cabeçalhos em todos os chunks derivados da tabela.
- Manter linhas completas dentro do mesmo chunk.
- Preservar a estrutura tabular durante a ingestão.

Exemplo:

```text
Região | Multiplicador
Sul    | 1.3
Sudeste| 1.1
Norte  | 1.8
```

### Benefícios

- Preserva significado dos dados.
- Reduz risco de recuperação parcial.
- Melhora precisão das respostas relacionadas a frete.

---

## Estratégia para Wiki Confluence

### Características

As páginas da wiki possuem forte relacionamento entre si através de links internos, hierarquias e referências cruzadas.

### Estratégia Recomendada

Utilizar chunking semântico preservando:

- Título da página.
- Hierarquia da navegação.
- Breadcrumbs.
- Referências cruzadas.

Exemplo:

```text
Comercial
└── SLA
    └── Clientes Gold
```

Essas informações devem ser armazenadas como metadados dos chunks.

### Benefícios

- Mantém contexto organizacional.
- Facilita consultas multi-hop.
- Melhora relevância durante o retrieval.

---

## Estratégia para Planilhas

### Características

As planilhas possuem fórmulas interdependentes e lógica de negócio distribuída entre células.

### Estratégia Recomendada

Evitar converter integralmente planilhas em texto para indexação vetorial.

Sempre que possível:

- Tratar dados como conteúdo estruturado.
- Armazenar informações em bancos relacionais.
- Utilizar consultas específicas para recuperação dos dados.

A geração de chunks deve ser utilizada apenas para descrições complementares e documentação auxiliar.

### Benefícios

- Preserva regras de cálculo.
- Evita perda de contexto matemático.
- Reduz alucinações relacionadas a valores.

---

## Relação com o Retrieval

A estratégia de chunking influencia diretamente a qualidade do retrieval.

Chunks excessivamente pequenos tendem a perder contexto semântico.

Chunks excessivamente grandes aumentam o ruído e dificultam a identificação dos documentos mais relevantes.

A combinação recomendada para o cenário da NovaTech é:

- Chunking semântico.
- Chunks entre 400 e 600 tokens.
- Overlap de aproximadamente 10%.
- Retrieval híbrido (vetorial + keyword).
- Reranking antes da montagem do contexto final.

---

## Relação com o Lost in the Middle

Uma boa estratégia de chunking também contribui para reduzir os impactos do fenômeno Lost in the Middle.

Ao recuperar poucos chunks altamente relevantes, o modelo recebe um contexto mais enxuto e focado, reduzindo a competição por atenção entre documentos.

Essa abordagem aumenta a probabilidade de que informações importantes sejam efetivamente utilizadas durante a geração da resposta.

---

## Conclusão

Considerando as características da documentação da NovaTech, recomenda-se uma estratégia de chunking predominantemente semântica, adaptada ao tipo de conteúdo processado.

PDFs, tabelas, wiki corporativa e planilhas apresentam comportamentos distintos e exigem tratamentos específicos durante a ingestão.

A utilização de uma estratégia única para todos os documentos aumentaria significativamente o risco de perda de contexto, degradação do retrieval e redução da qualidade das respostas geradas pelo assistente.

---

# Ajustes Incorporados Após Revisão Técnica

Durante a segunda iteração de análise, foi realizada uma revisão crítica da proposta utilizando IA Generativa com o objetivo de identificar riscos não considerados, premissas excessivamente otimistas e possíveis fragilidades arquiteturais.

A revisão trouxe contribuições relevantes principalmente nos temas relacionados à segurança, governança documental e confiabilidade das respostas geradas pelo assistente.

Embora a análise inicial já contemplasse os principais aspectos relacionados à ingestão documental, recuperação de contexto, chunking e retrieval, alguns pontos adicionais foram considerados importantes para fortalecer a proposta.

## Segurança e Controle de Acesso

A revisão destacou a necessidade de garantir que os documentos recuperados respeitem as permissões já existentes nas fontes corporativas.

Considerando que a solução será integrada ao ecossistema Microsoft da NovaTech, recomenda-se que os mecanismos de recuperação respeitem as permissões existentes no SharePoint e demais fontes documentais, evitando exposição indevida de informações restritas.

A adoção de mecanismos de Security Trimming contribui para aumentar a segurança da solução e reduzir riscos relacionados ao acesso indevido a documentos corporativos.

---

## Governança Documental

Outro ponto relevante identificado durante a revisão foi a necessidade de estabelecer critérios claros para tratamento de documentos contraditórios.

O cenário apresentado informa explicitamente que atualmente algumas divergências são resolvidas através do conhecimento tácito dos colaboradores, o que demonstra ausência de uma fonte única de verdade para determinados processos.

Nesse contexto, recomenda-se a definição de critérios de vigência documental, hierarquia de autoridade e processos de revisão capazes de reduzir inconsistências entre documentos.

---

## Grounding e Confiabilidade das Respostas

A revisão também reforçou a importância de mecanismos que garantam que as respostas geradas estejam fundamentadas em conteúdo efetivamente recuperado das fontes corporativas.

Para isso, recomenda-se que a solução priorize respostas acompanhadas de referências documentais e utilize mecanismos de abstenção quando não houver evidências suficientes para responder uma determinada pergunta.

Essa abordagem reduz o risco de alucinações e aumenta a confiabilidade das informações fornecidas aos atendentes.

---

## Atualização da Base de Conhecimento

Considerando que a documentação da NovaTech sofre atualizações frequentes realizadas por diferentes áreas da organização, recomenda-se a adoção de processos de sincronização incremental entre as fontes documentais e o índice vetorial.

Essa estratégia reduz inconsistências, evita reprocessamentos desnecessários e melhora a eficiência operacional do pipeline de ingestão.

---

## Conclusão

As observações incorporadas nesta etapa complementam a análise inicial sem alterar suas conclusões fundamentais.

Os ajustes realizados fortalecem aspectos relacionados à segurança, governança e confiabilidade da solução, aumentando sua aderência aos requisitos normalmente encontrados em ambientes corporativos de produção.

---

# Conclusão Final

## Avaliação da Viabilidade Técnica

Com base na análise realizada, conclui-se que a construção do assistente de IA para a NovaTech é tecnicamente viável utilizando uma arquitetura baseada em Retrieval-Augmented Generation (RAG).

A combinação entre mecanismos de recuperação de contexto, indexação documental e modelos de linguagem permite atender ao objetivo de disponibilizar respostas fundamentadas na documentação oficial da empresa, reduzindo significativamente o tempo gasto pelos atendentes na busca por informações.

Além disso, a disponibilidade do ecossistema Microsoft já adotado pela organização reduz riscos relacionados à integração e favorece a adoção da solução dentro do ambiente corporativo existente.

---

## Principais Riscos Identificados

Durante a análise foram identificados riscos relevantes que podem impactar a qualidade da solução caso não sejam adequadamente tratados.

Os principais riscos observados foram:

- Perda de estrutura em tabelas complexas durante a ingestão.
- Erros de OCR em documentos escaneados.
- Existência de documentos contraditórios.
- Limitações da janela de contexto dos modelos de linguagem.
- Recuperação inadequada de informações relevantes.
- Atualizações frequentes da base documental.
- Problemas de governança da informação.

Embora esses riscos não inviabilizem a solução, eles exigem atenção durante as fases de discovery, implementação e evolução da arquitetura.

---

## Recomendações

Para maximizar as chances de sucesso do projeto, recomenda-se:

- Utilização de arquitetura baseada em RAG.
- Estratégia de chunking semântico adaptada ao tipo de conteúdo.
- Recuperação híbrida utilizando busca vetorial e busca por palavras-chave.
- Aplicação de mecanismos de reranking antes da montagem do contexto.
- Tratamento estruturado para planilhas e tabelas críticas.
- Governança documental para controle de versões e resolução de conflitos.
- Respostas fundamentadas em fontes recuperadas.
- Sincronização incremental da base documental.
- Respeito às permissões existentes nas fontes corporativas.

---

## Consideração Final

A principal conclusão desta análise é que o sucesso da solução dependerá menos da capacidade do modelo de linguagem utilizado e mais da qualidade da engenharia de contexto, da governança documental e do pipeline de recuperação de informações.

Considerando os desafios identificados e as estratégias propostas ao longo deste documento, recomenda-se prosseguir com a iniciativa, iniciando por uma fase de discovery capaz de validar as hipóteses levantadas, consolidar os mecanismos de governança da informação e definir os critérios de qualidade necessários para suportar a operação em ambiente corporativo.