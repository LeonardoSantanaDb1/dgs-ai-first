# Exercício 2.2 — Implementação de Spec com Spec Driven Development

**Nome:** Leonardo Santana  
**Papel/Cargo:** Desenvolvedor  
**Data:** 2026-06-18  

--- 

# Análise Inicial (Humana)

## Entendimento do Problema

O objetivo deste exercício é aplicar Spec Driven Development no módulo Query Endpoint do projeto NovaTech Assistant.

O fluxo esperado é partir de um `plan.md` já definido pelo Tech Lead, converter esse plano em um `tasks.md` com tarefas atômicas e, em seguida, implementar a primeira task utilizando padrões de produção do projeto.

O foco do exercício não é apenas gerar código, mas demonstrar capacidade de decompor uma especificação técnica em unidades executáveis, manter rastreabilidade entre plano e implementação, e revisar criticamente código gerado por agente de IA.

## Premissas Identificadas

- O Product Specialist já escreveu o `requirements.md`.
- O Tech Lead já escreveu o `plan.md`.
- O Desenvolvedor deve gerar o `tasks.md`.
- O endpoint alvo é o Query Endpoint.
- A implementação deve seguir TypeScript, Azure Functions v4, Zod, Pino e padrões do repositório.
- A primeira task implementada deve ser pequena, verificável e independente.

## Plan.md Recebido

O plano define um Azure Function HTTP Trigger que:

1. Recebe pergunta do atendente via `POST /api/query`.
2. Converte a pergunta em embedding via Azure OpenAI.
3. Busca os top-5 chunks no Azure AI Search.
4. Monta prompt com chunks, system prompt e pergunta.
5. Envia ao GPT-4o.
6. Retorna resposta com `source_document`.

## Decisões Técnicas Relevantes

- TypeScript com Azure Functions v4.
- Zod para validação de input/output.
- Retry com exponential backoff para chamadas Azure.
- Structured logging com Pino.
- Context budget conforme ADR-0002.
- Documentos contraditórios tratados conforme ADR-0003.
- System prompt versionado em `/prompts/system-prompt.md`.

## Estratégia Inicial

A estratégia será decompor o plano em tasks pequenas, ordenadas por dependência técnica.

A primeira task deve criar a base do endpoint, sem tentar implementar todo o fluxo RAG de uma vez. Isso reduz risco, facilita revisão e mantém aderência ao modelo SDD.

## Conclusão Inicial

O exercício deve evidenciar três capacidades principais do papel Desenvolvedor:

1. Transformar plano técnico em tarefas atômicas.
2. Implementar uma primeira unidade funcional do endpoint.
3. Revisar criticamente a saída gerada por IA antes de aceitar o código.

---

# Solução Inicial (Claude)

## Objetivo

Converter o plan.md em um tasks.md contendo tarefas atômicas para implementação do Query Endpoint.

## Resultado

A solução inicial produziu:

- Tasks QE-01 até QE-10
- Mapa de dependências
- Primeira implementação baseada em types.ts
- Revisão crítica inicial do código

## Pontos Positivos

- Boa decomposição do fluxo RAG.
- Dependências parcialmente identificadas.
- Estrutura aderente ao plan.md.

## Fragilidades Identificadas

- Primeira task não entregava endpoint executável.
- Critérios de aceite parcialmente subjetivos.
- Dependências inconsistentes.
- Ausência de task para configuração.

## Evidência

Ver:

- evidencias/exercicio-2.2/01-prompt-solucao-inicial.md

---

# Análise Crítica

## Objetivo

Revisar criticamente a solução inicial buscando inconsistências arquiteturais e problemas de SDD.

## Principais Problemas Encontrados

### Problema 1

Primeira task inadequada para o objetivo do exercício.

### Problema 2

Contradição na task Prompt Builder.

### Problema 3

Dependência invertida entre QE-07 e QE-08.

### Problema 4

Ausência de task para config.ts.

### Problema 5

QE-09 não atômica.

### Problema 6

Critérios de aceite subjetivos.

### Problema 7

Revisão crítica limitada apenas ao types.ts.

## Resultado da Análise

A solução precisava ser refinada antes da implementação.

## Evidência

Ver:

- evidencias/exercicio-2.2/02-prompt-analise-critica.md

---

# Refinamento

## Objetivo

Aplicar todas as correções apontadas na análise crítica.

## Ajustes Realizados

| Problema | Correção |
|-----------|-----------|
| Primeira task inadequada | QE-03 passou a ser a primeira task |
| Dependência QE-07/QE-08 | Corrigida |
| Configuração ausente | Criada task específica |
| QE-09 grande demais | Quebrada em subtasks |
| Critérios subjetivos | Tornados verificáveis |
| Contradição Prompt Builder | Resolvida |

## Resultado

A solução refinada passou a atender integralmente ao fluxo SDD.

## Evidência

Ver:

- evidencias/exercicio-2.2/03-prompt-refinamento.md

---

# Tasks Definidas

A versão final do tasks.md definiu as seguintes entregas:

- QE-00 — Configuração
- QE-01 — Types
- QE-02 — Errors
- QE-03 — Validator + Handler Base
- QE-04 — Search Service
- QE-05 — Completion Service
- QE-06 — Prompt Builder
- QE-07 — Handler Completo
- QE-08 — Response Builder
- QE-09A até QE-09D — Testes Unitários
- QE-10 — Teste de Integração

## Evidência

Ver:

- evidencias/exercicio-2.2/04-tasks-md-gerado.md

---

# Primeira Task Implementada

## Task Escolhida

QE-03 — Setup do Endpoint com Validação

## Tecnologias Demonstradas

- Azure Functions v4
- TypeScript
- Zod
- Pino

## Arquivos Implementados

- handler.ts
- validator.ts
- errors.ts
- types.ts
- config.ts
- logger.ts

## Resultado

O endpoint já é capaz de:

- Receber requisições
- Validar payload
- Retornar erros estruturados
- Gerar requestId
- Produzir logs estruturados

## Evidência

Ver:

- evidencias/exercicio-2.2/05-codigo-primeira-task.md

---

# Revisão Crítica do Código

## Principais Pontos Identificados

### 1. ADR ainda não criada

RequestContext depende de ADR-0004.

### 2. Tratamento de JSON inválido

Pode ser refinado.

### 3. randomUUID

Pode utilizar import explícito.

### 4. Evolução do handleError

Novos erros precisarão ser mapeados.

## Evidência

Ver:

- evidencias/exercicio-2.2/06-revisao-critica-codigo.md

---

# Conclusão Final

O exercício demonstrou a aplicação completa do ciclo Spec Driven Development:

Requirements
→ Plan
→ Tasks
→ Implementação
→ Revisão
→ Refinamento

O Query Endpoint foi decomposto em tarefas atômicas, a primeira entrega funcional foi implementada e o código passou por revisão crítica antes de sua aprovação.

O resultado final está aderente ao papel Desenvolvedor, aos padrões definidos pelo projeto NovaTech Assistant e aos critérios da certificação AI First.