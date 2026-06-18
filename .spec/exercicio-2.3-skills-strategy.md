# Exercício 2.3 — Definição de Estratégia de Skills

**Nome:** Leonardo Santana  
**Papel/Cargo:** Desenvolvedor  
**Data:** 2026-06-18  

--- 

# Análise Inicial (Humana)

## Entendimento do Problema

O objetivo deste exercício é definir uma estratégia de Skills para o projeto NovaTech Assistant, estabelecendo como o conhecimento técnico e as convenções do projeto serão reutilizados pelos agentes de IA durante o desenvolvimento.

As Skills devem permitir geração consistente de código, documentação, testes e artefatos SDD, reduzindo variabilidade entre agentes e aumentando aderência aos padrões arquiteturais do projeto.

## Premissas Identificadas

- O projeto utiliza Spec Driven Development (SDD).
- O projeto possui agentes apoiando múltiplos papéis.
- O repositório possui organização formal para Skills.
- As Skills devem seguir a hierarquia Foundation → Domain → Artifact.
- O código será desenvolvido em TypeScript utilizando Azure Functions, React, Vitest, Zod e Pino.

## Hipóteses Técnicas

- Grande parte do trabalho futuro será repetitivo.
- Skills bem definidas reduzirão retrabalho e inconsistências.
- Skills Foundation serão reutilizadas por praticamente todos os artefatos.
- Skills Domain encapsularão padrões arquiteturais específicos do projeto.
- Skills Artifact serão especializadas na geração de entregáveis concretos.

## Artefatos Repetitivos Identificados

- Endpoints Azure Functions
- Integrações com Azure AI Search
- Testes de integração
- Componentes React
- ADRs
- Specs SDD
- Documentação técnica

## Estratégia Inicial

A estratégia proposta será organizar as Skills em três níveis hierárquicos, garantindo reutilização progressiva do conhecimento do projeto.

Foundation fornecerá padrões globais.

Domain fornecerá padrões específicos de camada.

Artifact fornecerá receitas completas de geração.

## Conclusão Inicial

A qualidade dos artefatos produzidos pelos agentes dependerá diretamente da qualidade das Skills disponibilizadas. Portanto, o foco principal deve ser construir uma árvore de Skills pequena, reutilizável e alinhada aos padrões técnicos definidos para o NovaTech Assistant.

---

# Solução Inicial (Claude)

## Critérios para Existência de uma Skill

Uma Skill somente deve existir quando atender pelo menos um dos seguintes critérios:

1. Recorrência significativa no projeto.
2. Alto risco de divergência entre implementações.
3. Alta criticidade para o funcionamento do sistema.
4. Complexidade suficiente para justificar orientação explícita.

---

# Estratégia de Organização das Skills

## Foundation Skills

Responsáveis por estabelecer padrões transversais utilizados por todos os módulos do projeto.

### F-01 — typescript-conventions.md

| Campo | Valor |
|---------|---------|
| Categoria | Foundation |
| Objetivo | Padronizar o desenvolvimento TypeScript |
| Frase de Ativação | "Crie uma classe", "Implemente um Service", "Adicione uma Azure Function" |
| Quem Cria | Tech Lead |
| Quem Consome | Desenvolvedores e Agentes IA |
| Frequência | Muito Alta |
| Dependências | Nenhuma |

#### Justificativa

Esta Skill estabelece os padrões fundamentais de tipagem, validação, organização de código e compatibilidade com TypeScript em modo strict.

Representa a base da árvore de dependências utilizada por todas as demais Skills do projeto.

---

### F-02 — error-handling.md

| Campo | Valor |
|---------|---------|
| Categoria | Foundation |
| Objetivo | Padronizar tratamento de erros e observabilidade |
| Frase de Ativação | "Trate erros", "Adicione logging", "Implemente um try/catch" |
| Quem Cria | Tech Lead |
| Quem Consome | Desenvolvedores e Agentes IA |
| Frequência | Muito Alta |
| Dependências | F-01 |

#### Justificativa

