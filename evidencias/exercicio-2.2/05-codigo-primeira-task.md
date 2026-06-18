# Código da Primeira Task — Exercício 2.2

## Contexto

A primeira task refinada foi `QE-03 — Setup do endpoint com validação de input`.

Esta implementação demonstra:

- Azure Functions v4
- TypeScript strict
- Zod
- Pino
- Tratamento de erros tipado
- Estrutura aderente ao Anexo C

---

# Arquivos Implementados

## 1. `src/functions/query/handler.ts`

```typescript
/**
 * handler.ts — HTTP trigger do query endpoint (Azure Functions v4)
 *
 * FASE ATUAL: QE-03 — scaffold executável com validação real.
 * O fluxo RAG completo (search → prompt-builder → completion) será
 * implementado em QE-07. Por ora, retorna 501 após validação bem-sucedida.
 *
 * Responsabilidades do handler:
 *   - Criar e propagar RequestContext
 *   - Orquestrar chamadas a serviços e builders
 *   - Mapear erros de domínio para status HTTP
 *   - Logging estruturado de entrada e saída
 *
 * O que NÃO pertence aqui:
 *   - Lógica de negócio (.map, .filter, transformações inline)
 *   - Leitura direta do índice de busca
 *   - Montagem de prompt
 */

import { app, type HttpRequest, type HttpResponseInit, type InvocationContext } from '@azure/functions';
import type { RequestContext } from '../../shared/types.js';
import { logger } from '../../shared/logger.js';
import { ValidationError, SearchServiceError, CompletionServiceError } from '../../shared/errors.js';
import { validateQueryRequest } from './validator.js';

// ---------------------------------------------------------------------------
// Handler function
// ---------------------------------------------------------------------------

export async function queryHandler(
  req: HttpRequest,
  _fnCtx: InvocationContext,
): Promise<HttpResponseInit> {
  // Criar contexto de rastreabilidade — propagado como parâmetro para todos
  // os serviços que precisam de logging correlacionado (ver ADR-0004).
  const ctx: RequestContext = {
    requestId: crypto.randomUUID(),
    startedAt: Date.now(),
  };

  // Log de entrada — sem logar `question` (dado PII do atendente)
  logger.info({ requestId: ctx.requestId }, 'query.received');

  try {
    // ── Validação de input ─────────────────────────────────────────────────
    const body: unknown = await req.json().catch(() => null);
    const request = validateQueryRequest(body);

    // Enriquecer contexto com agentId após validação bem-sucedida
    ctx.agentId = request.agentId;

    // ── Fluxo RAG (a implementar em QE-07) ────────────────────────────────
    // TODO QE-07: substituir este bloco pelo fluxo completo:
    //   const systemPrompt = await readSystemPrompt();
    //   const chunks = await searchChunks(request.question, 5, ctx);
    //   const prompt = buildPrompt(systemPrompt, chunks, request.question);
    //   const completion = await getCompletion(prompt, ctx);
    //   const response = buildResponse(completion, chunks);
    //   return ok(response, ctx);
    logger.info({ requestId: ctx.requestId, durationMs: elapsed(ctx) }, 'query.not_implemented');
    return {
      status: 501,
      jsonBody: { error: 'NOT_IMPLEMENTED', message: 'RAG pipeline pendente (QE-07).' },
    };

  } catch (err: unknown) {
    return handleError(err, ctx);
  }
}

// ---------------------------------------------------------------------------
// Helpers privados
// ---------------------------------------------------------------------------

function elapsed(ctx: RequestContext): number {
  return Date.now() - ctx.startedAt;
}

function handleError(err: unknown, ctx: RequestContext): HttpResponseInit {
  if (err instanceof ValidationError) {
    logger.warn(
      { requestId: ctx.requestId, issues: err.issues, durationMs: elapsed(ctx) },
      'query.validation_failed',
    );
    return {
      status: 400,
      jsonBody: { error: err.code, issues: err.issues },
    };
  }

  if (err instanceof SearchServiceError || err instanceof CompletionServiceError) {
    logger.error(
      { requestId: ctx.requestId, errorCode: err.code, cause: err.context['cause'], durationMs: elapsed(ctx) },
      'query.service_error',
    );
    return {
      status: 502,
      jsonBody: { error: err.code },
    };
  }

  // Erro não previsto — loga sem expor detalhes ao chamador
  logger.error(
    { requestId: ctx.requestId, err, durationMs: elapsed(ctx) },
    'query.unexpected_error',
  );
  return {
    status: 500,
    jsonBody: { error: 'INTERNAL_ERROR' },
  };
}

// ---------------------------------------------------------------------------
// Registro Azure Functions v4
// ---------------------------------------------------------------------------

app.http('query', {
  methods: ['POST'],
  authLevel: 'function',
  handler: queryHandler,
});
```

