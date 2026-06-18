Atue como um **Arquiteto de Soluções Sênior**, especialista em AI First, Spec Driven Development, Engenharia de Contexto, GitHub Copilot Instructions e definição de Skills para agentes de IA.

Você recebeu:

1. A solução original do Exercício 2.3 — Estratégia de Skills.
2. Uma revisão crítica detalhada realizada por um Arquiteto Principal.

Sua tarefa agora é produzir uma **VERSÃO REFINADA E FINAL** da solução.

---

# Objetivo

Gerar uma nova versão que:

- Corrija todas as críticas classificadas como Alta.
- Corrija todas as críticas classificadas como Média.
- Preserve os pontos fortes da solução original.
- Mantenha profundidade técnica.
- Não simplifique a arquitetura apenas para reduzir críticas.
- Não remova justificativas arquiteturais relevantes.
- Mantenha aderência ao contexto NovaTech Assistant.
- Mantenha aderência ao Anexo C.
- Mantenha aderência ao papel Desenvolvedor.
- Mantenha aderência aos princípios de Spec Driven Development.

---

# Correções obrigatórias

## 1. Trocar a Skill Foundation principal

Substitua:

```text
error-handling.md
```

por:

```text
typescript-conventions.md
```

como Skill Foundation principal do projeto.

A justificativa deve explicar explicitamente:

- posição raiz na hierarquia de dependências
- impacto transversal
- influência sobre todas as demais Skills
- alinhamento com o papel Desenvolvedor
- alinhamento com a stack TypeScript

Também explicar que:

```text
error-handling.md
```

continua sendo uma Skill crítica,

porém:

- depende de convenções TypeScript
- depende de modelagem de tipos
- depende de tratamento padronizado de erros

Portanto não deve ocupar a posição mais alta da hierarquia.

---

## 2. Corrigir a árvore de dependências

A árvore deve eliminar dependências inadequadas.

Obrigatoriamente:

### NÃO PERMITIR

```text
azure-functions-endpoint
    └── testing-patterns
```

### PERMITIR

```text
testing-patterns
    └── azure-functions-endpoint
```

Justificar tecnicamente a decisão.

Evitar qualquer dependência circular.

Explicar explicitamente que a árvore deve permanecer acíclica.

---

## 3. Resolver a ambiguidade de create-react-card

A solução atual mistura conceitos distintos.

Separar explicitamente:

```text
create-teams-adaptive-card.md
```

e

```text
create-web-response-card.md
```

Para cada uma:

- objetivo
- consumidores
- artefatos gerados
- dependências

Caso decida manter uma única Skill, justificar tecnicamente de forma robusta.

A preferência é separar.

---

## 4. Adicionar cobertura explícita de Zod

A solução refinada deve contemplar Zod de forma explícita.

Pode ser:

### Opção A

Skill própria:

```text
zod-validation-patterns.md
```

### Opção B

Parte formal de:

```text
azure-functions-endpoint.md
```

Independentemente da abordagem escolhida, explicar:

- schemas reutilizáveis
- validação de input
- validação de output
- uso de `z.infer`
- tratamento de `ZodError`
- integração com TypeScript

---

## 5. Adicionar cobertura explícita de Prompt Builder

Criar cobertura formal para construção de prompts.

Pode ser:

### Domain Skill

ou

### Artifact Skill

A Skill deve abordar:

- context budget
- chunking
- grounding
- source_document
- citações
- versionamento de system prompt
- contexto recuperado
- prevenção de alucinação

A justificativa deve estar alinhada ao contexto AI First.

---

## 6. Remover referências não comprovadas pelo Anexo C

Não utilizar exemplos ou módulos não demonstrados pelo contexto.

Exemplo:

```text
metrics.increment()
```

Caso sejam mencionados:

- classificá-los explicitamente como melhoria futura
- não tratá-los como parte do estado atual do projeto

---

## 7. Corrigir o critério de existência das Skills

A solução refinada deve explicar explicitamente:

Uma Skill NÃO deve existir apenas porque é utilizada frequentemente.

Também pode existir porque:

- possui alta criticidade
- possui alto risco
- possui alta complexidade
- possui forte impacto arquitetural

Utilizar como exemplo:

```text
create-rag-endpoint.md
```

mesmo que tenha baixa frequência de criação.

---

## 8. Criar o SKILL.md completo da Skill Foundation principal

Produzir o conteúdo completo de:

```text
skills/foundation/typescript-conventions/SKILL.md
```

Utilizando a estrutura:

```markdown
# TypeScript Conventions

## Contexto

## Regras Prescritivas

## Exemplos DO

## Exemplos DON'T

## Anti-patterns

## Dependências

## Notas de Manutenção
```

---

# Requisitos para o SKILL.md

As regras devem ser:

- objetivas
- verificáveis
- aplicáveis por agentes

Devem contemplar:

### Tipagem

- evitar any
- preferir unknown
- interfaces vs type
- readonly
- discriminated unions

### Assinaturas

- retorno explícito
- promises tipadas

### Azure Functions

- contratos de request/response

### Zod

- schemas
- z.infer

### Logs

- uso de Pino
- sem console.log

### Testabilidade

- separação entre lógica e infraestrutura

---

# Estrutura obrigatória da resposta

A resposta deve ser produzida exatamente como um documento final de certificação.

Utilize a seguinte estrutura:

# Exercício 2.3 — Definição de Estratégia de Skills

## Análise Inicial

## Estratégia de Organização das Skills

## Árvore Completa de Skills

## Matriz de Skills

## Skills Mais Críticas

## Skill Foundation Principal Escolhida

## SKILL.md — typescript-conventions.md

## Autoavaliação Crítica

## Melhorias Futuras

---

# Critérios de qualidade

A solução deve demonstrar:

- aderência ao Anexo C
- aderência ao contexto NovaTech Assistant
- aderência ao papel Desenvolvedor
- entendimento real de Skills
- distinção correta entre Foundation, Domain e Artifact
- coerência de dependências
- visão de engenharia de contexto
- governança para agentes
- integração com SDD
- profundidade técnica adequada para avaliação nota máxima

---

# Importante

Não gere apenas uma versão resumida.

Produza uma versão final completa, pronta para ser salva no arquivo:

```text
exercicio-2.3-skills-strategy.md
```