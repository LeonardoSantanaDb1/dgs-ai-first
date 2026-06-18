## Prompt Utilizado

```text
Atue como um Desenvolvedor Sênior especialista em Spec Driven Development (SDD), TypeScript, Azure Functions v4, Azure OpenAI, Azure AI Search, Zod, Pino e Vitest.

Estou participando da certificação AI First da DB1 e atuo no papel de Desenvolvedor.

Preciso resolver o Exercício 2.2 — Implementação de spec com Spec Driven Development.

---

# Contexto

O fluxo do exercício é:

1. O Product Specialist criou o `requirements.md`
2. O Tech Lead converteu em `plan.md`
3. O Desenvolvedor deve:
   - Converter o `plan.md` em `tasks.md`
   - Implementar a primeira task
   - Revisar criticamente o código gerado

---

# Stack Técnica

- TypeScript
- Azure Functions v4
- Azure OpenAI
- Azure AI Search
- Zod
- Pino
- Vitest

---

# Estrutura relevante do repositório

```text
specs/
└── query-endpoint/
    └── tasks.md

src/
├── functions/
│   └── query/
│       ├── handler.ts
│       ├── validator.ts
│       └── response-builder.ts
│
├── services/
│   ├── search.ts
│   ├── completion.ts
│   ├── prompt-builder.ts
│   └── response-validator.ts
│
├── shared/
│   ├── types.ts
│   ├── logger.ts
│   └── errors.ts
│
tests/
├── unit/
├── integration/
└── fixtures/
```

---

# Plan.md recebido

```markdown
# Plan — Query Endpoint

## Approach

Azure Function HTTP trigger que:

1. Recebe pergunta do atendente via POST /api/query
2. Converte pergunta em embedding via Azure OpenAI
3. Busca top-5 chunks no Azure AI Search
4. Monta prompt com chunks + system prompt + pergunta
   (respeitando context budget: ~4K system + ~8K chunks + pergunta)
5. Envia ao GPT-4o e retorna resposta com source_document

## Technical Decisions

- TypeScript com Azure Functions v4
- Zod para validação de input/output
- Retry com exponential backoff para chamadas Azure
- Structured logging com pino

## Prior Decisions (do cenário 1)

- Context budget definido na ADR-0002: ~4K system + ~8K chunks
- Documentos contraditórios tratados com metadado de vigência (ADR-0003)
- System prompt versionado em /prompts/system-prompt.md

## Dependencies

- Azure AI Search index must be populated (pipeline de ingestão)
- System prompt must be finalized (ver /prompts/system-prompt.md)
```

---

# Tarefas obrigatórias

## 1. Converter o plan.md em tasks.md

Produza um `tasks.md` completo.

Para cada task informe obrigatoriamente:

- ID
- Descrição
- Critérios de aceite verificáveis
- Dependências
- Estimativa (P, M ou G)

---

# Regras para as tasks

As tasks devem ser:

- verdadeiramente atômicas
- pequenas o suficiente para implementação isolada
- pequenas o suficiente para teste isolado
- ordenadas por dependência
- aderentes ao fluxo SDD
- rastreáveis ao plan.md

Evite tasks excessivamente grandes.

Evite tasks com múltiplas responsabilidades.

---

## 2. Escolher a primeira task

Após gerar o tasks.md:

Indique qual task deve ser implementada primeiro.

Justifique tecnicamente a escolha.

A justificativa deve considerar:

- dependências
- redução de risco
- valor estrutural
- aderência ao enunciado
- expectativa de um avaliador experiente

---

## 3. Implementar a primeira task

Gere o código TypeScript completo da primeira task.

Importante:

O enunciado da certificação normalmente espera que a primeira entrega represente o:

```text
setup do endpoint com validação de input
```

Portanto avalie criticamente se a primeira task deve incluir:

- handler
- validator
- schema Zod
- request model
- integração Azure Functions

Não escolha uma task excessivamente abstrata.

---

# Requisitos técnicos obrigatórios

O código deve:

- utilizar Azure Functions v4
- utilizar TypeScript strict
- utilizar Zod
- utilizar Pino
- seguir separação de responsabilidades
- evitar any
- ser testável
- ser aderente à estrutura do repositório

---

# 4. Revisão crítica do código

Após implementar a primeira task:

Realize um code review da própria implementação.

A revisão deve conter pelo menos:

- 2 problemas reais
- justificativa técnica
- impacto
- melhoria sugerida

Evite críticas superficiais.

---

# 5. Arquivos criados ou modificados

Liste explicitamente:

- arquivos criados
- arquivos modificados

Utilize caminhos aderentes ao repositório.

Exemplo:

```text
specs/query-endpoint/tasks.md
src/functions/query/handler.ts
src/functions/query/validator.ts
src/shared/types.ts
tests/unit/query-validator.test.ts
```

---

# Autoavaliação

Ao final da solução, faça uma autoavaliação crítica.

Analise:

- atomicidade das tasks
- aderência ao SDD
- aderência ao papel Desenvolvedor
- possíveis riscos de perda de nota
- limitações da implementação inicial

---

# Critérios de qualidade esperados

A solução deve demonstrar:

- entendimento real de Spec Driven Development
- decomposição correta de plan.md em tasks.md
- tasks verdadeiramente atômicas
- critérios de aceite verificáveis
- uso correto de Azure Functions v4
- uso correto de Zod
- uso correto de Pino
- aderência ao papel Desenvolvedor
- implementação concreta da primeira task
- capacidade de revisão crítica

---

# Formato obrigatório da resposta

Organize a resposta exatamente na estrutura abaixo:

# Exercício 2.2 — Implementação de spec com SDD

## Contexto

## Análise do Plan.md

## Tasks.md

## Justificativa da Primeira Task

## Implementação da Primeira Task

## Revisão Crítica do Código

## Arquivos Criados ou Modificados

## Autoavaliação Crítica

---

Produza uma solução com profundidade suficiente para avaliação por um Tech Lead ou Arquiteto Principal da certificação AI First.
```