Esta Skill garante consistência no tratamento de erros, rastreabilidade de falhas e observabilidade da aplicação através do uso de Pino e erros tipados.

---

### F-03 — project-structure.md

| Campo | Valor |
|---------|---------|
| Categoria | Foundation |
| Objetivo | Padronizar organização do repositório |
| Frase de Ativação | "Onde criar este arquivo?", "Crie um novo módulo", "Adicione um Service" |
| Quem Cria | Tech Lead |
| Quem Consome | Desenvolvedores e Agentes IA |
| Frequência | Alta |
| Dependências | Nenhuma |

#### Justificativa

Esta Skill define a organização lógica do projeto, reduzindo acoplamento e evitando posicionamento incorreto de arquivos e responsabilidades.

---

## Domain Skills

### D-01 — azure-functions-endpoint.md

| Campo | Valor |
|---------|---------|
| Categoria | Domain |
| Objetivo | Padronizar a implementação de endpoints Azure Functions v4 utilizando TypeScript, Zod e arquitetura baseada em Services |
| Frase de Ativação | "Crie um endpoint", "Implemente uma Azure Function", "Adicione uma rota HTTP" |
| Quem Cria | Tech Lead / Desenvolvedor Sênior |
| Quem Consome | Desenvolvedores e Agentes IA |
| Frequência | Alta |
| Dependências | F-01, F-02 |

#### Justificativa

Esta Skill garante consistência entre todos os endpoints do projeto, padronizando validação de entrada, tratamento de erros, construção de respostas HTTP e separação entre handlers e services.

Também estabelece o uso de Zod para validação de contratos externos e reduz o risco de implementação incorreta da versão v4 do Azure Functions.

---

### D-02 — azure-ai-search-integration.md

| Campo | Valor |
|---------|---------|
| Categoria | Domain |
| Objetivo | Padronizar integrações com Azure AI Search |
| Frase de Ativação | "Recupere documentos", "Busque chunks", "Consulte o índice vetorial" |
| Quem Cria | Tech Lead / Desenvolvedor Sênior |
| Quem Consome | Desenvolvedores e Agentes IA |
| Frequência | Média |
| Dependências | F-01, F-02 |

#### Justificativa

Esta Skill define padrões para criação de consultas, recuperação de chunks, tratamento de paginação, filtros e respostas provenientes do Azure AI Search.

Seu objetivo é evitar múltiplas estratégias de acesso ao índice e garantir consistência no fluxo RAG.

---

### D-03 — testing-patterns.md

| Campo | Valor |
|---------|---------|
| Categoria | Domain |
| Objetivo | Padronizar testes unitários, integração e mocks utilizando Vitest |
| Frase de Ativação | "Crie um teste", "Implemente cobertura", "Adicione mocks" |
| Quem Cria | Tech Lead / Desenvolvedor Sênior |
| Quem Consome | Desenvolvedores e Agentes IA |
| Frequência | Alta |
| Dependências | F-01, F-02, D-01 |

#### Justificativa

Esta Skill define padrões de testes para garantir qualidade, previsibilidade e manutenção do código.

Inclui convenções para testes unitários, integração, mocks, fixtures e cobertura dos principais componentes da aplicação.

---

### D-04 — prompt-builder-patterns.md

| Campo | Valor |
|---------|---------|
| Categoria | Domain |
| Objetivo | Padronizar construção de prompts utilizados pelo sistema RAG |
| Frase de Ativação | "Monte um prompt", "Construa contexto", "Adicione grounding" |
| Quem Cria | Tech Lead / Especialista IA |
| Quem Consome | Desenvolvedores e Agentes IA |
| Frequência | Média |
| Dependências | F-01, F-02 |

#### Justificativa

Esta Skill estabelece padrões para montagem de prompts, controle de contexto, utilização de chunks recuperados e grounding das respostas.

Seu objetivo é reduzir alucinações e aumentar a qualidade das respostas geradas pelos modelos.

---

## Artifact Skills

### A-01 — create-rag-endpoint.md

