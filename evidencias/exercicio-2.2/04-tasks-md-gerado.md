# Tasks — Query Endpoint
> **Versão:** 2.0 — refinada pelo Tech Lead após revisão crítica
> **Gerado a partir de:** `specs/query-endpoint/plan.md`
> **Status:** aprovado pelo Tech Lead | pronto para implementação

---

## Decisão arquitetural sobre propagação de contexto

Antes de implementar qualquer task: `RequestContext` é propagado como **parâmetro explícito** em todas as funções que fazem logging. Não usar `AsyncLocalStorage` nesta fase — aumenta complexidade de teste sem ganho real no escopo atual. Registrar como ADR-0004 antes de QE-00.

---

## Mapa de dependências (corrigido)

```
QE-00 (config)
  ├── QE-01 (types)
  │     └── QE-02 (errors)
  │           ├── QE-03 (validator + handler scaffold) ← PRIMEIRA TASK
  │           ├── QE-08 (response-builder)
  │           │     └── QE-04 (search)
  │           │           └── QE-05 (completion)
  │           │                 └── QE-06 (prompt-builder)
  │           │                       └── QE-07 (handler completo)
  │           └── QE-09a (fixtures)
  │                 ├── QE-09b (testes validator)
  │                 ├── QE-09c (testes response-builder)
  │                 ├── QE-09d (testes prompt-builder)
  │                 └── QE-10 (teste integração)
  └── (QE-04 e QE-05 dependem de QE-00 para config)
```

> **Nota de leitura:** QE-08 (response-builder) precede QE-07 (handler completo).
> QE-03 entrega o scaffold executável do handler + o validator — primeira entrega de valor.

---

## Tasks

---

### QE-00 — Definir configuração de ambiente tipada
**Arquivo:** `src/shared/config.ts`
**Tamanho:** P

**Descrição:**
Criar e exportar o objeto `config` com todas as variáveis de ambiente necessárias ao query endpoint. Tipagem estrita — a ausência de variável obrigatória deve falhar em startup, não em runtime.

**Critérios de aceite:**
- [ ] Exporta objeto `config` com os campos: `azureSearchEndpoint: string`, `azureSearchIndexName: string`, `azureSearchApiKey: string`, `azureOpenAIEndpoint: string`, `azureOpenAIDeployment: string`, `azureOpenAIApiKey: string`, `completionTemperature: number` (default `0.2`)
- [ ] Cada campo obrigatório lança `Error` com mensagem `"Missing env: <NOME_VAR>"` se a variável não estiver definida — verificável em teste unitário com `process.env` mockado
- [ ] `completionTemperature` lê de `COMPLETION_TEMPERATURE` e faz parse para `number`; se ausente usa `0.2`
- [ ] Arquivo compila com `tsc --strict` sem erros
- [ ] Nenhum segredo logado — o objeto `config` nunca é serializado para log

**Dependências:** nenhuma

---

### QE-01 — Definir tipos TypeScript do domínio
**Arquivo:** `src/shared/types.ts`
**Tamanho:** P

**Descrição:**
Declarar todas as interfaces e tipos usados pelo query endpoint. Nenhuma lógica — apenas contratos. O campo `confidence` tem range documentado e responsabilidade de normalização explicitamente atribuída.

**Critérios de aceite:**
- [ ] `QueryRequest` tem `question: string` e `agentId?: string`
- [ ] `QueryResponse` tem `answer: string`, `source_document: string`, e `confidence?: number` com JSDoc explicitando range `[0, 1]` e que a normalização é responsabilidade de `response-builder.ts`
- [ ] `SearchChunk` tem `id: string`, `content: string`, `source: string`, `score: number` (range irrestrito — score bruto do Azure AI Search), `vigencia?: string`
- [ ] `CompletionResult` tem `text: string`, `promptTokens: number`, `completionTokens: number`
- [ ] `RequestContext` tem `requestId: string`, `startedAt: number`, `agentId?: string` — com JSDoc indicando que é criado no handler e passado como parâmetro explícito (nunca como global)
- [ ] Arquivo compila com `tsc --strict` sem erros
- [ ] Nenhuma dependência externa