---

## Resposta Gerada pela IA

```text
## 1. Arquivo: `specs/query-endpoint/tasks.md`

O `plan.md` foi decomposto em 10 tasks atômicas (QE-01 a QE-10), cada uma implementável e testável de forma isolada.

O critério de atomicidade utilizado foi:

> Uma task não deve tocar mais de um arquivo principal de produção.

O mapa de dependências deixa explícito o fluxo de implementação antes da leitura da tabela de tasks.

---

## 2. Primeira Task Escolhida

### QE-01 — Definir tipos TypeScript do domínio

**Arquivo:** `src/shared/types.ts`

### Justificativa

A escolha de tipos como primeira task não é óbvia, porém é a mais aderente ao processo de Spec Driven Development.

#### Por que não começar pelo validator?

- O validator depende dos tipos.
- O search service depende dos tipos.
- O prompt builder depende dos tipos.
- O response builder depende dos tipos.
- O completion service depende dos tipos.

Sem contratos definidos previamente, cada implementação tende a criar estruturas próprias, gerando divergências posteriores.

Em SDD, os contratos representam a fundação da implementação.

### Decisões Técnicas Importantes

#### 1. `source_document: string`

Foi definido como string ao invés de expor diretamente `SearchChunk`.

Motivo:

- Evita acoplamento entre contrato público e estrutura interna do índice.
- Mudanças no Azure AI Search não quebram a API.

---

#### 2. `vigencia?: string`

Mantido como formato livre.

Motivo:

- É um metadado documental.
- O parsing e interpretação pertencem ao prompt-builder.
- O search service não deve assumir semântica de datas.

---

#### 3. `RequestContext`

Criado como tipo separado.

Motivo:

- Centraliza rastreabilidade.
- Evita propagação de parâmetros soltos.
- Facilita correlação de logs.

---

#### 4. Auditoria de Tokens

Incluídos:

```ts
promptTokens
completionTokens
```

Motivo:

- A ADR-0002 define budget de contexto.
- Sem auditoria de tokens não existe controle de custo.

---

## 3. Revisão Crítica do Código

### Ponto 1 — Confidence sem normalização definida

Problema:

```ts
confidence?: number
```

O score do Azure AI Search não possui escala padronizada.

Exemplos:

- BM25
- Busca Semântica
- Busca Híbrida

Podem retornar escalas diferentes.

Consequência:

Consumidores podem assumir incorretamente que:

```ts
confidence ∈ [0,1]
```

quando o valor pode ser:

```txt
3.8
4.2
5.1
```

### Correção

Uma das opções:

- Remover confidence temporariamente.
- Definir normalização explícita.
- Delegar normalização ao response-builder.

---

### Ponto 2 — Propagação de RequestContext indefinida

Problema:

O tipo existe:

```ts
RequestContext
```

Mas o plano não define como ele atravessa as camadas.

Alternativas:

- Parâmetro explícito
- AsyncLocalStorage
- Injeção por fábrica

Sem definição arquitetural existe risco de logs inconsistentes.

### Correção

Adicionar como critério explícito:

```ts
context: RequestContext
```

nas assinaturas de:

- search.ts
- completion.ts

ou registrar decisão arquitetural em ADR.

---

## 4. Arquivos Criados ou Modificados

| Arquivo | Ação | Task |
|----------|--------|--------|
| specs/query-endpoint/tasks.md | Criado | — |
| src/shared/types.ts | Criado | QE-01 |
| src/shared/errors.ts | Criar | QE-02 |
| src/functions/query/validator.ts | Criar | QE-03 |
| src/services/search.ts | Criar | QE-04 |
| src/services/completion.ts | Criar | QE-05 |
| src/services/prompt-builder.ts | Criar | QE-06 |
| src/functions/query/handler.ts | Criar | QE-07 |
| src/functions/query/response-builder.ts | Criar | QE-08 |
| tests/fixtures/chunks.ts | Criar | QE-09 |
| tests/fixtures/queries.ts | Criar | QE-09 |
| tests/unit/query/* | Criar | QE-09 |
| tests/integration/query/handler.test.ts | Criar | QE-10 |

---

# tasks.md

## Mapa de Dependências

```text
QE-01 (types)
    └── QE-02 (errors)
            └── QE-03 (validator)