---

## 2. `src/functions/query/validator.ts`

```typescript
/**
 * validator.ts — Validação de input do query endpoint
 *
 * Responsabilidades:
 *   - Definir o schema Zod para QueryRequest
 *   - Exportar função validateQueryRequest como função pura (sem I/O)
 *   - Lançar ValidationError (nunca retornar null/undefined em caso de falha)
 *
 * O que NÃO pertence aqui:
 *   - Logging (responsabilidade do handler)
 *   - Chamadas de rede
 *   - Leitura de arquivo ou variável de ambiente
 */

import { z } from 'zod';
import type { QueryRequest } from '../../shared/types.js';
import { ValidationError } from '../../shared/errors.js';

// ---------------------------------------------------------------------------
// Schema
// ---------------------------------------------------------------------------

export const QueryRequestSchema = z.object({
  question: z
    .string({ required_error: 'O campo question é obrigatório.' })
    .min(1, { message: 'A pergunta não pode ser vazia.' })
    .max(500, { message: 'A pergunta não pode ultrapassar 500 caracteres.' }),

  agentId: z
    .string()
    .uuid({ message: 'agentId deve ser um UUID v4 válido.' })
    .optional(),
});

// ---------------------------------------------------------------------------
// Função de validação
// ---------------------------------------------------------------------------

/**
 * Valida e converte `body` desconhecido em `QueryRequest` tipado.
 *
 * @param body - Corpo da requisição HTTP, tipo desconhecido.
 * @returns QueryRequest validado.
 * @throws {ValidationError} quando a validação falha — inclui todos os issues
 *         do Zod acessíveis via `error.context.issues`.
 *
 * @example
 * // No handler:
 * const request = validateQueryRequest(await context.req.json());
 */
export function validateQueryRequest(body: unknown): QueryRequest {
  const result = QueryRequestSchema.safeParse(body);

  if (!result.success) {
    throw new ValidationError(result.error.issues);
  }

  return result.data;
}
```

---

## 3. `src/shared/errors.ts`

```typescript
/**
 * errors.ts — Hierarquia de erros tipados do NovaTech Assistant
 *
 * Convenção:
 *   - Todo erro carrega `context: Record<string, unknown>` com metadados
 *     suficientes para o logger produzir um evento completo sem o stack trace.
 *   - Nenhuma classe loga diretamente (sem console.log / console.error).
 *     Logging é responsabilidade exclusiva do handler.
 */

import type { ZodIssue } from 'zod';

// ---------------------------------------------------------------------------
// Base
// ---------------------------------------------------------------------------

export abstract class AppError extends Error {
  abstract readonly code: string;
  readonly context: Record<string, unknown>;

  constructor(message: string, context: Record<string, unknown> = {}) {
    super(message);
    this.name = this.constructor.name;
    this.context = context;
    // Mantém stack trace correto no V8
    if (Error.captureStackTrace) {
      Error.captureStackTrace(this, this.constructor);
    }
  }
}

// ---------------------------------------------------------------------------
// Erros de domínio
// ---------------------------------------------------------------------------

export class ValidationError extends AppError {
  readonly code = 'VALIDATION_ERROR' as const;

  constructor(issues: ZodIssue[]) {
    super('Falha na validação do input.', { issues });
  }

  /** Atalho tipado para acessar os issues sem cast. */
  get issues(): ZodIssue[] {
    return this.context['issues'] as ZodIssue[];
  }
}

export class SearchServiceError extends AppError {
  readonly code = 'SEARCH_ERROR' as const;

  constructor(message: string, cause: unknown) {
    super(message, { cause });
  }
}

export class CompletionServiceError extends AppError {
  readonly code = 'COMPLETION_ERROR' as const;

  constructor(message: string, cause: unknown) {
    super(message, { cause });
  }
}

export class ContextBudgetExceededError extends AppError {
  readonly code = 'CONTEXT_BUDGET_EXCEEDED' as const;

  constructor(tokenCount: number, budgetLimit: number) {
    super(
      `Context budget excedido: ${tokenCount} tokens (limite: ${budgetLimit}).`,
      { tokenCount, budgetLimit },
    );
  }

  get tokenCount(): number {
    return this.context['tokenCount'] as number;
  }

  get budgetLimit(): number {
    return this.context['budgetLimit'] as number;
  }
}
```