**Dependências:** nenhuma

---

### QE-02 — Implementar custom errors
**Arquivo:** `src/shared/errors.ts`
**Tamanho:** P

**Descrição:**
Hierarquia de erros tipados. Cada erro carrega metadados estruturados suficientes para o logger produzir um evento de log completo sem acesso ao stack trace.

**Critérios de aceite:**
- [ ] `AppError extends Error` exportado com campos `readonly code: string` e `readonly context: Record<string, unknown>`
- [ ] `ValidationError` estende `AppError` com `code = "VALIDATION_ERROR"` e aceita `issues: ZodIssue[]` no construtor; `issues` acessível via `error.context.issues`
- [ ] `SearchServiceError` estende `AppError` com `code = "SEARCH_ERROR"` e aceita `cause: unknown`; `cause` acessível via `error.context.cause`
- [ ] `CompletionServiceError` estende `AppError` com `code = "COMPLETION_ERROR"` e aceita `cause: unknown`
- [ ] `ContextBudgetExceededError` estende `AppError` com `code = "CONTEXT_BUDGET_EXCEEDED"` e aceita `tokenCount: number`, `budgetLimit: number`; ambos acessíveis via `error.context`
- [ ] Nenhuma classe chama `console.log` ou `console.error` — verificável por `grep -n console src/shared/errors.ts` retornar vazio
- [ ] Arquivo compila com `tsc --strict`

**Dependências:** QE-01 (para tipos de `ZodIssue` — importado de `zod`, não de `types.ts`)

> **Nota:** A dependência de QE-01 aqui é indireta — `errors.ts` usa `ZodIssue` de `zod` diretamente. A dependência explícita é que `errors.ts` pode referenciar `RequestContext` em mensagens futuras.

---

### QE-03 — Scaffold executável do handler + validator (PRIMEIRA TASK)
**Arquivos:** `src/functions/query/validator.ts`, `src/functions/query/handler.ts`
**Tamanho:** M
**⭐ PRIMEIRA TASK A IMPLEMENTAR**

**Descrição:**
Entregar o endpoint `POST /api/query` funcionando de ponta a ponta com validação real. O handler ainda não chama Search nem OpenAI — responde com `501 Not Implemented` para o fluxo principal, mas já valida o input, já loga com Pino, já mapeia erros para status HTTP corretos, e já está registrado com a sintaxe correta do Azure Functions v4.

Esta task demonstra: (a) Azure Functions v4 funcionando, (b) Zod integrado, (c) Pino integrado, (d) estrutura de erro → HTTP mapeada. É a entrega de valor mínima verificável por qualquer membro da equipe com um `curl`.

**Critérios de aceite — `validator.ts`:**
- [ ] Exporta `QueryRequestSchema` (schema Zod) e `validateQueryRequest(body: unknown): QueryRequest`
- [ ] `question`: obrigatório, `z.string().min(1).max(500)` — mensagens de erro em português
- [ ] `agentId`: opcional, `z.string().uuid()` quando presente
- [ ] `validateQueryRequest` lança `ValidationError` (de `errors.ts`) quando `schema.safeParse` falha, passando `result.error.issues`
- [ ] Verificável em teste: `validateQueryRequest({})` lança `ValidationError` com `error.context.issues` não vazio
- [ ] Verificável em teste: `validateQueryRequest({ question: '' })` lança com issue `too_small`
- [ ] Verificável em teste: `validateQueryRequest({ question: 'x'.repeat(501) })` lança com issue `too_big`
- [ ] Verificável em teste: `validateQueryRequest({ question: 'ok', agentId: 'nao-uuid' })` lança com issue `invalid_string`
- [ ] Verificável em teste: `validateQueryRequest({ question: 'ok' })` retorna objeto `QueryRequest` válido sem lançar