QE-04 (search)
QE-05 (completion)

      └──────────────┬──────────────┘
                     ↓
               QE-06 (prompt-builder)
                     ↓
               QE-07 (handler)
                 ├── QE-08 (response-builder)
                 └── QE-09 (unit tests)
                          ↓
                     QE-10 (integration test)
```

---

## QE-01 — Definir Tipos TypeScript do Domínio

**Arquivo:** `src/shared/types.ts`

**Tamanho:** P

### Descrição

Declarar todas as interfaces e tipos utilizados pelo endpoint.

### Critérios de Aceite

- QueryRequest possui:
  - question: string
  - agentId?: string

- QueryResponse possui:
  - answer: string
  - source_document: string
  - confidence?: number

- SearchChunk possui:
  - id: string
  - content: string
  - source: string
  - score: number
  - vigencia?: string

- CompletionResult possui:
  - text: string
  - promptTokens: number
  - completionTokens: number

- Compila com:
  
```bash
tsc --strict
```

### Dependências

Nenhuma

### Prioridade

⭐ Primeira Task

---

## QE-02 — Implementar Custom Errors

**Arquivo:** `src/shared/errors.ts`

**Tamanho:** P

### Critérios de Aceite

- AppError base
- ValidationError
- SearchServiceError
- CompletionServiceError
- ContextBudgetExceededError

Dependência:

- QE-01

---

## QE-03 — Implementar Validator com Zod

**Arquivo:** `src/functions/query/validator.ts`

**Tamanho:** P

### Critérios de Aceite

- question obrigatória
- máximo 500 caracteres
- agentId UUID v4
- função pura
- mínimo 4 testes unitários

Dependências:

- QE-01
- QE-02

---

## QE-04 — Search Service

**Arquivo:** `src/services/search.ts`

**Tamanho:** M

### Critérios de Aceite

- Azure AI Search
- Retry:
  - 1s
  - 2s
  - 4s
- Máximo 3 tentativas
- Ordenação por score

Dependências:

- QE-01
- QE-02

---

## QE-05 — Completion Service

**Arquivo:** `src/services/completion.ts`

**Tamanho:** M

### Critérios de Aceite

- Azure OpenAI GPT-4o
- Retry exponencial
- Retorno de tokens
- Temperature configurável

Dependências:

- QE-01
- QE-02

---

## QE-06 — Prompt Builder

**Arquivo:** `src/services/prompt-builder.ts`

**Tamanho:** M

### Critérios de Aceite

- Respeita ADR-0002
- Budget:
  - 4K system
  - 8K chunks
- Prioriza chunks com maior score
- Inclui vigência

Dependências:

- QE-01
- QE-02

---

## QE-07 — Handler HTTP

**Arquivo:** `src/functions/query/handler.ts`

**Tamanho:** M

### Critérios de Aceite

- Azure Functions v4
- POST `/api/query`
- Pino logging
- RequestId
- Mapeamento correto de erros

Dependências:

- QE-03
- QE-04
- QE-05
- QE-06
- QE-08

---

## QE-08 — Response Builder

**Arquivo:** `src/functions/query/response-builder.ts`

**Tamanho:** P

### Critérios de Aceite

- Seleciona chunk com maior score
- Fallback "unknown"
- Função pura

Dependências:

- QE-01

---

## QE-09 — Testes Unitários

**Arquivos:**

- tests/unit/query/
- tests/fixtures/

**Tamanho:** M

### Critérios de Aceite

- Cobertura de branches
- Sem chamadas reais
- Fixtures reutilizáveis

Dependências:

- QE-03
- QE-06
- QE-08

---

## QE-10 — Teste de Integração

**Arquivo:** `tests/integration/query/handler.test.ts`

**Tamanho:** G

### Critérios de Aceite

- Fluxo ponta a ponta
- Mock Azure AI Search
- Mock Azure OpenAI
- Fluxo feliz
- Search vazio
- Retry 429

Dependências:

- QE-07
- QE-09

---

# Código Gerado — `src/shared/types.ts`

```ts
export interface QueryRequest {
  question: string;
  agentId?: string;
}

export interface QueryResponse {
  answer: string;
  source_document: string;
  confidence?: number;
}

export interface SearchChunk {
  id: string;
  content: string;
  source: string;
  score: number;
  vigencia?: string;
}

export interface CompletionResult {
  text: string;
  promptTokens: number;
  completionTokens: number;
}

export interface RequestContext {
  requestId: string;
  startedAt: number;
  agentId?: string;
}
```
```