---

## 4. `src/shared/types.ts`

```typescript
/**
 * types.ts — Contratos de domínio do NovaTech Assistant
 *
 * Regra: nenhuma lógica aqui. Apenas tipos e interfaces.
 *
 * ATENÇÃO: `confidence` em QueryResponse é range [0, 1].
 * A normalização do score bruto do Azure AI Search para esse range
 * é responsabilidade exclusiva de src/functions/query/response-builder.ts.
 * Nunca atribua um score bruto diretamente a este campo.
 *
 * `RequestContext` deve ser criado no handler e passado como parâmetro
 * explícito para funções que precisam de logging. Não use AsyncLocalStorage
 * nesta fase — ver ADR-0004.
 */

// ---------------------------------------------------------------------------
// Request / Response do query endpoint
// ---------------------------------------------------------------------------

/**
 * Payload recebido no POST /api/query.
 * Validado em src/functions/query/validator.ts antes de qualquer uso.
 */
export interface QueryRequest {
  /** Pergunta do atendente. Entre 1 e 500 caracteres. */
  question: string;
  /** Identificador do atendente que originou a consulta. UUID v4. Opcional. */
  agentId?: string;
}

/**
 * Resposta retornada ao chamador após o ciclo completo de RAG.
 */
export interface QueryResponse {
  /** Resposta gerada pelo modelo. */
  answer: string;
  /**
   * Documento de origem do chunk com maior score de relevância.
   * Valor "unknown" quando nenhum chunk foi recuperado.
   */
  source_document: string;
  /**
   * Indicador de confiança normalizado para o range [0, 1].
   *
   * Calculado por response-builder.ts usando score_max / (score_max + 1).
   * NUNCA atribua o score bruto do Azure AI Search diretamente aqui —
   * scores brutos são irrestrito e podem ultrapassar 1.0 em busca semântica.
   *
   * Ausente quando nenhum chunk foi recuperado (chunks array vazio).
   */
  confidence?: number;
}

// ---------------------------------------------------------------------------
// Artefatos internos do pipeline RAG
// ---------------------------------------------------------------------------

/**
 * Chunk recuperado do Azure AI Search.
 * Reflete o esquema do índice definido em infra/modules/ai-search.bicep.
 */
export interface SearchChunk {
  /** Identificador único do chunk no índice. */
  id: string;
  /** Texto do trecho do documento. */
  content: string;
  /** Nome ou caminho do documento de origem (ex: "politica-devolucao-v3.pdf"). */
  source: string;
  /**
   * Score de relevância retornado pelo Azure AI Search.
   * Range irrestrito — varia conforme tipo de busca (BM25, semântica, híbrida).
   * NÃO usar diretamente como `confidence` — normalizar em response-builder.ts.
   */
  score: number;
  /**
   * Período de vigência do documento, quando presente nos metadados.
   * Formato livre (ex: "2024-01-01 a 2024-12-31").
   * Usado pelo prompt-builder para sinalizar documentos com vigência definida.
   */
  vigencia?: string;
}

/**
 * Resultado retornado pelo serviço de completion (Azure OpenAI).
 * Inclui contagem de tokens para auditoria e controle de custo.
 * promptTokens e completionTokens são 0 quando `usage` ausente na resposta.
 */
export interface CompletionResult {
  /** Texto gerado pelo modelo. */
  text: string;
  /** Tokens consumidos pelo prompt (input). 0 se `usage` ausente. */
  promptTokens: number;
  /** Tokens gerados na resposta (output). 0 se `usage` ausente. */
  completionTokens: number;
}

// ---------------------------------------------------------------------------
// Metadados de rastreabilidade
// ---------------------------------------------------------------------------

/**
 * Contexto de rastreabilidade criado no handler e propagado como parâmetro
 * explícito para todas as camadas que precisam de logging correlacionado.
 *
 * Padrão de uso:
 *   const ctx: RequestContext = { requestId: crypto.randomUUID(), startedAt: Date.now() }
 *   await searchChunks(question, 5, ctx)
 *   await getCompletion(prompt, ctx)
 *
 * PROIBIDO: usar variável de módulo ou AsyncLocalStorage para propagar ctx.
 * Motivo: dificulta teste unitário e rastreabilidade em hot-reload.
 * Referência: ADR-0004.
 */
export interface RequestContext {
  /** UUID v4 gerado por requisição para correlação de logs. */
  requestId: string;
  /** Timestamp de entrada da requisição (ms desde epoch). */
  startedAt: number;
  /** Repassado de QueryRequest.agentId quando presente. */
  agentId?: string;
}
```

