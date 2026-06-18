# TypeScript Conventions — NovaTech Assistant

## Objetivo

Esta Skill define os padrões obrigatórios para desenvolvimento TypeScript no projeto NovaTech Assistant.

Seu objetivo é garantir:

- Consistência entre implementações.
- Compatibilidade com `strict: true`.
- Redução de erros em runtime.
- Reutilização de tipos.
- Maior legibilidade e manutenção do código.

Esta Skill deve ser aplicada sempre que forem criados ou modificados arquivos `.ts` ou `.tsx`.

---

## Contexto do Projeto

O NovaTech Assistant utiliza:

- TypeScript
- Azure Functions v4
- React
- Vitest
- Zod
- Pino

Todo código produzido deve seguir os padrões definidos nesta Skill.

---

# Regras Prescritivas

## R-01 — Nunca utilizar `any`

Evitar completamente o uso de:

```typescript
any
```

Utilizar:

```typescript
unknown
```

quando o tipo for desconhecido.

### Correto

```typescript
function process(data: unknown): string {
  if (typeof data === 'string') {
    return data;
  }

  return '';
}
```

### Incorreto

```typescript
function process(data: any): string {
  return data;
}
```

---

## R-02 — Utilizar Tipos Nomeados

Sempre preferir:

```typescript
interface
type
```

ao invés de objetos anônimos.

### Correto

```typescript
interface QueryRequest {
  question: string;
}
```

### Incorreto

```typescript
function execute(data: {
  question: string;
}) {}
```

---

## R-03 — Tipar Retornos Explicitamente

Toda função pública deve possuir retorno explícito.

### Correto

```typescript
function buildPrompt(): string {
  return 'Prompt';
}
```

### Incorreto

```typescript
function buildPrompt() {
  return 'Prompt';
}
```

---

## R-04 — Utilizar Readonly Sempre que Possível

### Correto

```typescript
interface Chunk {
  readonly id: string;
  readonly content: string;
}
```

### Incorreto

```typescript
interface Chunk {
  id: string;
  content: string;
}
```

---

## R-05 — Utilizar Optional Chaining

### Correto

```typescript
const city = customer?.address?.city;
```

### Incorreto

```typescript
const city =
  customer &&
  customer.address &&
  customer.address.city;
```

---

## R-06 — Utilizar Nullish Coalescing

### Correto

```typescript
const limit = request.limit ?? 10;
```

### Incorreto

```typescript
const limit = request.limit || 10;
```

---

## R-07 — Utilizar Zod para Contratos Externos

Toda entrada externa deve ser validada.

### Correto

```typescript
const QuerySchema = z.object({
  question: z.string().min(1)
});

type QueryRequest =
  z.infer<typeof QuerySchema>;
```

### Incorreto

```typescript
const request = await req.json();

const question = request.question;
```

---

## R-08 — Tratar ZodError Explicitamente

### Correto

```typescript
try {
  QuerySchema.parse(body);
}
catch (error) {
  if (error instanceof ZodError) {
    return badRequest(error);
  }
}
```

### Incorreto

```typescript
catch {
  return internalServerError();
}
```

---

## R-09 — Não Utilizar console.log

Todo log deve utilizar Pino.

### Correto

```typescript
logger.info(
  { question },
  'Consulta recebida'
);
```

### Incorreto

```typescript
console.log(question);
```

---

## R-10 — Separar Camadas

### Azure Function

Responsável por:

- Receber requisição.
- Validar entrada.
- Chamar serviço.
- Retornar resposta.

### Service

Responsável por:

- Regras de negócio.
- Integrações.
- Processamento.

Nunca colocar regra de negócio dentro do Handler.

---

## R-11 — Utilizar Imports ESM

### Correto

```typescript
import { logger } from '../shared/logger.js';
```

### Incorreto

```typescript
import { logger } from '../shared/logger';
```

---

# Exemplos DO

## Endpoint Tipado

```typescript
export async function query(
  request: HttpRequest
): Promise<HttpResponseInit> {

  const body =
    await request.json();

  const input =
    QuerySchema.parse(body);

  const result =
    await queryService.execute(input);

  return ok(result);
}
```

---

## Uso de Zod

```typescript
const ChunkSchema = z.object({
  id: z.string(),
  content: z.string()
});

type Chunk =
  z.infer<typeof ChunkSchema>;
```

---

## Uso de Logger

```typescript
logger.info(
  { chunkCount: chunks.length },
  'Chunks recuperados'
);
```

---

# Exemplos DON'T

## Uso de Any

```typescript
const execute = (data: any) => {
  return data;
};
```

---

## Console Log

```typescript
console.log(result);
```

---

## Retorno Sem Tipo

```typescript
function search() {
  return [];
}
```

---

## Ignorar Validação

```typescript
const body =
  await request.json();

service.execute(body);
```

---

# Anti-Patterns

| Anti-Pattern | Problema |
|-------------|-----------|
| Uso de any | Remove segurança de tipos |
| Console.log | Não possui observabilidade estruturada |
| Lógica de negócio no Handler | Aumenta acoplamento |
| Validação manual | Duplica regras |
| Ignorar ZodError | Retornos incorretos |
| Objetos anônimos | Reduz reutilização |
| Retorno implícito | Dificulta manutenção |

---

# Dependências

Esta Skill é a raiz da árvore de Skills.

Não possui dependências.

Skills dependentes:

- error-handling.md
- project-structure.md
- azure-functions-endpoint.md
- azure-ai-search-integration.md
- testing-patterns.md
- prompt-builder-patterns.md
- create-rag-endpoint.md
- create-integration-test.md
- create-teams-adaptive-card.md

---

# Notas de Manutenção

Sempre que houver mudança em:

- tsconfig.json
- padrões de lint
- convenções de importação
- estratégia de validação com Zod
- estratégia de logging com Pino

esta Skill deve ser revisada.

A Skill `typescript-conventions.md` é considerada a Skill Foundation mais importante do projeto, servindo como base para todas as demais Skills do NovaTech Assistant.