**Critérios de aceite — `handler.ts`:**
- [ ] Registrado com `app.http('query', { methods: ['POST'], authLevel: 'function', handler: queryHandler })` — sintaxe Azure Functions v4
- [ ] `queryHandler` exportado como named export (não default)
- [ ] Cria `RequestContext` com `requestId: crypto.randomUUID()` e `startedAt: Date.now()` no início de cada requisição
- [ ] Log de entrada via Pino: `logger.info({ requestId, agentId }, 'query.received')` — sem logar `question` (PII)
- [ ] Chama `validateQueryRequest(body)` — em caso de `ValidationError`, retorna `{ status: 400, jsonBody: { error: 'VALIDATION_ERROR', issues: err.context.issues } }`
- [ ] Para o fluxo principal (pós-validação): retorna `{ status: 501, jsonBody: { error: 'NOT_IMPLEMENTED' } }` — placeholder para QE-07
- [ ] Em caso de erro não esperado: retorna `{ status: 500, jsonBody: { error: 'INTERNAL_ERROR' } }` e loga com `logger.error`
- [ ] Log de saída via Pino com `durationMs: Date.now() - ctx.startedAt` e `status` HTTP retornado
- [ ] `curl -X POST http://localhost:7071/api/query -H "Content-Type: application/json" -d '{}'` retorna `400` com body JSON
- [ ] `curl -X POST http://localhost:7071/api/query -H "Content-Type: application/json" -d '{"question":"teste"}'` retorna `501`

**Dependências:** QE-00, QE-01, QE-02

---

### QE-04 — Implementar serviço de busca (Azure AI Search)
**Arquivo:** `src/services/search.ts`
**Tamanho:** M

**Descrição:**
Integração com Azure AI Search. Função pura em relação ao cliente — cliente injetado como parâmetro para permitir mock em teste.

**Critérios de aceite:**
- [ ] Exporta `searchChunks(question: string, topK: number, ctx: RequestContext, client?: SearchClient): Promise<SearchChunk[]>`
- [ ] Quando `client` não fornecido, cria instância usando `config` de QE-00
- [ ] Retry com exponential backoff: tentativa 1 imediata, tentativa 2 após 1s, tentativa 3 após 2s — total máx 3 tentativas
- [ ] Após 3 falhas, lança `SearchServiceError` com `cause` sendo o último erro capturado
- [ ] Resultados retornados ordenados por `score` decrescente — verificável em teste com mock retornando array fora de ordem
- [ ] Log via Pino: `logger.info({ requestId: ctx.requestId, topK, resultCount }, 'search.completed')` — sem logar `content` dos chunks
- [ ] Verificável em teste: spy no `logger` não registra nenhum campo chamado `content` durante a execução
- [ ] Compila com `tsc --strict`

**Dependências:** QE-00, QE-01, QE-02

---

### QE-05 — Implementar serviço de completion (Azure OpenAI)
**Arquivo:** `src/services/completion.ts`
**Tamanho:** M

**Descrição:**
Integração com GPT-4o via Azure OpenAI. Mesma política de retry de QE-04. Cliente injetável para testabilidade.

**Critérios de aceite:**
- [ ] Exporta `getCompletion(prompt: string, ctx: RequestContext, client?: OpenAIClient): Promise<CompletionResult>`
- [ ] Quando `client` não fornecido, cria instância usando `config` de QE-00
- [ ] Retry com mesma política de QE-04 (1s → 2s, máx 3 tentativas)
- [ ] Após 3 falhas, lança `CompletionServiceError` com `cause`
- [ ] `CompletionResult.promptTokens` e `completionTokens` preenchidos de `response.usage.prompt_tokens` e `response.usage.completion_tokens`
- [ ] Temperature lida de `config.completionTemperature`
- [ ] Log via Pino: `logger.info({ requestId: ctx.requestId, promptTokens, completionTokens }, 'completion.done')`
- [ ] Verificável em teste: mock do cliente retorna `usage: null` — função deve retornar `promptTokens: 0, completionTokens: 0` sem lançar
- [ ] Compila com `tsc --strict`

**Dependências:** QE-00, QE-01, QE-02

---

### QE-06 — Implementar prompt-builder com context budget
**Arquivo:** `src/services/prompt-builder.ts`
**Tamanho:** M