| Campo | Valor |
|---------|---------|
| Categoria | Artifact |
| Objetivo | Fornecer uma receita completa para implementação de um endpoint RAG |
| Frase de Ativação | "Implemente o endpoint de consulta", "Crie um fluxo RAG" |
| Quem Cria | Desenvolvedor Sênior |
| Quem Consome | Desenvolvedores e Agentes IA |
| Frequência | Baixa |
| Dependências | D-01, D-02, D-04 |

#### Justificativa

Esta Skill descreve o fluxo completo de recuperação, construção de contexto, chamada ao modelo e retorno da resposta.

Apesar da baixa frequência de criação, possui altíssima criticidade por representar o principal fluxo de negócio do sistema.

---

### A-02 — create-integration-test.md

| Campo | Valor |
|---------|---------|
| Categoria | Artifact |
| Objetivo | Fornecer uma receita padronizada para criação de testes de integração |
| Frase de Ativação | "Crie um teste de integração", "Valide um endpoint" |
| Quem Cria | Desenvolvedor Sênior |
| Quem Consome | Desenvolvedores e Agentes IA |
| Frequência | Alta |
| Dependências | D-01, D-03 |

#### Justificativa

Esta Skill reduz a variabilidade entre implementações de testes de integração e garante que os principais fluxos do sistema sejam validados de forma consistente.

---

### A-03 — create-teams-adaptive-card.md

| Campo | Valor |
|---------|---------|
| Categoria | Artifact |
| Objetivo | Fornecer uma receita completa para criação de Adaptive Cards para Microsoft Teams |
| Frase de Ativação | "Crie um Adaptive Card", "Monte um card de resposta" |
| Quem Cria | Desenvolvedor Sênior |
| Quem Consome | Desenvolvedores e Agentes IA |
| Frequência | Média |
| Dependências | F-01, F-02 |

#### Justificativa

Esta Skill padroniza a criação de cards utilizados pelo Teams Bot, garantindo consistência visual, compatibilidade com o schema oficial do Adaptive Card e reutilização dos modelos de resposta do projeto.

---

# Mapa de Dependências

```text
Foundation
├── F-01 typescript-conventions
├── F-02 error-handling
└── F-03 project-structure

Domain
├── D-01 azure-functions-endpoint
├── D-02 azure-ai-search-integration
├── D-03 testing-patterns
└── D-04 prompt-builder-patterns

Artifact
├── A-01 create-rag-endpoint
├── A-02 create-integration-test
└── A-03 create-teams-adaptive-card
```

---

# Matriz Consolidada de Skills

| ID | Skill | Categoria | Frequência | Criticidade |
|----|---------|-----------|-----------|-----------|
| F-01 | typescript-conventions | Foundation | Muito Alta | Muito Alta |
| F-02 | error-handling | Foundation | Muito Alta | Muito Alta |
| F-03 | project-structure | Foundation | Alta | Alta |
| D-01 | azure-functions-endpoint | Domain | Alta | Muito Alta |
| D-02 | azure-ai-search-integration | Domain | Média | Muito Alta |
| D-03 | testing-patterns | Domain | Alta | Alta |
| D-04 | prompt-builder-patterns | Domain | Média | Muito Alta |
| A-01 | create-rag-endpoint | Artifact | Baixa | Altíssima |
| A-02 | create-integration-test | Artifact | Alta | Alta |
| A-03 | create-teams-adaptive-card | Artifact | Média | Média |

---

# Skills Mais Críticas

## 1. F-01 — typescript-conventions.md

Representa a raiz da árvore de dependências.

Todas as demais Skills dependem direta ou indiretamente desta Skill.

Define padrões fundamentais de tipagem, validação, organização de código e compatibilidade com TypeScript em modo strict.

---

## 2. F-02 — error-handling.md

Responsável por padronizar tratamento de erros, observabilidade e rastreabilidade.

Evita falhas silenciosas e reduz o tempo de diagnóstico de incidentes.

---

## 3. A-01 — create-rag-endpoint.md

Implementa o principal fluxo de negócio do sistema.

Integra Azure Functions, Azure AI Search, Prompt Builder e geração de respostas.

Um erro nesta Skill compromete diretamente a funcionalidade principal do produto.

