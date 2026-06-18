# Análise Crítica — Exercício 2.2

## Objetivo da Revisão

Avaliar criticamente a solução inicial produzida para o Exercício 2.2, identificando riscos, inconsistências, problemas de modelagem das tasks e desvios em relação ao enunciado da certificação.

---

## Principais Problemas Identificados

### 1. Primeira Task Escolhida Não Atende à Expectativa do Exercício

**Gravidade:** Alta

A task QE-01 foi definida como a criação do arquivo `src/shared/types.ts`.

Embora tecnicamente correta como dependência arquitetural, ela não atende à expectativa do exercício, que sugere explicitamente a implementação inicial do endpoint com validação de entrada.

Problemas identificados:

- Não demonstra Azure Functions v4.
- Não demonstra utilização de Zod.
- Não demonstra utilização de Pino.
- Não gera um endpoint executável.

**Impacto:**

Risco elevado de perda de nota no critério de implementação prática.

**Correção sugerida:**

Implementar inicialmente o setup do endpoint e a validação de input utilizando Azure Functions v4 e Zod.

---

### 2. Contradição na Task QE-06

**Gravidade:** Alta

A task QE-06 contém dois critérios mutuamente exclusivos:

- Ler o system prompt diretamente do arquivo em runtime.
- Manter a função pura recebendo o conteúdo via parâmetro.

Uma função não pode simultaneamente realizar leitura de arquivo e ser considerada pura.

**Impacto:**

Ambiguidade durante implementação e validação.

**Correção sugerida:**

Manter o prompt-builder puro.

A leitura do arquivo deve ocorrer no handler ou em camada de infraestrutura.

---

### 3. Dependência Invertida Entre QE-07 e QE-08

**Gravidade:** Alta

O diagrama de dependências mostra:

```text
QE-07
 └── QE-08
```

Entretanto o handler depende diretamente do response-builder.

A relação correta deveria ser:

```text
QE-08
 └── QE-07
```

#### Impacto

Ordem de implementação inconsistente.

O handler não pode ser implementado antes da existência do response-builder.

#### Correção Sugerida

Atualizar o grafo de dependências para refletir corretamente a relação entre as tasks.

O response-builder deve ser implementado antes do handler.
 
---

### 4. Ausência de Task Para Configuração

**Gravidade:** Média

As tasks `QE-04` e `QE-05` dependem de configurações armazenadas em `src/shared/config.ts`.

Entretanto, nenhuma task foi criada para definir explicitamente esse arquivo ou estabelecer seu contrato.

#### Impacto

Existe uma dependência implícita não controlada.

Isso pode gerar divergências entre implementações, alterações não coordenadas e inconsistências na configuração utilizada pelos serviços de Search e Completion.

#### Correção Sugerida

Criar uma task específica para definição da configuração da aplicação.

Exemplo:

```text
QE-03A — Criar src/shared/config.ts

Critérios de aceite:
- Variáveis de ambiente tipadas
- Validação de configuração na inicialização
- Exportação centralizada das configurações
```

---

### 5. QE-09 Não É Atômica

**Gravidade:** Alta

A task `QE-09` concentra múltiplas responsabilidades:

- Criação de fixtures
- Testes do validator
- Testes do prompt-builder
- Testes do response-builder

Isso viola o princípio de atomicidade definido para o exercício.

#### Impacto

Dificulta rastreabilidade, revisão, aprovação e identificação de falhas.

Caso apenas uma parte da task falhe, toda a entrega fica bloqueada.

#### Correção Sugerida

Separar a task em unidades menores e independentes.

Exemplo:

```text
QE-09A — Fixtures compartilhadas

QE-09B — Testes do validator

QE-09C — Testes do response-builder

QE-09D — Testes do prompt-builder
```

---

### 6. Critérios de Aceite Não Totalmente Verificáveis

**Gravidade:** Média

Alguns critérios definidos no `tasks.md` são subjetivos e difíceis de validar objetivamente.

Exemplos:

- "Não loga dados sensíveis"
- "Não contém lógica de negócio"

#### Impacto

Critérios subjetivos podem gerar interpretações diferentes entre desenvolvedores, revisores e avaliadores.

Além disso, dificultam a automação de validações em pipelines de integração contínua.

#### Correção Sugerida

Substituir critérios subjetivos por critérios observáveis e verificáveis.

Exemplos:

**Em vez de:**

```text
Não loga dados sensíveis
```

**Utilizar:**

```text
Nenhuma chamada ao logger contém os campos
question ou content dos chunks.
```

**Em vez de:**

```text
Não contém lógica de negócio
```

**Utilizar:**

```text
Toda transformação de domínio ocorre em módulos de service.
O handler apenas orquestra chamadas e mapeia erros.
```

Dessa forma os critérios passam a ser objetivos, auditáveis e passíveis de validação automatizada.

---

### 7. Revisão Crítica Focada Apenas em Types.ts

**Gravidade:** Média

A revisão crítica realizada concentrou-se exclusivamente no arquivo `types.ts`.

Não foram avaliados aspectos estruturais do próprio `tasks.md`.

#### Impacto

Problemas relevantes permaneceram sem identificação durante a revisão.

Entre eles:

- Dependências inconsistentes
- Tasks não atômicas
- Critérios de aceite subjetivos
- Ordem inadequada de implementação

#### Correção Sugerida

Expandir o escopo da revisão crítica para incluir tanto o código produzido quanto os artefatos de planejamento.

Itens mínimos a serem revisados:

- Dependências entre tasks
- Atomicidade das tasks
- Critérios de aceite
- Ordem de implementação
- Consistência com o `plan.md`
- Aderência aos padrões do projeto

Dessa forma, a revisão passa a cobrir não apenas o código implementado, mas também a qualidade do processo de Spec Driven Development e a coerência entre planejamento, implementação e validação.