**Descrição:**
Função pura que monta o prompt final respeitando o budget da ADR-0002. Recebe o conteúdo do system prompt como parâmetro — leitura do arquivo é responsabilidade exclusiva do handler (QE-07). A função não faz I/O.

**Critérios de aceite:**
- [ ] Exporta `buildPrompt(systemPrompt: string, chunks: SearchChunk[], question: string): string`
- [ ] A função **não lê nenhum arquivo** — recebe `systemPrompt` como `string` já carregada. Verificável por `grep -n "readFile\|fs\." src/services/prompt-builder.ts` retornar vazio
- [ ] Chunks são selecionados por score decrescente até o budget de ~8.000 tokens ser atingido; chunks excedentes são descartados silenciosamente
- [ ] Estimativa de tokens usa heurística `Math.ceil(text.length / 4)` — documentada em comentário inline
- [ ] Lança `ContextBudgetExceededError` com `tokenCount` e `budgetLimit` se a `question` sozinha exceder 500 tokens (~2.000 caracteres)
- [ ] Quando `vigencia` presente no chunk, inclui no bloco: `[Vigência: <valor>]` imediatamente antes do conteúdo do chunk
- [ ] Verificável em teste: `buildPrompt(sys, [], question)` retorna string sem seção de chunks
- [ ] Verificável em teste: `buildPrompt(sys, chunksQueCabem, question)` inclui todos os chunks
- [ ] Verificável em teste: `buildPrompt(sys, chunksQueNaoCabem, question)` inclui apenas os primeiros por score, sem lançar erro
- [ ] Verificável em teste: `buildPrompt(sys, [], 'x'.repeat(2001))` lança `ContextBudgetExceededError`
- [ ] Compila com `tsc --strict`

**Dependências:** QE-01, QE-02

---

### QE-07 — Implementar handler completo (fluxo RAG)
**Arquivo:** `src/functions/query/handler.ts` (evolução de QE-03)
**Tamanho:** M

**Descrição:**
Substituir o `501` de QE-03 pelo fluxo completo: leitura do system prompt → search → prompt-builder → completion → response-builder → resposta. O handler permanece como orquestrador puro — sem lógica de negócio inline.

**Critérios de aceite:**
- [ ] Lê `/prompts/system-prompt.md` uma vez por instância via `fs.promises.readFile` no escopo do módulo (fora do handler function) para evitar I/O por requisição
- [ ] Fluxo: `validateQueryRequest` → `searchChunks` → `buildPrompt` → `getCompletion` → `buildResponse`
- [ ] Retorna `{ status: 400 }` para `ValidationError`, `{ status: 502 }` para `SearchServiceError` e `CompletionServiceError`, `{ status: 500 }` para erros não previstos
- [ ] Propaga `RequestContext` (com `requestId`) para `searchChunks` e `getCompletion` — verificável inspecionando a assinatura das chamadas
- [ ] Log de saída inclui `durationMs`, `promptTokens`, `completionTokens`, `resultCount` (número de chunks usados)
- [ ] Nenhuma transformação de dado inline no handler — toda transformação delega a um serviço ou builder importado. Verificável: nenhuma expressão `.map(`, `.filter(`, `.reduce(` dentro do corpo do `queryHandler`
- [ ] `curl -X POST .../api/query -d '{"question":"qual o prazo de entrega?"}'` retorna `200` com `answer` e `source_document`

**Dependências:** QE-03, QE-04, QE-05, QE-06, QE-08

---

### QE-08 — Implementar response-builder
**Arquivo:** `src/functions/query/response-builder.ts`
**Tamanho:** P

**Descrição:**
Função pura que monta `QueryResponse` a partir de `CompletionResult` e `SearchChunk[]`. Responsável por normalizar `confidence` para o range `[0, 1]` usando min-max sobre os scores retornados.