---

## 5. `src/shared/config.ts`

```typescript
/**
 * config.ts — Configuração de ambiente tipada
 *
 * Todas as variáveis obrigatórias são verificadas em startup.
 * A ausência de qualquer variável obrigatória lança Error imediatamente,
 * antes de qualquer requisição ser processada.
 *
 * NUNCA serializar este objeto em logs — contém chaves de API.
 */

function requireEnv(name: string): string {
  const value = process.env[name];
  if (!value) {
    throw new Error(`Missing env: ${name}`);
  }
  return value;
}

function optionalEnvNumber(name: string, defaultValue: number): number {
  const raw = process.env[name];
  if (raw === undefined || raw === '') return defaultValue;
  const parsed = Number(raw);
  if (Number.isNaN(parsed)) {
    throw new Error(`Invalid numeric env: ${name} = "${raw}"`);
  }
  return parsed;
}

export const config = {
  azureSearchEndpoint:   requireEnv('AZURE_SEARCH_ENDPOINT'),
  azureSearchIndexName:  requireEnv('AZURE_SEARCH_INDEX_NAME'),
  azureSearchApiKey:     requireEnv('AZURE_SEARCH_API_KEY'),
  azureOpenAIEndpoint:   requireEnv('AZURE_OPENAI_ENDPOINT'),
  azureOpenAIDeployment: requireEnv('AZURE_OPENAI_DEPLOYMENT'),
  azureOpenAIApiKey:     requireEnv('AZURE_OPENAI_API_KEY'),
  completionTemperature: optionalEnvNumber('COMPLETION_TEMPERATURE', 0.2),
} as const;

export type Config = typeof config;
```

---

## 6. `src/shared/logger.ts`

```typescript
/**
 * logger.ts — Logger estruturado baseado em Pino
 *
 * Instância única exportada. Não usar console.log no projeto —
 * usar sempre este logger para garantir saída estruturada em JSON.
 */

import pino from 'pino';

export const logger = pino({
  level: process.env['LOG_LEVEL'] ?? 'info',
  // Em desenvolvimento, formata para leitura humana
  ...(process.env['NODE_ENV'] === 'development' && {
    transport: { target: 'pino-pretty' },
  }),
});
```

---

# Observação

Embora a primeira entrega funcional seja o endpoint com validação (`handler.ts` + `validator.ts`), alguns arquivos compartilhados foram incluídos como suporte mínimo para a task:

- `types.ts`
- `errors.ts`
- `config.ts`
- `logger.ts`

Esses arquivos garantem que o código esteja alinhado aos padrões do projeto e possa evoluir para as próximas tasks.