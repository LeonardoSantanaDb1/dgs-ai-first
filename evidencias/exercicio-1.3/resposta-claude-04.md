# Resposta Claude 04 - Implementação da Montagem de Prompt

**Nome:** Leonardo Santana  
**Papel/Cargo:** Desenvolvedor  
**Data:** 2026-06-04

---

# Objetivo

Implementar a etapa de montagem de prompt do pipeline RAG da NovaTech.

O objetivo desta etapa é combinar os chunks recuperados durante a busca semântica com o System Prompt definido para o assistente, produzindo um contexto estruturado e pronto para utilização por um modelo de linguagem.

---

# Resposta Gerada pelo Claude

## Análise da Solução

Antes de gerar a implementação, o Claude realizou uma análise da arquitetura já existente e apresentou recomendações relacionadas à engenharia de contexto e organização do pipeline.

---

# Decisões Técnicas Propostas

## Reutilização da Busca Semântica

### Recomendação

Importar diretamente as funções implementadas em `search.py`, evitando duplicação de código.

### Justificativa

O Claude destacou que as funcionalidades de geração de embeddings e recuperação semântica já foram implementadas e validadas anteriormente.

A reutilização dessas funções reduz acoplamento, melhora a manutenção do código e garante consistência entre a recuperação realizada durante os testes e a recuperação utilizada para construção do prompt.

---

## Separação Entre Contexto Estático e Contexto Dinâmico

### Recomendação

Manter o System Prompt como contexto estático e os chunks recuperados como contexto dinâmico.

### Justificativa

Essa separação reflete diretamente os conceitos de Engenharia de Contexto estudados ao longo da trilha.

O contexto estático define comportamento, regras e guardrails do assistente.

O contexto dinâmico representa o conhecimento recuperado especificamente para cada consulta realizada.

---

## Utilização de Delimitadores de Contexto

### Recomendação

Utilizar marcadores explícitos:

```text
[CONTEXTO_INICIO]
...
[CONTEXTO_FIM]
```

### Justificativa

Segundo o Claude, delimitadores explícitos ajudam o modelo a distinguir instruções do sistema, conteúdo documental e pergunta do usuário.

Essa abordagem reduz riscos de mistura entre contexto e instruções durante a geração da resposta.

---

## Exibição de Estimativa de Tokens

### Recomendação

Exibir uma estimativa do tamanho do prompt gerado.

### Justificativa

A recomendação busca tornar visível o conceito de orçamento de contexto.

A implementação utiliza uma aproximação simples baseada em quantidade de caracteres, permitindo acompanhar o crescimento do prompt sem necessidade de bibliotecas adicionais.

---

## Configuração Flexível do Top-K

### Recomendação

Permitir configuração do número de chunks recuperados.

### Justificativa

Embora Top-K = 3 seja suficiente para a maior parte dos testes da prova de conceito, algumas consultas podem exigir recuperação de um conjunto maior de documentos.

A parametrização aumenta a flexibilidade sem adicionar complexidade significativa à implementação.

---

## Diagnóstico Opcional dos Chunks

### Recomendação

Implementar flag opcional:

```text
--show-chunks
```

### Justificativa

A funcionalidade permite exibir informações de diagnóstico relacionadas aos chunks recuperados, incluindo score de similaridade.

Essa informação é útil para validação e análise crítica do comportamento do pipeline.

---

# Implementação Gerada

Arquivo:

```text
src/prompt_builder.py
```

Responsabilidades implementadas:

- Receber perguntas via linha de comando.
- Reutilizar a busca semântica implementada anteriormente.
- Recuperar os chunks mais relevantes.
- Construir o contexto dinâmico.
- Incorporar o System Prompt.
- Delimitar explicitamente o contexto recuperado.
- Produzir um prompt completo pronto para utilização manual no Claude.
- Exibir estimativa de tamanho do prompt.
- Permitir configuração de Top-K.
- Permitir exibição opcional dos chunks recuperados.

---

# Arquitetura Consolidada do Pipeline

Após a implementação do prompt_builder.py, o pipeline passou a possuir três componentes principais.

## ingest.py

Responsável por:

- leitura dos documentos;
- chunking;
- geração de embeddings;
- armazenamento no ChromaDB.

---

## search.py

Responsável por:

- geração do embedding da pergunta;
- consulta ao banco vetorial;
- recuperação dos chunks mais similares.

---

## prompt_builder.py

Responsável por:

- montagem do contexto final;
- combinação entre contexto estático e dinâmico;
- geração do prompt completo para utilização pelo modelo de linguagem.

---

# Benefícios da Solução

A implementação proposta apresenta os seguintes benefícios:

- Reutilização de componentes já validados.
- Separação clara de responsabilidades.
- Baixo acoplamento.
- Facilidade de manutenção.
- Compatibilidade com futuras integrações via API.
- Melhor visibilidade sobre consumo de contexto.
- Aderência aos princípios de Engenharia de Contexto.

---

# Resultado Esperado

A implementação deverá permitir gerar prompts completos contendo:

- Instruções do sistema.
- Chunks recuperados.
- Pergunta do usuário.

Esses prompts poderão ser utilizados diretamente em modelos de linguagem para validação do comportamento do assistente.

---

# Próximos Passos

Após a implementação do prompt_builder.py serão realizados testes ponta a ponta do pipeline.

O fluxo completo passará a ser:

```text
Pergunta
        ↓
search.py
        ↓
Chunks Recuperados
        ↓
prompt_builder.py
        ↓
Prompt Final
        ↓
Claude
        ↓
Resposta
```

Os resultados desses testes serão utilizados para validar o comportamento completo da solução e preencher as seções finais da análise do exercício.