**Critérios de aceite:**
- [ ] Exporta `buildResponse(completion: CompletionResult, chunks: SearchChunk[]): QueryResponse`
- [ ] `source_document`: campo `source` do chunk com maior `score`; `"unknown"` se `chunks` vazio
- [ ] `confidence`: normalizado para `[0, 1]` usando `score_max / (score_max + 1)` (monotônica, bounded); ausente quando `chunks` vazio
- [ ] Fórmula de normalização documentada em comentário inline com justificativa
- [ ] Função pura — sem I/O, sem side effects. Verificável: `grep -n "readFile\|fetch\|axios\|http" src/functions/query/response-builder.ts` retorna vazio
- [ ] Verificável em teste: `buildResponse(result, [])` retorna `{ source_document: 'unknown' }` sem campo `confidence`
- [ ] Verificável em teste: `buildResponse(result, [chunkScore2, chunkScore5])` retorna `source_document` do chunk com score 5 e `confidence` igual a `5/6 ≈ 0.833`
- [ ] Verificável em teste: empate de score — retorna qualquer um dos empatados de forma determinística (primeiro do array após sort estável)
- [ ] Compila com `tsc --strict`

**Dependências:** QE-01

---

### QE-09a — Fixtures de teste compartilhadas
**Arquivos:** `tests/fixtures/chunks.ts`, `tests/fixtures/queries.ts`, `tests/fixtures/expected-responses.ts`
**Tamanho:** P

**Descrição:**
Criar os dados de teste compartilhados entre todas as suites unitárias. Sem lógica de asserção — apenas dados exportados.

**Critérios de aceite:**
- [ ] `chunks.ts` exporta `mockChunks: SearchChunk[]` com mínimo 6 itens variando: scores distintos (0.3, 0.7, 0.9, 1.5, 2.0, 4.2), com e sem `vigencia`, sources distintos
- [ ] `chunks.ts` exporta `emptyChunks: SearchChunk[]` (array vazio)
- [ ] `chunks.ts` exporta `chunksOverBudget: SearchChunk[]` — 20 chunks com `content` de ~500 chars cada para simular estouro de budget
- [ ] `queries.ts` exporta `validQuery: QueryRequest`, `emptyQuestionQuery`, `longQuestionQuery` (501 chars), `invalidAgentIdQuery`, `queryWithValidAgentId`
- [ ] `expected-responses.ts` exporta `happyPathResponse: QueryResponse` correspondente ao fluxo feliz com `mockChunks`
- [ ] Todos os arquivos compilam com `tsc --strict`
- [ ] Nenhum arquivo de fixture importa de `vitest` — são dados puros

**Dependências:** QE-01

---

### QE-09b — Testes unitários do validator
**Arquivo:** `tests/unit/query/validator.test.ts`
**Tamanho:** P

**Descrição:**
Cobertura unitária completa de `src/functions/query/validator.ts`.

**Critérios de aceite:**
- [ ] Caso: `validateQueryRequest({})` → lança `ValidationError`, `error.context.issues` tem ao menos 1 issue com `path: ['question']`
- [ ] Caso: `question` vazia (`''`) → lança `ValidationError` com issue `too_small`
- [ ] Caso: `question` com 501 chars → lança `ValidationError` com issue `too_big`
- [ ] Caso: `agentId` não-UUID → lança `ValidationError` com issue `invalid_string` em `path: ['agentId']`
- [ ] Caso: `question` válida sem `agentId` → retorna `QueryRequest` sem lançar
- [ ] Caso: `question` válida com UUID válido em `agentId` → retorna objeto completo
- [ ] Nenhum teste faz I/O ou chamada de rede
- [ ] `vitest run tests/unit/query/validator.test.ts` passa sem erros

**Dependências:** QE-03, QE-09a

---

### QE-09c — Testes unitários do response-builder
**Arquivo:** `tests/unit/query/response-builder.test.ts`
**Tamanho:** P

**Descrição:**
Cobertura unitária completa de `src/functions/query/response-builder.ts`.

**Critérios de aceite:**
- [ ] Caso: chunks vazios → `source_document: 'unknown'`, sem campo `confidence`
- [ ] Caso: array com chunks de scores variados → `source_document` é o source do maior score
- [ ] Caso: dois chunks com mesmo score → `source_document` determinístico (primeiro após sort estável)
- [ ] Caso: chunk com score `4.2` → `confidence` ≈ `0.807` (tolerância `±0.001`)
- [ ] Nenhum teste faz I/O
- [ ] `vitest run tests/unit/query/response-builder.test.ts` passa sem erros