---

## 4. D-01 — azure-functions-endpoint.md

Padroniza a camada de entrada da aplicação.

Garante consistência na validação, tratamento de requisições e construção de respostas HTTP.

---

## 5. D-04 — prompt-builder-patterns.md

Responsável por garantir grounding, controle de contexto e qualidade das respostas geradas.

Erros nesta camada impactam diretamente a precisão do sistema RAG.

---

# Skill Foundation Principal Escolhida

## typescript-conventions.md

### Justificativa

A Skill `typescript-conventions.md` foi escolhida como a Skill Foundation mais importante do projeto por representar a raiz da hierarquia de dependências.

Todas as demais Skills dependem direta ou indiretamente dela.

Sua aplicação é transversal a todos os módulos do sistema:

- Azure Functions
- Services
- Pipeline
- React
- Bot Teams
- Testes

Além disso, estabelece padrões fundamentais para:

- Type Safety
- Strict Mode
- Validação com Zod
- Logging com Pino
- Organização de código
- Contratos entre módulos

Por esses motivos, sua correta utilização influencia diretamente a qualidade dos artefatos produzidos pelos agentes de IA e pelos desenvolvedores.

---

# Referência ao SKILL.md

O detalhamento completo da Skill Foundation principal encontra-se no arquivo:

```text
.spec/evidencias/exercicio-2.3/04-skill-typescript-conventions.md
```

Este artefato contém:

- Contexto
- Regras Prescritivas
- Exemplos DO
- Exemplos DON'T
- Anti-patterns
- Dependências
- Notas de Manutenção

---

# Revisão Crítica (Arquiteto Principal)

Durante a revisão da solução inicial foram identificados os seguintes pontos de melhoria:

- A Skill principal deveria ser `typescript-conventions.md` e não `error-handling.md`.
- A árvore de dependências precisava refletir corretamente a hierarquia Foundation → Domain → Artifact.
- Era necessário adicionar cobertura explícita para Prompt Builder.
- A estratégia deveria manter aderência ao cenário definido pelo Anexo C.
- A justificativa das Skills mais críticas precisava ser fortalecida.

Todos os pontos identificados foram corrigidos na versão final.

---

# Autoavaliação Crítica

## Pontos Fortes

- Estrutura aderente ao modelo Foundation → Domain → Artifact.
- Dependências acíclicas.
- Cobertura dos principais componentes técnicos do projeto.
- Forte alinhamento ao papel Desenvolvedor.
- Reutilização adequada de conhecimento entre Skills.
- Skill Foundation principal claramente identificada.

---

## Fragilidades Identificadas

- Ainda não existe uma Skill específica para o fluxo completo de Spec Driven Development.
- O módulo Teams Bot possui menor profundidade de cobertura em comparação aos módulos backend.
- As Skills precisarão ser revisadas conforme a evolução do projeto.

---

# Melhorias Futuras

### F-04 — sdd-workflow.md

Skill dedicada ao fluxo completo de Requirements → Plan → Tasks.

---

### D-05 — teams-bot-patterns.md

Skill especializada em ActivityHandler, Adaptive Cards e tratamento de eventos do Teams.

---

## skills/README.md

Criação de um índice centralizado contendo:

- Objetivo das Skills
- Dependências
- Responsáveis
- Histórico de revisão

---

## Processo de Governança

Definir revisões periódicas das Skills para garantir aderência às práticas mais recentes do projeto.

---

# Conclusão

A estratégia proposta estabelece uma estrutura consistente de Skills para o projeto NovaTech Assistant, permitindo reutilização de conhecimento, padronização técnica e redução de variabilidade entre agentes de IA.

A organização em Foundation, Domain e Artifact cria uma hierarquia clara de responsabilidades e dependências, enquanto a escolha da Skill `typescript-conventions.md` como principal garante uma base sólida para todas as implementações futuras.

A solução atende aos requisitos do exercício ao definir uma árvore de Skills coerente, justificar sua existência, identificar as Skills mais críticas e detalhar a Skill Foundation principal utilizada pelo projeto.