**Dependências:** QE-08, QE-09a

---

### QE-09d — Testes unitários do prompt-builder
**Arquivo:** `tests/unit/query/prompt-builder.test.ts`
**Tamanho:** P

**Descrição:**
Cobertura unitária completa de `src/services/prompt-builder.ts`.

**Critérios de aceite:**
- [ ] Caso: chunks dentro do budget → todos aparecem no prompt retornado
- [ ] Caso: chunks que excedem budget → apenas os de maior score aparecem; nenhum erro lançado
- [ ] Caso: chunk com `vigencia` → string `[Vigência: <valor>]` presente no prompt
- [ ] Caso: `question` com 2001 chars → lança `ContextBudgetExceededError` com `tokenCount >= 500`
- [ ] Caso: `chunks` vazio → prompt retornado não contém seção de chunks
- [ ] Nenhum teste faz I/O — `systemPrompt` passado como string literal
- [ ] `vitest run tests/unit/query/prompt-builder.test.ts` passa sem erros

**Dependências:** QE-06, QE-09a

---

### QE-10 — Teste de integração do fluxo completo
**Arquivo:** `tests/integration/query/handler.test.ts`
**Tamanho:** G

**Descrição:**
Teste de integração com `msw` mockando Azure AI Search e Azure OpenAI. Importa o handler diretamente. Sem deploy, sem HTTP real entre processos.

**Critérios de aceite:**
- [ ] `msw` intercepta chamadas ao endpoint do Azure AI Search e retorna `mockChunks` do fixture
- [ ] `msw` intercepta chamadas ao endpoint do Azure OpenAI e retorna resposta controlada com `usage` preenchido
- [ ] Caso: fluxo feliz → status `200`, `answer` não vazio, `source_document` igual ao source do chunk de maior score do fixture
- [ ] Caso: body inválido (sem `question`) → status `400`, body tem campo `error: 'VALIDATION_ERROR'`
- [ ] Caso: search retorna array vazio → status `200`, `source_document: 'unknown'`
- [ ] Caso: Azure OpenAI retorna `429` na primeira chamada, sucesso na segunda → status `200` (retry funcionou)
- [ ] Caso: Azure OpenAI retorna `429` nas 3 tentativas → status `502`
- [ ] `QueryResponse` retornado validado contra `QueryResponseSchema` (Zod) — schema definido em `tests/fixtures/`
- [ ] `vitest run tests/integration/query/` passa sem erros

**Dependências:** QE-07, QE-09a, QE-09b, QE-09c, QE-09d

---

## Resumo e ordem de implementação

| ID | Descrição curta | Tam | Deps | Stack obrigatório |
|----|----------------|-----|------|-------------------|
| QE-00 | Config de ambiente | P | — | TS strict |
| QE-01 | Tipos do domínio | P | — | TS strict |
| QE-02 | Custom errors | P | QE-01 | TS strict, Zod |
| **QE-03** | **Scaffold handler + validator** ⭐ | **M** | **QE-00,01,02** | **Az Fn v4, Zod, Pino** |
| QE-08 | Response-builder | P | QE-01 | TS strict |
| QE-04 | Search service | M | QE-00,01,02 | TS strict, Pino |
| QE-05 | Completion service | M | QE-00,01,02 | TS strict, Pino |
| QE-06 | Prompt-builder | M | QE-01,02 | TS strict |
| QE-07 | Handler completo | M | QE-03,04,05,06,08 | Az Fn v4, Pino |
| QE-09a | Fixtures de teste | P | QE-01 | TS strict |
| QE-09b | Testes validator | P | QE-03,09a | Vitest |
| QE-09c | Testes response-builder | P | QE-08,09a | Vitest |
| QE-09d | Testes prompt-builder | P | QE-06,09a | Vitest |
| QE-10 | Teste integração | G | QE-07,09a–d | Vitest, msw |

**QE-08 pode ser implementado em paralelo com QE-04/QE-05 — sem dependência entre eles.**